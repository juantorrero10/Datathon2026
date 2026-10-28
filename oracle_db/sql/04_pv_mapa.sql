-- =====================================================================
-- 04_pv_mapa — Modelo masivo del mapa: un año -> métricas de 155 municipios
--
-- Firma:  PV_MAPA(p_anio) RETURN CLOB  (JSON)
--
-- IMPLEMENTACIÓN: una ÚNICA SQL masiva (EXECUTE IMMEDIATE, sin binds en los
-- CTE — los parámetros se incrustan como literales ENTEROS/TEXTO controlados)
-- con las 7 PREDICTION en línea. Coste: ~3 s frente a ~50 s del cursor.
--
-- Para CADA municipio (PV_BASE_MODELOS × 155):
--   1. M1_DEMOGRAFIA  -> factor de crecimiento poblacional hasta p_anio
--                        (año <= 2025: corte real, factor = 1)
--   2. estado proyectado: población base + stocks constantes -> ratios
--   3. M2_CAPACIDAD_{DEM,VIV,SER,ACC,EMP} -> 5 dimensiones del año
--   4. M3_VALOR -> factor del valor catastral proyectado
--   5. índice ponderado (0.20/0.15/0.25/0.25/0.15) + factor limitante
--
-- EXTRAPOLACIÓN SOSTENIDA (>5 años): el modelo solo tiene labels hasta 2025
-- (h=5). Para horizontes mayores se consulta el modelo con h=5 y el factor
-- se compone geométricamente hasta el objetivo:
--     f(h) = POWER(f5, h/5)
-- Para h <= 5 es exactamente el valor del modelo (exponente = 1).
--
-- Requiere: PV_BASE_MODELOS (01), modelos ONNX (M1/M2/M3), PV_MUN_BASE
-- (dims/índice 2025). Los stocks no crecen solos (misma regla que el
-- Simulador).
-- =====================================================================

CREATE OR REPLACE FUNCTION PV_MAPA (
    P_ANIO IN NUMBER
) RETURN CLOB IS
    V_JSON       CLOB;
    V_SQL        VARCHAR2(32767);
    V_FUT        NUMBER;
    V_HORIZON    NUMBER;
    V_H_MODEL    NUMBER;
    V_EXPO       VARCHAR2(32);
    V_ERR_MIL    NUMBER;
    V_FACTOR_M3  VARCHAR2(4000);
    V_FACTOR_M6  VARCHAR2(4000);
    V_FACTOR_M7_VIV VARCHAR2(4000);
    V_FACTOR_M7_SAL VARCHAR2(4000);
    V_FACTOR_M7_PAR VARCHAR2(4000);
BEGIN
    IF NVL(P_ANIO, 2025) <= 2025 THEN
        V_FUT       := 0;
        V_HORIZON   := 1;
        V_H_MODEL   := 1;
        V_EXPO      := '1';
        V_ERR_MIL   := 930;
        V_FACTOR_M3 := '1';
        V_FACTOR_M6 := '1';
    ELSE
        V_FUT     := 1;
        V_HORIZON := LEAST(P_ANIO - 2025, 10);
        V_H_MODEL := LEAST(V_HORIZON, 5);
        V_EXPO := REPLACE(TO_CHAR(V_HORIZON / V_H_MODEL, 'FM990.999999'), ',', '.');
        V_ERR_MIL := CASE
                         WHEN V_HORIZON <= 1 THEN 930
                         WHEN V_HORIZON <= 2 THEN 1340
                         WHEN V_HORIZON <= 3 THEN 1340
                         WHEN V_HORIZON <= 4 THEN 1620
                         ELSE 2200
                     END;

        V_FACTOR_M3 := 'EXP(PREDICTION(M1_DEMOGRAFIA USING '
            || 'b.LOG_POB   AS LOG_POB,   b.CAGR_1    AS CAGR_1,'
            || 'b.CAGR_3    AS CAGR_3,    b.CAGR_5    AS CAGR_5,'
            || 'b.CAGR_10   AS CAGR_10,   b.VOL_5     AS VOL_5,'
            || 'b.EDAD_MEDIA AS EDAD_MEDIA, b.PCT_MENOR_15 AS PCT_MENOR_15,'
            || 'b.PCT_65MAS AS PCT_65MAS, b.REEMPLAZAMIENTO AS REEMPLAZAMIENTO,'
            || 'b.PARO_100  AS PARO_100,  b.VAR_PARO  AS VAR_PARO,'
            || 'b.MIGRACION_3Y AS MIGRACION_3Y,'
            || 'b.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM,'
            || 'b.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN, '
            || V_H_MODEL || ' AS HORIZONTE))';

        V_FACTOR_M6 := 'EXP(PREDICTION(M3_VALOR USING '
            || 'e.LOG_VALOR AS LOG_VALOR, e.VCAGR_1 AS VCAGR_1, e.VCAGR_3 AS VCAGR_3,'
            || 'e.VCAGR_5 AS VCAGR_5, e.VCAGR_10 AS VCAGR_10, e.VVOL_5 AS VVOL_5,'
            || 'e.LOG_POB AS LOG_POB, e.CAGR_5 AS CAGR_5, e.VOL_5 AS VOL_5,'
            || 'e.EDAD_MEDIA AS EDAD_MEDIA, e.PCT_65MAS AS PCT_65MAS,'
            || 'e.REEMPLAZAMIENTO AS REEMPLAZAMIENTO, e.PARO_100 AS PARO_100,'
            || 'e.VAR_PARO AS VAR_PARO, e.MIGRACION_3Y AS MIGRACION_3Y,'
            || 'e.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM,'
            || 'e.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN, '
            || V_H_MODEL || ' AS HORIZONTE))';
    END IF;

    -- ── M4 · factores de los stocks proyectados (viviendas/salud/paradas) ──
    -- factor = EXP(pred(5)) compuesto con V_EXPO para h > 5 (patrón M1/M3). El
    -- stock proyectado sale de la escala log1p: stock_y = (stock+1)*f - 1.
    V_FACTOR_M7_VIV := 'EXP(PREDICTION(M4_VIVIENDAS USING '
        || 'LN(p.VIV_STOCK + 1) AS LOG_ST, p.VIV_CAGR_1 AS ST_CAGR_1, p.VIV_CAGR_3 AS ST_CAGR_3,'
        || 'p.VIV_CAGR_5 AS ST_CAGR_5, p.VIV_CAGR_10 AS ST_CAGR_10, p.VIV_VOL_5 AS ST_VOL_5,'
        || 'p.VIV_P1000 AS ST_P1000, p.VIV_LOG_POB AS LOG_POB, p.VIV_POB_CAGR_5 AS POB_CAGR_5,'
        || V_H_MODEL || ' AS HORIZONTE))';
    V_FACTOR_M7_SAL := 'EXP(PREDICTION(M4_SALUD USING '
        || 'LN(p.CENTROS_SALUD_NUM + 1) AS LOG_ST, p.SAL_CAGR_1 AS ST_CAGR_1, p.SAL_CAGR_3 AS ST_CAGR_3,'
        || 'p.SAL_CAGR_5 AS ST_CAGR_5, p.SAL_CAGR_10 AS ST_CAGR_10, p.SAL_VOL_5 AS ST_VOL_5,'
        || 'p.SAL_P1000 AS ST_P1000, p.SAL_LOG_POB AS LOG_POB, p.SAL_POB_CAGR_5 AS POB_CAGR_5,'
        || V_H_MODEL || ' AS HORIZONTE))';
    V_FACTOR_M7_PAR := 'EXP(PREDICTION(M4_PARADAS USING '
        || 'LN(p.PARADAS_BASE + 1) AS LOG_ST, p.PAR_CAGR_1 AS ST_CAGR_1, p.PAR_CAGR_3 AS ST_CAGR_3,'
        || 'p.PAR_CAGR_5 AS ST_CAGR_5, p.PAR_CAGR_10 AS ST_CAGR_10, p.PAR_VOL_5 AS ST_VOL_5,'
        || 'p.PAR_P1000 AS ST_P1000, p.PAR_LOG_POB AS LOG_POB, p.PAR_POB_CAGR_5 AS POB_CAGR_5,'
        || V_H_MODEL || ' AS HORIZONTE))';

    V_SQL :=
        'WITH proy AS (' ||
        'SELECT b.COD_INE, b.NOMBRE, b.POBLACION_2025, b.LAT, b.LON, ' ||
        'CASE WHEN ' || V_FUT || ' = 0 THEN 1 ELSE POWER(' || V_FACTOR_M3 || ', ' || V_EXPO || ') END AS FACTOR_M3, ' ||
        'b.VALOR_2025, ' ||
        'b.LOG_VALOR, b.VCAGR_1, b.VCAGR_3, b.VCAGR_5, b.VCAGR_10, b.VVOL_5, ' ||
        'b.LOG_POB, b.CAGR_1, b.CAGR_3, b.CAGR_5, b.CAGR_10, b.VOL_5, ' ||
        'b.EDAD_MEDIA, b.PCT_MENOR_15, b.PCT_65MAS, b.REEMPLAZAMIENTO, b.PARO_100, b.VAR_PARO, ' ||
        'b.MIGRACION_3Y, b.DISTANCIA_SOL_KM, b.TIEMPO_CENTRO, b.CREC_10Y_BASE, ' ||
        'b.CENTROS_SALUD_NUM, b.ESCUELAS, b.PARADAS_BASE, b.TELEFONO, b.VIV_STOCK, ' ||
        -- M4: features de los stocks completas para las PREDICTION de estp
        'b.VIV_LOG_POB, b.VIV_LOG_ST, b.VIV_CAGR_1, b.VIV_CAGR_3, b.VIV_CAGR_5, b.VIV_CAGR_10, b.VIV_VOL_5, b.VIV_P1000, b.VIV_POB_CAGR_5, ' ||
        'b.SAL_LOG_POB, b.SAL_LOG_ST, b.SAL_CAGR_1, b.SAL_CAGR_3, b.SAL_CAGR_5, b.SAL_CAGR_10, b.SAL_VOL_5, b.SAL_P1000, b.SAL_POB_CAGR_5, ' ||
        'b.PAR_LOG_POB, b.PAR_LOG_ST, b.PAR_CAGR_1, b.PAR_CAGR_3, b.PAR_CAGR_5, b.PAR_CAGR_10, b.PAR_VOL_5, b.PAR_P1000, b.PAR_POB_CAGR_5 ' ||
        'FROM PV_BASE_MODELOS b), ' ||
        'estp AS (' ||
        'SELECT p.*, p.POBLACION_2025 * p.FACTOR_M3 AS POB_Y, ' ||
        'LN(GREATEST(p.POBLACION_2025 * p.FACTOR_M3, 0.5)) AS LOG_POB_Y, ' ||
        'CASE WHEN ' || V_FUT || ' = 0 THEN p.CREC_10Y_BASE ' ||
        'ELSE CASE WHEN p.FACTOR_M3 > 0 THEN POWER(p.FACTOR_M3, 1 / ' || V_HORIZON || ') - 1 ELSE 0 END END AS CREC_Y, ' ||
        -- M4: stocks proyectados (escenario: lo que se predeciría construir)
        'CASE WHEN ' || V_FUT || ' = 0 THEN p.VIV_STOCK ' ||
        'ELSE (p.VIV_STOCK + 1) * POWER(' || V_FACTOR_M7_VIV || ', ' || V_EXPO || ') - 1 END AS VIV_STOCK_Y, ' ||
        'CASE WHEN ' || V_FUT || ' = 0 THEN p.CENTROS_SALUD_NUM ' ||
        'ELSE (p.CENTROS_SALUD_NUM + 1) * POWER(' || V_FACTOR_M7_SAL || ', ' || V_EXPO || ') - 1 END AS SALUD_NUM_Y, ' ||
        'CASE WHEN ' || V_FUT || ' = 0 THEN p.PARADAS_BASE ' ||
        'ELSE (p.PARADAS_BASE + 1) * POWER(' || V_FACTOR_M7_PAR || ', ' || V_EXPO || ') - 1 END AS PARADAS_NUM_Y, ' ||
        -- escuelas esperadas: el ESC es cross-sectional; el stock proyectado
        -- crece por la PROPORCIÓN del "esperado por tamaño" entre pob_y y
        -- pob_2025 (un municipio sin escuelas hoy no las gana de la nada)
        'CASE WHEN ' || V_FUT || ' = 0 THEN p.ESCUELAS ' ||
        'ELSE p.ESCUELAS * PREDICTION(M4_ESCUELAS USING LN(GREATEST(p.POBLACION_2025 * p.FACTOR_M3, 0.5)) AS LOG_POB, p.EDAD_MEDIA AS EDAD_MEDIA, p.PCT_MENOR_15 AS PCT_MENOR_15, p.PCT_65MAS AS PCT_65MAS, p.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM, p.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN) / NULLIF(PREDICTION(M4_ESCUELAS USING LN(GREATEST(p.POBLACION_2025, 0.5)) AS LOG_POB, p.EDAD_MEDIA AS EDAD_MEDIA, p.PCT_MENOR_15 AS PCT_MENOR_15, p.PCT_65MAS AS PCT_65MAS, p.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM, p.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN), 0) END AS ESCUELAS_Y, ' ||
        'p.CENTROS_SALUD_NUM / p.POBLACION_2025 * 10000 AS SALUD_10K_25, ' ||
        'p.ESCUELAS          / p.POBLACION_2025 * 1000  AS ESCUELAS_1000_25, ' ||
        'p.PARADAS_BASE      / p.POBLACION_2025 * 1000  AS PARADAS_1000_25, ' ||
        'p.TELEFONO          / p.POBLACION_2025 * 1000  AS TELEFONO_1000_25, ' ||
        'p.VIV_STOCK         / p.POBLACION_2025 * 1000  AS VIV_1000_25 ' ||
        'FROM proy p), ' ||
        'est AS (' ||
        'SELECT f.*, ' ||
        'f.SALUD_NUM_Y  / f.POBLACION_2025 / f.FACTOR_M3 * 10000 AS SALUD_10K_Y, ' ||
        'f.ESCUELAS_Y   / f.POBLACION_2025 / f.FACTOR_M3 * 1000  AS ESCUELAS_1000_Y, ' ||
        'f.PARADAS_NUM_Y / f.POBLACION_2025 / f.FACTOR_M3 * 1000 AS PARADAS_1000_Y, ' ||
        'f.TELEFONO     / f.POBLACION_2025 / f.FACTOR_M3 * 1000  AS TELEFONO_1000_Y, ' ||
        'f.VIV_STOCK_Y  / f.POBLACION_2025 / f.FACTOR_M3 * 1000  AS VIV_1000_Y ' ||
        'FROM estp f), ' ||
        'dims AS (' ||
        'SELECT e.*, ' ||
        'POWER(' || V_FACTOR_M6 || ', ' || V_EXPO || ') AS FACTOR_M6, ' ||
        'PREDICTION(M2_CAPACIDAD_DEM USING e.LOG_POB_Y AS LOG_POB, e.SALUD_10K_Y AS SALUD_10K, e.ESCUELAS_1000_Y AS ESCUELAS_1000, e.PARADAS_1000_Y AS PARADAS_1000, e.TELEFONO_1000_Y AS TELEFONO_1000, e.VIV_1000_Y AS VIV_1000, e.CREC_Y AS CREC_10Y_PCT, e.PCT_MENOR_15 AS PCT_MENOR_15, e.PCT_65MAS AS PCT_65MAS, e.REEMPLAZAMIENTO AS REEMPLAZAMIENTO, e.PARO_100 AS PARO_100, e.VAR_PARO AS VAR_PARO, e.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN, e.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM) AS DIM_DEM_Y, ' ||
        'PREDICTION(M2_CAPACIDAD_VIV USING e.LOG_POB_Y AS LOG_POB, e.SALUD_10K_Y AS SALUD_10K, e.ESCUELAS_1000_Y AS ESCUELAS_1000, e.PARADAS_1000_Y AS PARADAS_1000, e.TELEFONO_1000_Y AS TELEFONO_1000, e.VIV_1000_Y AS VIV_1000, e.CREC_Y AS CREC_10Y_PCT, e.PCT_MENOR_15 AS PCT_MENOR_15, e.PCT_65MAS AS PCT_65MAS, e.REEMPLAZAMIENTO AS REEMPLAZAMIENTO, e.PARO_100 AS PARO_100, e.VAR_PARO AS VAR_PARO, e.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN, e.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM) AS DIM_VIV_Y, ' ||
        'PREDICTION(M2_CAPACIDAD_SER USING e.LOG_POB_Y AS LOG_POB, e.SALUD_10K_Y AS SALUD_10K, e.ESCUELAS_1000_Y AS ESCUELAS_1000, e.PARADAS_1000_Y AS PARADAS_1000, e.TELEFONO_1000_Y AS TELEFONO_1000, e.VIV_1000_Y AS VIV_1000, e.CREC_Y AS CREC_10Y_PCT, e.PCT_MENOR_15 AS PCT_MENOR_15, e.PCT_65MAS AS PCT_65MAS, e.REEMPLAZAMIENTO AS REEMPLAZAMIENTO, e.PARO_100 AS PARO_100, e.VAR_PARO AS VAR_PARO, e.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN, e.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM) AS DIM_SER_Y, ' ||
        'PREDICTION(M2_CAPACIDAD_ACC USING e.LOG_POB_Y AS LOG_POB, e.SALUD_10K_Y AS SALUD_10K, e.ESCUELAS_1000_Y AS ESCUELAS_1000, e.PARADAS_1000_Y AS PARADAS_1000, e.TELEFONO_1000_Y AS TELEFONO_1000, e.VIV_1000_Y AS VIV_1000, e.CREC_Y AS CREC_10Y_PCT, e.PCT_MENOR_15 AS PCT_MENOR_15, e.PCT_65MAS AS PCT_65MAS, e.REEMPLAZAMIENTO AS REEMPLAZAMIENTO, e.PARO_100 AS PARO_100, e.VAR_PARO AS VAR_PARO, e.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN, e.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM) AS DIM_ACC_Y, ' ||
        'PREDICTION(M2_CAPACIDAD_EMP USING e.LOG_POB_Y AS LOG_POB, e.SALUD_10K_Y AS SALUD_10K, e.ESCUELAS_1000_Y AS ESCUELAS_1000, e.PARADAS_1000_Y AS PARADAS_1000, e.TELEFONO_1000_Y AS TELEFONO_1000, e.VIV_1000_Y AS VIV_1000, e.CREC_Y AS CREC_10Y_PCT, e.PCT_MENOR_15 AS PCT_MENOR_15, e.PCT_65MAS AS PCT_65MAS, e.REEMPLAZAMIENTO AS REEMPLAZAMIENTO, e.PARO_100 AS PARO_100, e.VAR_PARO AS VAR_PARO, e.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN, e.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM) AS DIM_EMP_Y ' ||
        'FROM est e) ' ||
        'SELECT JSON_OBJECT(' ||
        '''anio'' VALUE ' || NVL(P_ANIO, 2025) || ', ' ||
        '''generado'' VALUE TO_CHAR(SYSDATE, ''YYYY-MM-DD"T"HH24:MI:SS''), ' ||
        '''municipios'' VALUE JSON_ARRAYAGG(' ||
        'JSON_OBJECT(' ||
        '''cod'' VALUE d.COD_INE, ' ||
        '''nombre'' VALUE d.NOMBRE, ' ||
        '''lat'' VALUE ROUND(d.LAT, 6), ' ||
        '''lon'' VALUE ROUND(d.LON, 6), ' ||
        '''pob_2025'' VALUE ROUND(d.POBLACION_2025), ' ||
        '''pob_y'' VALUE ROUND(d.POB_Y), ' ||
        '''d_pob'' VALUE ROUND(d.POB_Y - d.POBLACION_2025), ' ||
        '''d_pob_pct'' VALUE ROUND((d.FACTOR_M3 - 1) * 100, 2), ' ||
        '''p10'' VALUE ROUND(d.POB_Y * (1000 - ' || V_ERR_MIL || ') / 1000), ' ||
        '''p90'' VALUE ROUND(d.POB_Y * (1000 + ' || V_ERR_MIL || ') / 1000), ' ||
        '''dim_dem_2025'' VALUE ROUND(b2.DIM_DEM, 1), ''dim_dem_y'' VALUE ROUND(d.DIM_DEM_Y, 1), ' ||
        '''dim_viv_2025'' VALUE ROUND(b2.DIM_VIV, 1), ''dim_viv_y'' VALUE ROUND(d.DIM_VIV_Y, 1), ' ||
        '''dim_ser_2025'' VALUE ROUND(b2.DIM_SER, 1), ''dim_ser_y'' VALUE ROUND(d.DIM_SER_Y, 1), ' ||
        '''dim_acc_2025'' VALUE ROUND(b2.DIM_ACC, 1), ''dim_acc_y'' VALUE ROUND(d.DIM_ACC_Y, 1), ' ||
        '''dim_emp_2025'' VALUE ROUND(b2.DIM_EMP, 1), ''dim_emp_y'' VALUE ROUND(d.DIM_EMP_Y, 1), ' ||
        '''indice_2025'' VALUE ROUND(b2.INDICE, 1), ' ||
        '''indice_y'' VALUE ROUND(d.DIM_DEM_Y * 0.20 + d.DIM_VIV_Y * 0.15 + d.DIM_SER_Y * 0.25 + d.DIM_ACC_Y * 0.25 + d.DIM_EMP_Y * 0.15, 1), ' ||
        '''d_indice'' VALUE ROUND((d.DIM_DEM_Y * 0.20 + d.DIM_VIV_Y * 0.15 + d.DIM_SER_Y * 0.25 + d.DIM_ACC_Y * 0.25 + d.DIM_EMP_Y * 0.15) - b2.INDICE, 1), ' ||
        '''factor_limitante'' VALUE CASE ' ||
        'WHEN LEAST(d.DIM_DEM_Y, d.DIM_VIV_Y, d.DIM_SER_Y, d.DIM_ACC_Y, d.DIM_EMP_Y) = d.DIM_DEM_Y THEN ''Demografía'' ' ||
        'WHEN LEAST(d.DIM_DEM_Y, d.DIM_VIV_Y, d.DIM_SER_Y, d.DIM_ACC_Y, d.DIM_EMP_Y) = d.DIM_VIV_Y THEN ''Vivienda'' ' ||
        'WHEN LEAST(d.DIM_DEM_Y, d.DIM_VIV_Y, d.DIM_SER_Y, d.DIM_ACC_Y, d.DIM_EMP_Y) = d.DIM_SER_Y THEN ''Servicios'' ' ||
        'WHEN LEAST(d.DIM_DEM_Y, d.DIM_VIV_Y, d.DIM_SER_Y, d.DIM_ACC_Y, d.DIM_EMP_Y) = d.DIM_ACC_Y THEN ''Accesibilidad'' ' ||
        'ELSE ''Empleo'' END, ' ||
        '''salud_10k_2025'' VALUE ROUND(d.SALUD_10K_25, 2), ''salud_10k_y'' VALUE ROUND(d.SALUD_10K_Y, 2), ' ||
        '''escuelas_1000_2025'' VALUE ROUND(d.ESCUELAS_1000_25, 3), ''escuelas_1000_y'' VALUE ROUND(d.ESCUELAS_1000_Y, 3), ' ||
        '''paradas_1000_2025'' VALUE ROUND(d.PARADAS_1000_25, 3), ''paradas_1000_y'' VALUE ROUND(d.PARADAS_1000_Y, 3), ' ||
        '''viv_1000_2025'' VALUE ROUND(d.VIV_1000_25, 1), ''viv_1000_y'' VALUE ROUND(d.VIV_1000_Y, 1), ' ||
        '''valor_2025'' VALUE ROUND(d.VALOR_2025, 0), ''valor_y'' VALUE ROUND(d.VALOR_2025 * d.FACTOR_M6, 0), ' ||
        '''d_valor_pct'' VALUE ROUND((d.FACTOR_M6 - 1) * 100, 2) ' ||
        'RETURNING CLOB) ORDER BY d.NOMBRE RETURNING CLOB) ' ||
        'RETURNING CLOB) ' ||
        'FROM dims d LEFT JOIN PV_MUN_BASE b2 ON b2.COD_INE = d.COD_INE';

    EXECUTE IMMEDIATE V_SQL INTO V_JSON;
    RETURN V_JSON;
END;

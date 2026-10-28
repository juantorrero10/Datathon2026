-- =====================================================================
-- 03_pv_simula_v2 — Función del simulador What-If (M3 + M4 en Oracle)
--
-- Firma:  PV_SIMULA(p_cod, p_anio, p_add_pop, p_add_viv, p_add_salud,
--                   p_add_esc, p_add_paradas) RETURN CLOB  (JSON)
--
-- Orden de ejecución (por diseño, M3 SIEMPRE antes de M4):
--   1. M3_DEMOGRAFIA  → factor de crecimiento hasta p_anio
--                      (para año <= 2025 usa la serie real de PV_SERIE)
--   2. etado simulado: base(año) + choque del usuario → ratios
--   3. M4_CAPACIDAD_{DEM,VIV,SER,ACC,EMP} → 5 dimensiones (0-100)
--   4. índice (pesos fijos 0.20/0.15/0.25/0.25/0.15) y factor limitante
--      (argmin de las 5 dims) — SQL determinista, sin modelo
--
-- Requiere: PV_BASE_M3_M4 (01), modelos ONNX (02), PV_SERIE y PV_MUN_BASE.
-- Bandas del M3: mediana de |err| % por horizonte (ficha
-- oracle_db/models/m3_demografia.json); horizontes > 5 son extrapolación
-- y usan la banda de h=5 (2,2 %) como mínimo declarado.
-- =====================================================================

CREATE OR REPLACE FUNCTION PV_SIMULA (
    P_COD          IN VARCHAR2,
    P_ANIO         IN NUMBER,
    P_ADD_POP      IN NUMBER DEFAULT 0,
    P_ADD_VIV      IN NUMBER DEFAULT 0,
    P_ADD_SALUD    IN NUMBER DEFAULT 0,
    P_ADD_ESC      IN NUMBER DEFAULT 0,
    P_ADD_PARADAS  IN NUMBER DEFAULT 0
) RETURN CLOB IS
    R             PV_BASE_M3_M4%ROWTYPE;
    V_JSON        CLOB;
    V_HORIZON     NUMBER;
    V_FACTOR      NUMBER := 1;
    V_ERR_PCT     NUMBER;
    V_POB_BASE    NUMBER;
    V_POB25       NUMBER;
    V_P10         NUMBER;
    V_P90         NUMBER;
    V_POB_SIM     NUMBER;
    V_LOG_POB     NUMBER;
    V_CREC        NUMBER;
    V_SALUD_10K   NUMBER;
    V_ESC_1000    NUMBER;
    V_PAR_1000    NUMBER;
    V_VIV_1000    NUMBER;
    V_DIM_DEM     NUMBER;
    V_DIM_VIV     NUMBER;
    V_DIM_SER     NUMBER;
    V_DIM_ACC     NUMBER;
    V_DIM_EMP     NUMBER;

    -- "antes": mismo estado base que "después" y que el mapa (PV_BASE_M3_M4).
    -- PV_MUN_BASE se usa SOLO para las dims/índice del corte 2025 (ranks de
    -- cohorte). Los stares/ratios de PV_MUN_BASE quedan fuera: su SALUD_10K se
    -- computó sin sumar CONSULTORIOS (121/155 con servicio real a 0 en el
    --	store) y con sanidad 2025 vacía sin el "último dato disponible" — eso
    --    pantallaaba 0,000 en el WI frente a 142,86 en el mapa.
    B_POB         NUMBER;  B_VIV NUMBER;  B_SALUD NUMBER;  B_ESC NUMBER;  B_PAR NUMBER;
    BS_10K        NUMBER;  BS_E1000 NUMBER;  BS_P1000 NUMBER;  BS_V1000 NUMBER;
    BD_DEM        NUMBER;  BD_VIV NUMBER;  BD_SER NUMBER;  BD_ACC NUMBER;  BD_EMP NUMBER;
    B_INDICE      NUMBER;
BEGIN
    -- ── 0 · estado base (features con paridad de entrenamiento) ──
    SELECT * INTO R FROM PV_BASE_M3_M4 WHERE COD_INE = P_COD;
    SELECT DIM_DEM, DIM_VIV, DIM_SER, DIM_ACC, DIM_EMP, INDICE
      INTO BD_DEM, BD_VIV, BD_SER, BD_ACC, BD_EMP, B_INDICE
      FROM PV_MUN_BASE WHERE COD_INE = P_COD;

    -- stocks "antes" = mismos stocks que "después" sin choque del usuario
    B_POB   := R.POBLACION_2025;
    B_VIV   := R.VIV_STOCK;
    B_SALUD := R.CENTROS_SALUD_NUM;
    B_ESC   := R.ESCUELAS;
    B_PAR   := R.PARADAS_BASE;
    BS_10K   := CASE WHEN B_POB > 0 THEN B_SALUD / B_POB * 10000 ELSE 0 END;
    BS_E1000 := CASE WHEN B_POB > 0 THEN B_ESC   / B_POB * 1000  ELSE 0 END;
    BS_P1000 := CASE WHEN B_POB > 0 THEN B_PAR   / B_POB * 1000  ELSE 0 END;
    BS_V1000 := CASE WHEN B_POB > 0 THEN B_VIV   / B_POB * 1000  ELSE 0 END;

    -- ── 1 · M3: factor de crecimiento hacia p_anio ──
    IF NVL(P_ANIO, 2025) <= 2025 THEN
        V_HORIZON := GREATEST(2025 - NVL(P_ANIO, 2025), 1);
        BEGIN
            SELECT NVL(S.POBLACION, R.POBLACION_2025) / R.POBLACION_2025
              INTO V_FACTOR FROM PV_SERIE S
             WHERE S.COD_INE = R.COD_INE AND S.ANIO = P_ANIO;
        EXCEPTION WHEN NO_DATA_FOUND THEN V_FACTOR := 1;
        END;
        V_FACTOR := GREATEST(V_FACTOR, 0.01);
        V_CREC := R.CREC_10Y_BASE;   -- estado (real) del año elegido
    ELSE
        V_HORIZON := LEAST(P_ANIO - 2025, 10);
        SELECT EXP(PREDICTION(M3_DEMOGRAFIA USING
                     R.LOG_POB   AS LOG_POB,
                     R.CAGR_1    AS CAGR_1,
                     R.CAGR_3    AS CAGR_3,
                     R.CAGR_5    AS CAGR_5,
                     R.CAGR_10   AS CAGR_10,
                     R.VOL_5     AS VOL_5,
                     R.EDAD_MEDIA AS EDAD_MEDIA,
                     R.PCT_MENOR_15 AS PCT_MENOR_15,
                     R.PCT_65MAS AS PCT_65MAS,
                     R.REEMPLAZAMIENTO AS REEMPLAZAMIENTO,
                     R.PARO_100  AS PARO_100,
                     R.VAR_PARO  AS VAR_PARO,
                     R.MIGRACION_3Y AS MIGRACION_3Y,
                     R.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM,
                     R.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN,
                     V_HORIZON   AS HORIZONTE))
          INTO V_FACTOR FROM DUAL;
    END IF;

    V_POB25    := R.POBLACION_2025;
    V_POB_BASE := V_POB25 * V_FACTOR;
    IF NVL(P_ANIO, 2025) > 2025 THEN
        V_CREC := POWER(V_POB_BASE / V_POB25, 1 / V_HORIZON) - 1;
    END IF;

    -- banda M3 (mediana |err| % del backtest por horizonte)
    V_ERR_PCT := CASE
                     WHEN V_HORIZON <= 1 THEN 0.93
                     WHEN V_HORIZON <= 2 THEN 1.34
                     WHEN V_HORIZON <= 3 THEN 1.34
                     WHEN V_HORIZON <= 4 THEN 1.62
                     ELSE 2.20
                 END;

    -- ── 2 · estado simulado = base(año) + choque del usuario ──
    V_P10     := V_POB_BASE * (1 - V_ERR_PCT / 100);
    V_P90     := V_POB_BASE * (1 + V_ERR_PCT / 100);
    V_POB_SIM := V_POB_BASE + NVL(P_ADD_POP, 0);
    V_LOG_POB := LN(GREATEST(V_POB_SIM, 0.5));
    V_SALUD_10K := (R.CENTROS_SALUD_NUM + NVL(P_ADD_SALUD, 0)) / V_POB_SIM * 10000;
    V_ESC_1000  := (R.ESCUELAS + NVL(P_ADD_ESC, 0)) / V_POB_SIM * 1000;
    V_PAR_1000  := (R.PARADAS_BASE + NVL(P_ADD_PARADAS, 0)) / V_POB_SIM * 1000;
    V_VIV_1000  := (R.VIV_STOCK + NVL(P_ADD_VIV, 0)) / V_POB_SIM * 1000;

    -- ── 3 · M4: las cinco dimensiones del estado simulado ──
    SELECT PREDICTION(M4_CAPACIDAD_DEM USING
                V_LOG_POB AS LOG_POB,
                V_SALUD_10K AS SALUD_10K,
                V_ESC_1000 AS ESCUELAS_1000,
                V_PAR_1000 AS PARADAS_1000,
                R.TELEFONO AS TELEFONO_1000,
                V_VIV_1000 AS VIV_1000,
                V_CREC AS CREC_10Y_PCT,
                R.PCT_MENOR_15 AS PCT_MENOR_15,
                R.PCT_65MAS AS PCT_65MAS,
                R.REEMPLAZAMIENTO AS REEMPLAZAMIENTO,
                R.PARO_100 AS PARO_100,
                R.VAR_PARO AS VAR_PARO,
                R.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN,
                R.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM)
      INTO V_DIM_DEM FROM DUAL;

    SELECT PREDICTION(M4_CAPACIDAD_VIV USING
                V_LOG_POB AS LOG_POB,
                V_SALUD_10K AS SALUD_10K,
                V_ESC_1000 AS ESCUELAS_1000,
                V_PAR_1000 AS PARADAS_1000,
                R.TELEFONO AS TELEFONO_1000,
                V_VIV_1000 AS VIV_1000,
                V_CREC AS CREC_10Y_PCT,
                R.PCT_MENOR_15 AS PCT_MENOR_15,
                R.PCT_65MAS AS PCT_65MAS,
                R.REEMPLAZAMIENTO AS REEMPLAZAMIENTO,
                R.PARO_100 AS PARO_100,
                R.VAR_PARO AS VAR_PARO,
                R.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN,
                R.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM)
      INTO V_DIM_VIV FROM DUAL;

    SELECT PREDICTION(M4_CAPACIDAD_SER USING
                V_LOG_POB AS LOG_POB,
                V_SALUD_10K AS SALUD_10K,
                V_ESC_1000 AS ESCUELAS_1000,
                V_PAR_1000 AS PARADAS_1000,
                R.TELEFONO AS TELEFONO_1000,
                V_VIV_1000 AS VIV_1000,
                V_CREC AS CREC_10Y_PCT,
                R.PCT_MENOR_15 AS PCT_MENOR_15,
                R.PCT_65MAS AS PCT_65MAS,
                R.REEMPLAZAMIENTO AS REEMPLAZAMIENTO,
                R.PARO_100 AS PARO_100,
                R.VAR_PARO AS VAR_PARO,
                R.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN,
                R.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM)
      INTO V_DIM_SER FROM DUAL;

    SELECT PREDICTION(M4_CAPACIDAD_ACC USING
                V_LOG_POB AS LOG_POB,
                V_SALUD_10K AS SALUD_10K,
                V_ESC_1000 AS ESCUELAS_1000,
                V_PAR_1000 AS PARADAS_1000,
                R.TELEFONO AS TELEFONO_1000,
                V_VIV_1000 AS VIV_1000,
                V_CREC AS CREC_10Y_PCT,
                R.PCT_MENOR_15 AS PCT_MENOR_15,
                R.PCT_65MAS AS PCT_65MAS,
                R.REEMPLAZAMIENTO AS REEMPLAZAMIENTO,
                R.PARO_100 AS PARO_100,
                R.VAR_PARO AS VAR_PARO,
                R.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN,
                R.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM)
      INTO V_DIM_ACC FROM DUAL;

    SELECT PREDICTION(M4_CAPACIDAD_EMP USING
                V_LOG_POB AS LOG_POB,
                V_SALUD_10K AS SALUD_10K,
                V_ESC_1000 AS ESCUELAS_1000,
                V_PAR_1000 AS PARADAS_1000,
                R.TELEFONO AS TELEFONO_1000,
                V_VIV_1000 AS VIV_1000,
                V_CREC AS CREC_10Y_PCT,
                R.PCT_MENOR_15 AS PCT_MENOR_15,
                R.PCT_65MAS AS PCT_65MAS,
                R.REEMPLAZAMIENTO AS REEMPLAZAMIENTO,
                R.PARO_100 AS PARO_100,
                R.VAR_PARO AS VAR_PARO,
                R.TIEMPO_CENTRO AS TIEMPO_CENTRO_MIN,
                R.DISTANCIA_SOL_KM AS DISTANCIA_SOL_KM)
      INTO V_DIM_EMP FROM DUAL;

    -- ── 4 · JSON de salida (mismo esquema que consume la página + bloques nuevos) ──
    SELECT JSON_OBJECT(
        'cod' VALUE R.COD_INE,
        'anio_simulado' VALUE NVL(P_ANIO, 2025),
        'factor_m3' VALUE ROUND(V_FACTOR, 5),
        'poblacion_base_2025' VALUE ROUND(V_POB25, 0),
        'poblacion_base_anio' VALUE ROUND(V_POB_BASE, 0),
        'poblacion_anio_p10' VALUE ROUND(V_P10, 0),
        'poblacion_anio_p90' VALUE ROUND(V_P90, 0),
        'poblacion_antes' VALUE ROUND(B_POB, 0),
        'poblacion_despues' VALUE ROUND(V_POB_SIM, 0),
        'viviendas_antes' VALUE ROUND(B_VIV, 0),
        'viviendas_despues' VALUE ROUND(R.VIV_STOCK + NVL(P_ADD_VIV, 0), 0),
        'centros_salud_antes' VALUE ROUND(B_SALUD, 0),
        'centros_salud_despues' VALUE ROUND(R.CENTROS_SALUD_NUM + NVL(P_ADD_SALUD, 0), 0),
        'escuelas_antes' VALUE ROUND(B_ESC, 0),
        'escuelas_despues' VALUE ROUND(R.ESCUELAS + NVL(P_ADD_ESC, 0), 0),
        'paradas_antes' VALUE ROUND(B_PAR, 0),
        'paradas_despues' VALUE ROUND(R.PARADAS_BASE + NVL(P_ADD_PARADAS, 0), 0),
        'salud_10k_antes' VALUE ROUND(BS_10K, 2),
        'salud_10k_despues' VALUE ROUND(V_SALUD_10K, 2),
        'escuelas_1000_antes' VALUE ROUND(BS_E1000, 3),
        'escuelas_1000_despues' VALUE ROUND(V_ESC_1000, 3),
        'paradas_1000_antes' VALUE ROUND(BS_P1000, 3),
        'paradas_1000_despues' VALUE ROUND(V_PAR_1000, 3),
        'viv_1000_antes' VALUE ROUND(BS_V1000, 1),
        'viv_1000_despues' VALUE ROUND(V_VIV_1000, 1),
        'dim_dem_antes' VALUE ROUND(BD_DEM, 1),
        'dim_dem_despues' VALUE ROUND(V_DIM_DEM, 1),
        'dim_viv_antes' VALUE ROUND(BD_VIV, 1),
        'dim_viv_despues' VALUE ROUND(V_DIM_VIV, 1),
        'dim_ser_antes' VALUE ROUND(BD_SER, 1),
        'dim_ser_despues' VALUE ROUND(V_DIM_SER, 1),
        'dim_acc_antes' VALUE ROUND(BD_ACC, 1),
        'dim_acc_despues' VALUE ROUND(V_DIM_ACC, 1),
        'dim_emp_antes' VALUE ROUND(BD_EMP, 1),
        'dim_emp_despues' VALUE ROUND(V_DIM_EMP, 1),
        'indice_antes' VALUE ROUND(B_INDICE, 1),
        'indice_despues' VALUE ROUND(
            V_DIM_DEM * 0.20 + V_DIM_VIV * 0.15 + V_DIM_SER * 0.25 +
            V_DIM_ACC * 0.25 + V_DIM_EMP * 0.15, 1),
        'delta_indice' VALUE ROUND(
            (V_DIM_DEM * 0.20 + V_DIM_VIV * 0.15 + V_DIM_SER * 0.25 +
             V_DIM_ACC * 0.25 + V_DIM_EMP * 0.15) - B_INDICE, 1),
        'factor_limitante' VALUE CASE
            WHEN LEAST(V_DIM_DEM, V_DIM_VIV, V_DIM_SER, V_DIM_ACC, V_DIM_EMP) = V_DIM_DEM THEN 'Demografía'
            WHEN LEAST(V_DIM_DEM, V_DIM_VIV, V_DIM_SER, V_DIM_ACC, V_DIM_EMP) = V_DIM_VIV THEN 'Vivienda'
            WHEN LEAST(V_DIM_DEM, V_DIM_VIV, V_DIM_SER, V_DIM_ACC, V_DIM_EMP) = V_DIM_SER THEN 'Servicios'
            WHEN LEAST(V_DIM_DEM, V_DIM_VIV, V_DIM_SER, V_DIM_ACC, V_DIM_EMP) = V_DIM_ACC THEN 'Accesibilidad'
            ELSE 'Empleo'
        END
        RETURNING CLOB) INTO V_JSON FROM DUAL;
    RETURN V_JSON;
END;
/

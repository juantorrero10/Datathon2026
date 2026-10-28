/* LoDCORE · Mapa de municipios (mapa.js) — lógica. Requiere Leaflet 1.9.4 cargado antes. Endpoint: CONFIG.apiUrl */
(function () {
  'use strict';

  // ===================== CONFIGURACIÓN =====================
  var CONFIG = {
    // Endpoint ORDS. Si el HTML se sirve desde el mismo host que ORDS puedes usar la ruta relativa:
    // '/ords/datathon/lodcore/municipios'
    apiUrl: 'https://g0c7419060d3399-n590x9g2v58k2mzg.adb.eu-madrid-1.oraclecloudapps.com/ords/datathon/lodcore/municipios',
    centro: [40.50, -3.70],
    zoom: 9
  };

  var LIMITE_MADRID = {"type":"Feature","geometry":{"type":"MultiPolygon","coordinates":[[[[-3.536705,41.160576],[-3.488751,41.094294],[-3.425805,41.082899],[-3.438935,41.04267],[-3.39445,41.000278],[-3.418296,40.987564],[-3.444062,40.906849],[-3.460577,40.906659],[-3.440487,40.87535],[-3.47257,40.864217],[-3.477387,40.823561],[-3.511572,40.788496],[-3.45901,40.781324],[-3.444343,40.76158],[-3.450416,40.734887],[-3.434945,40.727986],[-3.468553,40.689937],[-3.404735,40.669637],[-3.393354,40.692458],[-3.345598,40.637743],[-3.316497,40.655177],[-3.338516,40.625849],[-3.321644,40.612192],[-3.328275,40.594836],[-3.284069,40.568977],[-3.297126,40.537521],[-3.249915,40.544316],[-3.199955,40.514449],[-3.198597,40.442252],[-3.155515,40.439425],[-3.130558,40.405185],[-3.15343,40.367703],[-3.141212,40.350542],[-3.182857,40.308267],[-3.194449,40.248037],[-3.173397,40.23417],[-3.153718,40.263714],[-3.112674,40.285478],[-3.101528,40.278092],[-3.067845,40.157914],[-3.089276,40.16297],[-3.096755,40.142389],[-3.056194,40.113743],[-3.060707,40.090564],[-3.11819,40.061429],[-3.161579,40.064928],[-3.178137,40.092207],[-3.200956,40.060488],[-3.275756,40.047276],[-3.332241,40.080482],[-3.37529,40.075393],[-3.375783,40.051255],[-3.401072,40.034181],[-3.506863,40.048674],[-3.519689,40.021072],[-3.589995,40.013172],[-3.637944,39.988352],[-3.634499,39.965892],[-3.74387,39.940802],[-3.804398,39.88472],[-3.868326,39.904859],[-3.87519,39.928736],[-3.840044,39.941956],[-3.832042,39.93156],[-3.809548,39.953965],[-3.783347,39.944796],[-3.763602,39.967518],[-3.770486,39.950552],[-3.75437,39.950443],[-3.758817,39.968885],[-3.727936,39.964545],[-3.746207,39.981089],[-3.720088,39.984441],[-3.699891,40.019543],[-3.636088,40.041626],[-3.607628,40.108967],[-3.655732,40.124912],[-3.667313,40.143291],[-3.683724,40.13227],[-3.722216,40.147713],[-3.744375,40.132224],[-3.770453,40.139399],[-3.804603,40.176841],[-3.834186,40.161353],[-3.872016,40.190153],[-3.931143,40.203977],[-3.950892,40.190335],[-3.952866,40.212797],[-3.991002,40.209478],[-4.026159,40.235611],[-4.024028,40.248968],[-4.072894,40.265451],[-4.104272,40.241833],[-4.145769,40.245177],[-4.143992,40.264621],[-4.190871,40.297355],[-4.20323,40.268818],[-4.247999,40.273481],[-4.269961,40.235685],[-4.306111,40.221778],[-4.307989,40.233882],[-4.348488,40.236747],[-4.356386,40.308621],[-4.38011,40.318341],[-4.383482,40.289049],[-4.435246,40.259127],[-4.437426,40.236698],[-4.509789,40.21919],[-4.527911,40.200093],[-4.574993,40.206642],[-4.559329,40.231269],[-4.568788,40.258712],[-4.529379,40.293125],[-4.546225,40.341825],[-4.526788,40.344873],[-4.502898,40.314893],[-4.455762,40.319351],[-4.460596,40.341381],[-4.438636,40.352754],[-4.443729,40.3857],[-4.42173,40.406229],[-4.321089,40.410309],[-4.341252,40.428678],[-4.315679,40.464766],[-4.328218,40.533757],[-4.289262,40.564194],[-4.278572,40.603172],[-4.290709,40.627823],[-4.271102,40.629023],[-4.262141,40.60518],[-4.245439,40.602447],[-4.161183,40.623465],[-4.172853,40.630362],[-4.171567,40.680626],[-4.096991,40.747739],[-4.0767,40.788881],[-3.979676,40.784555],[-3.947105,40.862974],[-3.952276,40.893632],[-3.907197,40.955303],[-3.781366,41.000312],[-3.740455,41.05364],[-3.676065,41.086696],[-3.613703,41.149053],[-3.536705,41.160576]],[[-3.372259,40.635612],[-3.380257,40.632854],[-3.382135,40.630471],[-3.363665,40.631602],[-3.372259,40.635612]]],[[[-4.255731,40.65317],[-4.31951,40.647644],[-4.324122,40.658029],[-4.284817,40.681221],[-4.255731,40.65317]]]]},"properties":{"cod_ccaa":"13","noml_ccaa":"COMUNIDAD DE MADRID","name":"Madrid","cartodb_id":13,"created_at":"2014-09-30T00:00:00Z","updated_at":"2014-12-25T02:07:41Z"}};

  // ===================== UTILIDADES =====================
  var $ = function (id) { return document.getElementById(id); };

  function esc(s) {
    return String(s === null || s === undefined ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  // Red de seguridad: si la BD guarda "ChinchÃ³n" (UTF-8 leído como Latin-1) lo devuelve a "Chinchón".
  // Si el texto ya está bien, no hace nada.
  function reparar(s) {
    if (typeof s !== 'string' || !/[\u00C2\u00C3]/.test(s)) return s;
    try { return decodeURIComponent(escape(s)); } catch (e) { return s; }
  }

  function num(v) {
    if (v === null || v === undefined || v === '') return null;
    var n = Number(v);
    return isFinite(n) ? n : null;
  }

  function fmt(v, dec) {
    if (v === null || v === undefined) return '—';
    dec = dec || 0;
    return v.toLocaleString('es-ES', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  }

  function cap(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1).toLowerCase() : s; }
  function plano(s) { return String(s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); }
  function clamp100(v) { return v === null ? 0 : Math.max(0, Math.min(100, v)); }

  // ===================== MODELO =====================
  var M = [];
  var cur = 'ica';
  var sel = null;       // id del municipio seleccionado
  var pinned = null;    // id con la tarjeta fijada (clic)
  var map = null, capaMarcadores = null, capaTile = null;

  var GRIS = '#A0AEC0';
  var COLOR_NIVEL = { Alta: '#1B7A3C', Media: '#B7791F', Baja: '#C8102E' };
  var CLASE_NIVEL = { Alta: 'green', Media: 'amber', Baja: 'red' };
  var BD_NIVEL = { Alta: 'proy', Media: 'est', Baja: 'sim' };
  var COLOR_LIMIT = { 'Sanidad': '#0078A8', 'Educación': '#B7791F', 'Vivienda': '#4A5568' };
  var ALERTAS = {
    ESTABLE: ['Estable', 'green'],
    ATENCION_MEDIA: ['Atención media', 'amber'],
    URGENTE_REFUERZO: ['Refuerzo urgente', 'red']
  };

  var CAPAS = [
    { k: 'ica',     label: 'Índice ICA Global (Semáforo)', bd: ['est', 'Est.'],  unit: '/100',   dec: 1 },
    { k: 'colapso', label: 'Capacidad Neta sin Colapso',   bd: ['proy', 'Proy.'], unit: ' hab.',  dec: 0 },
    { k: 'limit',   label: 'Cuello de Botella Dominante',  bd: ['obs', 'Obs.'],  unit: '',       dec: 0 },
    { k: 'prc',     label: 'Precio Vivienda (€/m²)',       bd: ['est', 'Est.'],  unit: ' €/m²',  dec: 0 },
    { k: 'trans',   label: 'Transporte & Conectividad',    bd: ['obs', 'Obs.'],  unit: '/100',   dec: 1 },
    { k: 'serv',    label: 'Dotación de Servicios',        bd: ['obs', 'Obs.'],  unit: '/100',   dec: 1 },
    { k: 'pop',     label: 'Población Padrón 2025',        bd: ['obs', 'Obs.'],  unit: ' mil',   dec: 1 }
  ];
  function capaDef(k) { for (var i = 0; i < CAPAS.length; i++) if (CAPAS[i].k === k) return CAPAS[i]; return CAPAS[0]; }

  // Un registro del endpoint -> objeto interno
  function normalizar(it) {
    var lat = num(it.latitud), lon = num(it.longitud);
    var pobl = num(it.poblacion_actual);
    var nombre = reparar(it.nombre) || '(sin nombre)';
    return {
      id: String(it.id_municipio !== undefined && it.id_municipio !== null ? it.id_municipio : it.codigo_ine),
      ine: it.codigo_ine,
      n: nombre,
      nq: plano(nombre),
      com: reparar(it.comarca) || '—',
      tip: cap(reparar(it.tipologia)) || '—',
      lat: lat, lon: lon,
      pobl: pobl,
      pop: pobl === null ? null : pobl / 1000,          // en miles, como el prototipo
      prc: num(it.precio_m2_compra),
      trans: num(it.score_conectividad),
      serv: num(it.score_servicios),
      ica: num(it.indice_capacidad_global),
      nivel: cap(it.nivel_idoneidad) || null,
      colapso: num(it.personas_absorbibles_sin_colapso),
      limit: reparar(it.factor_limitante) || null,
      limit_det: reparar(it.detalle_limitante) || '',
      tiempo: num(it.tiempo_medio_madrid_minutos),
      hmed: num(it.hab_por_medico),
      esc_oc: num(it.ocupacion_escolar_pct),
      fib: num(it.cobertura_fibra_pct),
      patr: reparar(it.patrimonio_entorno) || '',
      alerta: it.alerta_planificacion || null,
      origen: it.origen || '', metodo: it.metodo || '', version: it.dataset_version || '', fuente: it.fuente_datos || ''
    };
  }

  function rango(k) {
    var lo = Infinity, hi = -Infinity;
    M.forEach(function (m) { var v = m[k]; if (v !== null && v !== undefined) { if (v < lo) lo = v; if (v > hi) hi = v; } });
    return lo === Infinity ? [0, 1] : [lo, hi];
  }

  function colorICA(m) {
    if (COLOR_NIVEL[m.nivel]) return COLOR_NIVEL[m.nivel];      // el nivel publicado manda sobre el redondeo
    if (m.ica === null) return GRIS;
    return m.ica >= 60 ? COLOR_NIVEL.Alta : m.ica >= 40 ? COLOR_NIVEL.Media : COLOR_NIVEL.Baja;
  }

  function getColor(m, k) {
    if (k === 'limit') return COLOR_LIMIT[m.limit] || GRIS;
    if (k === 'ica') return colorICA(m);
    if (m[k] === null || m[k] === undefined) return GRIS;
    var r = rango(k), lo = r[0], hi = r[1];
    var t = Math.max(0, Math.min(1, (m[k] - lo) / ((hi - lo) || 1)));
    return 'rgb(' + Math.round(214 - t * 214) + ',' + Math.round(232 - t * 146) + ',' + Math.round(243 - t * 121) + ')';
  }

  // ===================== FILTROS =====================
  function getFilters() {
    return {
      q: plano($('lc-q').value).trim(),
      com: $('lc-comarca').value,
      pop: +$('lc-pop').value,
      pr: +$('lc-pr').value,
      tr: +$('lc-tr').value,
      limit: $('lc-limit').value
    };
  }

  function passFilter(m, F) {
    if (F.q && m.nq.indexOf(F.q) === -1) return false;
    if (F.com !== 'all' && m.com !== F.com) return false;
    if (m.pop !== null && m.pop > F.pop) return false;
    if (m.prc !== null && m.prc > F.pr) return false;
    if (m.trans !== null && m.trans < F.tr) return false;
    if (F.limit !== 'all' && m.limit !== F.limit) return false;
    return true;
  }

  function porId(id) { for (var i = 0; i < M.length; i++) if (M[i].id === id) return M[i]; return null; }

  // ===================== MAPA =====================
  var TILES = {
    ign: {
      url: 'https://www.ign.es/wmts/ign-base?service=WMTS&request=GetTile&version=1.0.0&Format=image/png&layer=IGNBaseTodo&style=default&tilematrixset=GoogleMapsCompatible&TileMatrix={z}&TileRow={y}&TileCol={x}',
      opt: { maxZoom: 18, attribution: '&copy; <a href="https://www.ign.es/" target="_blank" rel="noopener">IGN España / CNIG</a>' }
    },
    street: {
      url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
      opt: { maxZoom: 18, attribution: 'Tiles &copy; Esri &mdash; Sources: Esri, DeLorme, HERE, USGS, Intermap, INCREMENT P' }
    },
    sat: {
      url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      opt: { maxZoom: 19, attribution: 'Tiles &copy; Esri, Maxar, Earthstar Geographics' }
    }
  };
  var TILE_INICIAL = 'ign';

  function setTile(tipo) {
    if (!map) return;
    if (capaTile) map.removeLayer(capaTile);
    capaTile = L.tileLayer(TILES[tipo].url, TILES[tipo].opt).addTo(map);
    capaTile.bringToBack();
    Array.prototype.forEach.call(document.querySelectorAll('#lodcore .lc-pill'), function (b) {
      b.classList.toggle('on', b.getAttribute('data-tile') === tipo);
    });
  }

  function dibujarMarcadores() {
    if (!capaMarcadores) return;
    capaMarcadores.clearLayers();
    var F = getFilters();
    M.forEach(function (m) {
      if (m.lat === null || m.lon === null || !passFilter(m, F)) return;
      var radio = 6 + Math.sqrt(m.pop || 0) * 1.3;
      var esSel = m.id === sel;
      var mk = L.circleMarker([m.lat, m.lon], {
        radius: esSel ? radio + 3 : radio,
        fillColor: getColor(m, cur),
        fillOpacity: esSel ? 0.95 : 0.8,
        color: esSel ? '#232323' : '#ffffff',
        weight: esSel ? 3 : 1.5,
        bubblingMouseEvents: false
      });
      mk.on('mouseover', function () {
        mk.setStyle({ weight: 3, color: '#232323' });
        mostrarTarjeta(m, puntoDe(m), m.id === pinned);
      });
      mk.on('mouseout', function () {
        if (m.id !== sel) mk.setStyle({ weight: 1.5, color: '#ffffff' });
        restaurarTarjeta();
      });
      mk.on('click', function () { seleccionar(m.id); });
      capaMarcadores.addLayer(mk);
    });
  }

  // ===================== TARJETA =====================
  function puntoDe(m) {
    var p = map.latLngToContainerPoint([m.lat, m.lon]);
    return { x: p.x, y: p.y, r: 8 };
  }

  var ICO_AVISO = '<span class="fa fa-exclamation-triangle lc-ico" aria-hidden="true"></span>';
  var ICO_CERRAR = '<span class="fa fa-times" aria-hidden="true"></span>';

  function tarjetaHTML(m, fijada) {
    var cc = CLASE_NIVEL[m.nivel] || '';
    var bar = function (l, v, c) {
      return '<div class="lc-m"><span>' + l + '</span><div class="lc-b ' + (c || '') + '"><i style="width:' + clamp100(v) + '%"></i></div><b>' + fmt(v, 1) + '</b></div>';
    };
    var stat = function (l, v) { return '<div class="lc-stat"><div>' + l + '</div><b>' + v + '</b></div>'; };
    var al = ALERTAS[m.alerta];
    var chip = m.alerta ? '<span class="lc-chip ' + (al ? al[1] : 'gray') + '">' + esc(al ? al[0] : cap(String(m.alerta).replace(/_/g, ' '))) + '</span>' : '';
    var proc = [m.origen, m.metodo, m.version, m.fuente].filter(Boolean).map(esc).join(' · ');

    // --- Primer campo: la métrica de la capa seleccionada ---
    var valorBarra = function (etiqueta, v, clase) {
      return '<div class="lc-dest-l">' + etiqueta + '</div>' +
        '<div class="lc-dest-v">' + fmt(v, 1) + '<small>/100</small></div>' +
        '<div class="lc-b ' + (clase || '') + '"><i style="width:' + clamp100(v) + '%"></i></div>';
    };
    var valorGrande = function (etiqueta, valor, sub) {
      return '<div class="lc-dest-l">' + etiqueta + '</div><div class="lc-dest-v">' + valor + '</div>' +
        (sub ? '<div class="lc-dest-s">' + sub + '</div>' : '');
    };
    var cuerpo = '';
    if (cur === 'ica')          cuerpo = valorBarra('Índice ICA', m.ica, cc);
    else if (cur === 'trans')   cuerpo = valorBarra('Transporte y conectividad', m.trans);
    else if (cur === 'serv')    cuerpo = valorBarra('Dotación de servicios', m.serv);
    else if (cur === 'colapso') cuerpo = valorGrande('Capacidad neta sin colapso', fmt(m.colapso) + '<small> hab.</small>');
    else if (cur === 'prc')     cuerpo = valorGrande('Precio de la vivienda', fmt(m.prc) + '<small> €/m²</small>');
    else if (cur === 'pop')     cuerpo = valorGrande('Población (Padrón)', fmt(m.pop, 1) + '<small> mil</small>', fmt(m.pobl) + ' habitantes');
    else if (cur === 'limit')   cuerpo = valorGrande('Cuello de botella dominante', esc(m.limit || '—'), esc(m.limit_det));
    var colorBorde = (cur === 'ica' || cur === 'limit') ? getColor(m, cur) : '';
    var destacado = '<div class="lc-dest"' + (colorBorde ? ' style="border-left-color:' + colorBorde + ';"' : '') + '>' +
      '<div class="lc-dest-t">Capa activa</div>' + cuerpo + '</div>';

    // --- Resto de campos (sin repetir el que ya va arriba) ---
    var barras = [['ica', '<b>Índice ICA</b>', m.ica, cc], ['trans', 'Transporte', m.trans, ''], ['serv', 'Servicios púb.', m.serv, '']]
      .filter(function (x) { return x[0] !== cur; })
      .map(function (x) { return bar(x[1], x[2], x[3]); }).join('');
    var celdas = [
      ['pop', 'Población', fmt(m.pop, 1) + ' mil'],
      ['prc', 'Precio', fmt(m.prc) + ' €/m²'],
      ['colapso', 'Acogida neta', fmt(m.colapso) + ' hab.'],
      ['tiempo', 'A Madrid', fmt(m.tiempo) + ' min'],
      ['hmed', 'Hab/médico', fmt(m.hmed)],
      ['esc_oc', 'Ocup. escolar', fmt(m.esc_oc, 1) + '%'],
      ['fib', 'Fibra', fmt(m.fib, 1) + '%']
    ].filter(function (x) { return x[0] !== cur; })
     .map(function (x) { return stat(x[1], x[2]); }).join('');
    var cuello = cur === 'limit' ? '' :
      '<div style="padding:7px 9px;background:var(--madrid-red-light);border:1px solid var(--madrid-red-border);border-radius:var(--radius-sm);">' +
        '<div style="font-size:11.5px;font-weight:700;color:var(--madrid-red-dark);">' + ICO_AVISO + 'Cuello de botella: ' + esc(m.limit || '—') + '</div>' +
        (m.limit_det ? '<div style="font-size:11px;color:var(--text-secondary);margin-top:2px;">' + esc(m.limit_det) + '</div>' : '') +
      '</div>';

    return '' +
      '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;">' +
        '<div><b style="font-size:16px;">' + esc(m.n) + '</b>' +
        '<div style="color:var(--mu);font-size:11.5px;margin:2px 0 6px;">' + esc(m.com) + ' · ' + esc(m.tip) + '</div></div>' +
        '<div style="display:flex;align-items:center;gap:6px;">' +
          (m.nivel ? '<span class="lc-bd ' + (BD_NIVEL[m.nivel] || '') + '">' + esc(m.nivel) + '</span>' : '') +
          (fijada ? '<button type="button" class="lc-btn lc-o" id="lc-hc-close" style="padding:2px 8px;font-size:11.5px;" aria-label="Cerrar">' + ICO_CERRAR + '</button>' : '') +
        '</div>' +
      '</div>' +
      destacado +
      barras +
      '<div class="lc-stats">' + celdas + '</div>' +
      cuello +
      (chip ? '<div style="margin-top:8px;font-size:11.5px;">Planificación: ' + chip + '</div>' : '') +
      (m.patr ? '<div class="lc-patr' + (fijada ? '' : ' lc-clamp') + '"><b>Patrimonio y entorno:</b> ' + esc(m.patr) + '</div>' : '') +
      (proc ? '<div class="lc-proc">Procedencia: ' + proc + '</div>' : '') +
      (fijada ? '' : '<div style="margin-top:8px;font-size:10.5px;color:var(--mu);">Haz clic para fijar la tarjeta</div>');
  }

  function mostrarTarjeta(m, pt, fijada) {
    var card = $('lc-hover');
    if (!pt) { card.style.display = 'none'; return; }
    card.innerHTML = tarjetaHTML(m, fijada);
    card.style.pointerEvents = fijada ? 'auto' : 'none';
    card.style.visibility = 'hidden';
    card.style.display = 'block';

    var stage = $('lc-stage');
    var W = stage.clientWidth, H = stage.clientHeight;
    var cw = card.offsetWidth, ch = card.offsetHeight, gap = pt.r + 12;
    var left = pt.x + gap;
    if (left + cw > W - 8) left = pt.x - gap - cw;
    left = Math.max(8, left);
    var top = Math.max(8, Math.min(H - ch - 8, pt.y - 40));
    card.style.left = left + 'px';
    card.style.top = top + 'px';
    card.style.visibility = 'visible';

    if (fijada) {
      var x = $('lc-hc-close');
      if (x) x.onclick = function () { pinned = null; restaurarTarjeta(); };
    }
  }

  function restaurarTarjeta() {
    var card = $('lc-hover');
    var m = pinned ? porId(pinned) : null;
    if (!m || m.lat === null || !passFilter(m, getFilters())) { card.style.display = 'none'; return; }
    var pt = puntoDe(m), stage = $('lc-stage');
    if (pt.x < 0 || pt.y < 0 || pt.x > stage.clientWidth || pt.y > stage.clientHeight) { card.style.display = 'none'; return; }
    mostrarTarjeta(m, pt, true);
  }

  function seleccionar(id) {
    var m = porId(id);
    if (!m) return;
    sel = id; pinned = id;
    if (map && m.lat !== null) map.flyTo([m.lat, m.lon], Math.max(map.getZoom(), 11), { duration: 0.8 });
    refrescar();
    // Para enlazar con Acciones Dinámicas de APEX u otros componentes de la página
    try {
      document.dispatchEvent(new CustomEvent('lodcore:municipio', { detail: { id_municipio: m.id, codigo_ine: m.ine, nombre: m.n } }));
    } catch (e) { /* sin soporte de CustomEvent */ }
  }

  // ===================== TOP 5, LEYENDA, ESTADO =====================
  function dibujarTop5() {
    var F = getFilters();
    var clave = cur === 'limit' ? 'ica' : cur;
    var def = capaDef(clave);
    var lista = M.filter(function (m) { return passFilter(m, F) && m[clave] !== null; })
      .sort(function (a, b) { return b[clave] - a[clave]; }).slice(0, 5);
    $('lc-top-sub').textContent = cur === 'limit' ? 'Índice ICA Global' : def.label;
    $('lc-top').innerHTML = lista.map(function (m, i) {
      return '<li data-id="' + esc(m.id) + '"><span><b>' + (i + 1) + '.</b> ' + esc(m.n) + '</span><b>' + fmt(m[clave], def.dec) + esc(def.unit) + '</b></li>';
    }).join('') || '<li class="lc-vacio">Sin resultados con estos filtros</li>';
    Array.prototype.forEach.call($('lc-top').querySelectorAll('li[data-id]'), function (li) {
      li.onclick = function () { seleccionar(li.getAttribute('data-id')); };
    });
  }

  function dibujarLeyenda() {
    Array.prototype.forEach.call(document.querySelectorAll('#lodcore input[name=lc-capa]'), function (r) { r.checked = (r.value === cur); });
    var el = $('lc-leyenda');
    var def = capaDef(cur);
    var titulo = '<div class="lc-leg-t">Escala: ' + esc(def.label) + '</div>';
    var barra = 'height:10px;border-radius:5px;margin:8px 0 3px;';
    var etiq = 'display:flex;justify-content:space-between;font-size:11.5px;color:var(--mu);';

    if (cur === 'limit') {
      el.innerHTML = titulo + '<div style="display:flex;flex-direction:column;gap:5px;margin-top:8px;font-size:12px;">' +
        Object.keys(COLOR_LIMIT).map(function (l) {
          return '<div style="display:flex;align-items:center;gap:8px;"><span style="width:14px;height:14px;border-radius:50%;background:' + COLOR_LIMIT[l] + ';display:inline-block;"></span>' + l + '</div>';
        }).join('') + '</div>';
      return;
    }
    if (cur === 'ica') {
      el.innerHTML = titulo +
        '<div style="' + barra + 'background:linear-gradient(90deg,#C8102E 0 40%,#B7791F 40% 60%,#1B7A3C 60% 100%);"></div>' +
        '<div style="' + etiq + '"><span>Baja (&lt;40)</span><span>Media (40–59)</span><span>Alta (≥60)</span></div>';
      return;
    }
    var r = rango(cur);
    el.innerHTML = titulo +
      '<div style="' + barra + 'background:linear-gradient(90deg,' + getColor({ [cur]: r[0] }, cur) + ',' + getColor({ [cur]: r[1] }, cur) + ');"></div>' +
      '<div style="' + etiq + '"><span>' + fmt(r[0], def.dec) + esc(def.unit) + '</span><span>' + fmt(r[1], def.dec) + esc(def.unit) + '</span></div>';
  }

  function dibujarEstado() {
    var F = getFilters();
    var visibles = M.filter(function (m) { return m.lat !== null && passFilter(m, F); }).length;
    var procs = [];
    M.forEach(function (m) {
      var p = [m.origen, m.metodo, m.version, m.fuente].filter(Boolean).join(' · ');
      if (p && procs.indexOf(p) === -1) procs.push(p);
    });
    $('lc-estado').innerHTML = 'Mostrando <b>' + visibles + '</b> de <b>' + M.length + '</b> municipios' +
      (procs.length ? '<br>Procedencia: ' + procs.map(esc).join('; ') : '');
  }

  function refrescar() {
    dibujarMarcadores();
    dibujarTop5();
    dibujarLeyenda();
    dibujarEstado();
    restaurarTarjeta();
  }

  // ===================== AVISOS =====================
  function aviso(html, esError) {
    var a = $('lc-aviso');
    if (!html) { a.hidden = true; return; }
    a.className = 'lc-aviso' + (esError ? ' lc-err' : '');
    a.innerHTML = html;
    a.hidden = false;
  }

  // ===================== DATOS (REST) =====================
  function cargarTodos(url) {
    var items = [];
    function pedir(u, intentos) {
      return fetch(u, { headers: { 'Accept': 'application/json' }, credentials: 'same-origin' })
        .then(function (r) {
          if (!r.ok) throw new Error('El endpoint respondió HTTP ' + r.status);
          return r.json();
        })
        .then(function (d) {
          items = items.concat(d.items || []);
          var sig = null;
          if (d.hasMore) (d.links || []).forEach(function (l) { if (l.rel === 'next') sig = l.href; });
          return (sig && intentos < 20) ? pedir(sig, intentos + 1) : items;
        });
    }
    return pedir(url, 0);
  }

  function rellenarComarcas() {
    var sel = $('lc-comarca'), previa = sel.value;
    var coms = [];
    M.forEach(function (m) { if (m.com !== '—' && coms.indexOf(m.com) === -1) coms.push(m.com); });
    coms.sort(function (a, b) { return a.localeCompare(b, 'es'); });
    sel.innerHTML = '<option value="all">Todas las comarcas</option>' +
      coms.map(function (c) { return '<option value="' + esc(c) + '">' + esc(c) + '</option>'; }).join('');
    sel.value = coms.indexOf(previa) !== -1 ? previa : 'all';
  }

  function recargar() {
    aviso('Cargando municipios…', false);
    return cargarTodos(CONFIG.apiUrl).then(function (items) {
      M = items.map(normalizar);
      var sinCoord = M.filter(function (m) { return m.lat === null || m.lon === null; }).length;
      if (sinCoord) console.warn('LoDCORE mapa: ' + sinCoord + ' municipios sin coordenadas (no se dibujan)');
      rellenarComarcas();
      refrescar();
      if (!M.length) aviso('El endpoint no devolvió municipios.', true);
      else aviso(null);
    }).catch(function (e) {
      console.error('LoDCORE mapa:', e);
      aviso('No se pudieron cargar los municipios.<small>' + esc(e && e.message ? e.message : e) +
        '<br>Comprueba la URL del endpoint, que el módulo esté publicado y, si el HTML está en otro dominio, el CORS (Origins Allowed).</small>' +
        '<button type="button" class="lc-btn" id="lc-reintentar">Reintentar</button>', true);
      var b = $('lc-reintentar');
      if (b) b.onclick = recargar;
    });
  }

  // ===================== ARRANQUE =====================
  function iniciar() {
    if (typeof L === 'undefined') {
      aviso('No se pudo cargar el mapa (Leaflet).<small>Puede estar bloqueado por la política de seguridad de contenido (CSP) de la aplicación: permite unpkg.com y los servidores de teselas.</small>', true);
      return;
    }

    // Selector de capas
    $('lc-capas').innerHTML = CAPAS.map(function (c) {
      return '<label><input type="radio" name="lc-capa" value="' + c.k + '"' + (c.k === cur ? ' checked' : '') + '> ' +
        (c.k === 'ica' ? '<b>' + esc(c.label) + '</b>' : esc(c.label)) + ' <span class="lc-bd ' + c.bd[0] + '">' + c.bd[1] + '</span></label>';
    }).join('');

    map = L.map('lc-map', { center: CONFIG.centro, zoom: CONFIG.zoom, minZoom: 8, maxZoom: 14, zoomControl: false });
    L.control.zoom({ position: 'bottomright' }).addTo(map);
    map.on('click', function () { pinned = null; restaurarTarjeta(); });
    map.on('move', restaurarTarjeta);

    setTile(TILE_INICIAL);
    L.geoJSON(LIMITE_MADRID, {
      style: { color: '#0078A8', weight: 2.2, dashArray: '3, 4', fillColor: '#0078A8', fillOpacity: 0.04 },
      interactive: false
    }).addTo(map);
    capaMarcadores = L.layerGroup().addTo(map);

    // Eventos de la interfaz
    Array.prototype.forEach.call(document.querySelectorAll('#lodcore .lc-pill'), function (b) {
      b.onclick = function () { setTile(b.getAttribute('data-tile')); };
    });
    ['lc-q', 'lc-comarca', 'lc-limit'].forEach(function (id) { $(id).oninput = refrescar; });
    ['lc-pop', 'lc-pr', 'lc-tr'].forEach(function (id) {
      $(id).oninput = function () {
        $('lc-pv').textContent = $('lc-pop').value;
        $('lc-prv').textContent = $('lc-pr').value;
        $('lc-tv').textContent = $('lc-tr').value;
        refrescar();
      };
    });
    $('lc-rst').onclick = function () {
      $('lc-q').value = ''; $('lc-comarca').value = 'all'; $('lc-limit').value = 'all';
      $('lc-pop').value = 50; $('lc-pv').textContent = 50;
      $('lc-pr').value = 3500; $('lc-prv').textContent = 3500;
      $('lc-tr').value = 0; $('lc-tv').textContent = 0;
      refrescar();
    };
    Array.prototype.forEach.call(document.querySelectorAll('#lodcore input[name=lc-capa]'), function (r) {
      r.onchange = function () { cur = r.value; refrescar(); };
    });

    // El contenedor puede estar oculto al cargar (pestañas, acordeones de APEX)
    window.addEventListener('resize', function () { map.invalidateSize(); });
    setTimeout(function () { map.invalidateSize(); }, 250);

    window.LODCORE_MAPA = { map: map, recargar: recargar, seleccionar: seleccionar };
    recargar();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();

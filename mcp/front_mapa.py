"""Front de la página 40 — Mapa interactivo (diferenciales por año objetivo).

CABECERA_MAPA -> primer HTP.P (estilos .t-Header, igual que el Simulador)
FRONT_MAPA    -> segundo HTP.P (CSS + HTML + JS; Leaflet vía CDN)

Fuente de datos (procesos AJAX de la propia página 40):
  PRED -> WKSP_DATATHON.PV_MAPA(año)   (métricas de 155 municipios)
  GEO  -> FeatureCollection de PV_GEO_MUNIS (polígonos OSM simplificados)
Sin datos hardcodeados: todo lo visible proviene del modelo o de las tablas
(los widgets de filtros están presentes pero inertes, sin valores ejemplo).

Estructura del JS:
  - Listeners básicos (slider, Enter, botón) registrados al cargar la página,
    SIN depender de Leaflet (funcionan aunque el CDN tarde).
  - boot() (espera window.L + window.apex): crea mapa, tiles, contorno,
    carga GEO, registra listeners de capas → READY=true.
  - run() (botón/Enter): PRED → render.
"""

from pathlib import Path

CABECERA_MAPA = (
    "<style>\n"
    ".t-Header,.t-Header .t-Header-branding,.t-Header .t-Header-navBar{background:#0f766e!important}\n"
    ".t-Header .a-Logo,.t-Header .a-Logo .a-Logo-text,.t-Header .t-Header-branding .a-Logo span{color:#fff!important}\n"
    ".t-Header .a-Logo:hover{color:#5eead4!important}\n"
    "</style>"
)

LIMITE = Path(__file__).resolve().parents[1] / "data" / "limite_madrid.json"
LIMITE_JSON = LIMITE.read_text(encoding="utf-8")

FRONT_MAPA = r"""<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
.mv{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#0f172a;max-width:1400px;margin:0 auto;padding:8px}
.mv .sub{font-size:13px;color:#5b6b7c;margin:0 0 10px}
.mv .topbar{display:flex;gap:14px;align-items:flex-end;margin:0 0 12px;flex-wrap:wrap}
.mv .topbar label{display:block;font-size:12px;font-weight:700;color:#334155;margin:0 0 4px}
.mv .topbar select{padding:8px 9px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;background:#fff}
.mv .btnrun{background:#0f766e;color:#fff;border:0;border-radius:9px;padding:10px 16px;font-weight:800;cursor:pointer;font-size:13px;height:38px}
.mv .btnrun:hover{filter:brightness(1.08)}
.mv .btnrun[disabled]{opacity:.6;cursor:wait}
.mv .bar{display:flex;gap:8px;align-items:flex-end;margin:0 0 0 auto;flex-wrap:wrap;opacity:.85}
.mv .bar label{display:block;font-size:11px;font-weight:700;color:#334155;margin:0 0 4px}
.mv .bar input,.mv .bar select{padding:6px 8px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;font-size:11px;background:#fff;max-width:130px}
.mv .bar .inerte{opacity:.55;pointer-events:none}
.mv .bar input[type=range]{max-width:110px}
.mv .err{display:none;margin:0 0 10px;font-size:12px;color:#92400e;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:8px}
.mv .stage{position:relative;min-height:640px;border:1px solid #dbe3ea;border-radius:14px;background:#fff;overflow:hidden}
.mv .stage.locked .mvBlur{filter:blur(7px);pointer-events:none;user-select:none}
.mv #mvOverlay{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:rgba(250,252,253,.72);color:#475569;font-weight:800;font-size:16px;z-index:60;text-align:center;padding:20px}
.mv #mvOverlay .spin{width:26px;height:26px;border-radius:50%;border:3px solid #cbd5e1;border-top-color:#0f766e;animation:mvspin .9s linear infinite}
@keyframes mvspin{to{transform:rotate(360deg)}}
.mv .grid{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:14px;align-items:start}
.mv #mvMap{height:640px;background:#eef3f7;border-radius:10px;z-index:1}
.mv .side{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:12px;margin-bottom:12px}
.mv .side h4{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#5b6b7c;margin:0 0 10px}
.mv .capa{display:block;font-size:12.5px;font-weight:600;color:#334155;margin:6px 0;cursor:pointer}
.mv .capa input{accent-color:#0f766e;margin-right:6px}
.mv .leg{height:10px;border-radius:5px;margin:8px 0 4px;background:linear-gradient(90deg,#C8102E,#f1f5f9 45%,#f1f5f9 55%,#1B7A3C)}
.mv .leg-et{display:flex;justify-content:space-between;font-size:11px;color:#64748b}
.mv .limchip{display:flex;align-items:center;gap:6px;font-size:12px;margin:5px 0}
.mv .limchip i{width:12px;height:12px;border-radius:50%;display:inline-block}
.mv .estado{font-size:11.5px;color:#64748b;line-height:1.5}
.mv .top{list-style:none;margin:0;padding:0;font-size:12px}
.mv .top li{display:flex;justify-content:space-between;gap:6px;padding:5px 6px;border-radius:7px;cursor:pointer}
.mv .top li:hover{background:#f4f7fa}
.mv .top li b{font-variant-numeric:tabular-nums}
.mv .tarjeta{position:absolute;top:12px;left:12px;width:300px;background:#fff;border:1px solid #dbe3ea;border-radius:12px;box-shadow:0 8px 22px rgba(15,42,68,.14);padding:12px;z-index:50;display:none;font-size:12px}
.mv .tarjeta b.t{font-size:15px;color:#0f2a44}
.mv .tarjeta .an{color:#64748b;font-size:11px;margin:2px 0 8px}
.mv .tarjeta .filas{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:8px 0}
.mv .tarjeta .f{background:#f6f9fb;border-radius:8px;padding:6px 8px}
.mv .tarjeta .f div{font-size:10px;text-transform:uppercase;letter-spacing:.05em;color:#5b6b7c;font-weight:700}
.mv .tarjeta .f b{font-size:13px;color:#0f2a44}
.mv .tarjeta .cierre{margin-top:8px;font-size:11px;color:#5b6b7c;border-top:1px dashed #e2e8f0;padding-top:6px}
.mv .pos{color:#0f766e}.mv .neg{color:#b91c1c}
.mv .pills{position:absolute;top:10px;right:10px;z-index:20;display:flex;gap:6px}
.mv .mv-pill{border:1px solid #cbd5e1;background:#fff;border-radius:99px;padding:5px 10px;font-size:11px;font-weight:700;cursor:pointer}
.mv .mv-pill.on{background:#0f766e;color:#fff;border-color:#0f766e}
@media(max-width:1000px){.mv .grid{grid-template-columns:1fr}}
</style>
<div class="mv">
 <div class="topbar">
  <div><label>A&ntilde;o: <span id="mvV">2030</span></label><input id="mvAnio" type="range" min="2025" max="2035" step="1" value="2030"></div>
  <div><button id="mvBtn" type="button" class="btnrun">Ejecutar Predicci&oacute;n</button></div>
  <div class="bar">
   <div><label>Buscar</label><input type="text" id="mvQ" disabled></div>
   <div><label>Comarca</label><select id="mvCom" disabled><option value="all">Todas</option></select></div>
   <div><label>Poblaci&oacute;n</label><input type="range" id="mvPop" disabled></div>
   <div><label>Transporte</label><input type="range" id="mvTr" disabled></div>
   <div><label>Cuello de botella</label><select id="mvLim" disabled>
     <option value="all">Cualquier factor</option>
     <option>Demogr&aacute;fico</option><option>Vivienda</option><option>Servicios</option>
     <option>Accesibilidad</option><option>Empleo</option>
   </select></div>
  </div>
 </div>
 <div id="mvErr" class="err"></div>
 <div class="stage locked" id="mvStage">
  <div id="mvOverlay"><div id="mvSpin" class="spin" style="display:none"></div>Ejecuta la predicci&oacute;n para visualizar</div>
  <div class="mvBlur">
   <div class="grid">
    <div style="position:relative"><div id="mvMap"></div>
     <div class="pills">
      <button type="button" class="mv-pill on" data-tile="ign">IGN</button>
      <button type="button" class="mv-pill" data-tile="street">Callejero</button>
      <button type="button" class="mv-pill" data-tile="sat">Sat&eacute;lite</button>
     </div>
    </div>
    <div class="lc-side">
     <div class="side"><h4>Capa activa (diferencial 2025 &rarr; a&ntilde;o)</h4><div id="mvCapas"></div><div id="mvLeyenda"></div></div>
     <div class="side"><h4>Estado</h4><div class="estado" id="mvEstado">&mdash;</div></div>
     <div class="side"><h4>Top 5</h4><ul class="top" id="mvTop"></ul></div>
    </div>
   </div>
   <div class="tarjeta" id="mvTarjeta"></div>
  </div>
 </div>
</div>
<script>window.__MV_LIMITE = __LIMITE_JSON__;</script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
(function(){
"use strict";
var DATA=[], M={}, GEO=null, GEO_MUNS={}, RESULT=null, ANIO=2030, CAPA="difpob", SEL=null, READY=false;
var MAP=null, geoLayer=null, suelto=null, TILE=null;
var VERDE="#1B7A3C", ROJO="#C8102E", GRIS="#A0AEC0";
var COLOR_DIM={"Demograf\u00eda":"#7C3AED","Vivienda":"#B7791F","Servicios":"#0078A8","Accesibilidad":"#38A169","Empleo":"#D69E2E"};
var CAPAS=[
  {k:"difpob",  label:"\u0394Poblaci\u00f3n (hab.)",        f:function(m){return m.d_pob;},       dec:0},
  {k:"difpobp", label:"\u0394Poblaci\u00f3n (%)",           f:function(m){return m.d_pob_pct;},   dec:2},
  {k:"difidx",  label:"\u0394\u00cdndice de vitalidad",     f:function(m){return m.d_indice;},    dec:1},
  {k:"difval",  label:"\u0394Valor catastral (%)",          f:function(m){return m.d_valor_pct;}, dec:2},
  {k:"difsal",  label:"\u0394Salud (centros/10k)",          f:function(m){return num(m.salud_10k_y)-num(m.salud_10k_2025);}, dec:2},
  {k:"difesc",  label:"\u0394Escuelas (/1k)",               f:function(m){return num(m.escuelas_1000_y)-num(m.escuelas_1000_2025);}, dec:3},
  {k:"difpar",  label:"\u0394Paradas (/1k)",                f:function(m){return num(m.paradas_1000_y)-num(m.paradas_1000_2025);}, dec:3},
  {k:"difviv",  label:"\u0394Viviendas (/1k)",              f:function(m){return num(m.viv_1000_y)-num(m.viv_1000_2025);}, dec:1},
  {k:"lim",     label:"Factor limitante (a\u00f1o)",        f:function(m){return m.factor_limitante;}, dec:0}
];
function $(i){return document.getElementById(i);}
function esc(s){return (s==null?"":(""+s)).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function fmt(v,d){return (v===null||v===undefined)?"\u2014":Number(v).toLocaleString("es-ES",{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}
function num(v){v=Number(v);return isNaN(v)?0:v;}
function capaDef(k){for(var i=0;i<CAPAS.length;i++)if(CAPAS[i].k===k)return CAPAS[i];return CAPAS[0];}
function capaVal(m){try{var v=capaDef(CAPA).f(m);return (v==null||isNaN(v))?null:v;}catch(e){return null;}}
var MVMAX=1;
function calcularMax(){var mx=0;for(var i=0;i<DATA.length;i++){var v=capaVal(DATA[i]);if(v!==null&&v!==undefined)mx=Math.max(mx,Math.abs(num(v)));}MVMAX=mx||1;}
function colorCapa(m){
  if(CAPA==="lim")return COLOR_DIM[m.factor_limitante]||GRIS;
  var v=capaVal(m);if(v===null||v===undefined||num(v)===0)return GRIS;
  var t=Math.min(1,Math.abs(num(v))/MVMAX);
  var base=num(v)>0?[27,122,60]:[200,16,46];
  return "rgb("+Math.round(255-(255-base[0])*t)+","+Math.round(255-(255-base[1])*t)+","+Math.round(255-(255-base[2])*t)+")";
}
function api(n,p,cb){apex.server.process(n,p,{dataType:"json",success:cb,error:function(){var e=$("mvErr"),b=$("mvBtn"),s=$("mvSpin");if(e){e.style.display="block";e.textContent="El servidor respondio con error; revisa el log de la base.";}if(b)b.disabled=false;if(s)s.style.display="none";}});}
function render(){
  calcularMax();
  if(geoLayer)geoLayer.eachLayer(function(l){l.setStyle({fillColor:colorCapa(M[l.__cod]||{})});});
  if(suelto)suelto.eachLayer(function(l){l.setStyle({fillColor:colorCapa(M[l.__cod]||{})});});
  dibujarTop();dibujarLeyenda();dibujarEstado();if(SEL&&M[SEL])pintarTarjeta(M[SEL],true);
}
function dibujarTop(){
  var clave=(CAPA==="lim")?"d_indice":CAPA;
  var lista=DATA.slice().sort(function(a,b){return num(b[clave==="difpob"?"d_pob":clave])-num(a[clave==="difpob"?"d_pob":clave]);}).slice(0,5);
  var def=capaDef(CAPA);
  $("mvTop").innerHTML=lista.map(function(m,i){return "<li data-cod=\""+m.cod+"\"><span><b>"+(i+1)+".</b> "+esc(m.nombre)+"</span><b>"+(CAPA==="lim"?esc(m.factor_limitante):fmt(capaVal(m),def.dec))+"</b></li>";}).join("");
  Array.prototype.forEach.call($("mvTop").querySelectorAll("li"),function(li){li.onclick=function(){SEL=li.getAttribute("data-cod");if(M[SEL])pintarTarjeta(M[SEL],true);};});
}
function dibujarLeyenda(){
  var el=$("mvLeyenda");
  if(CAPA==="lim"){el.innerHTML=Object.keys(COLOR_DIM).map(function(d){return "<div class=\"limchip\"><i style=\"background:"+COLOR_DIM[d]+"\"></i>"+esc(d)+"</div>";}).join("");return;}
  var mx=MVMAX||1;var dec=capaDef(CAPA).dec;
  el.innerHTML="<div class=\"leg\"></div><div class=\"leg-et\"><span class=\"neg\">\u25BC "+fmt(-mx,dec)+"</span><span>0</span><span class=\"pos\">\u25B1 +"+fmt(mx,dec)+"</span></div>";
}
function dibujarEstado(){$("mvEstado").innerHTML="Mostrando <b>"+DATA.length+"</b> municipios \u00B7 A\u00F1o <b>"+ANIO+"</b><br>Modelos: M3 + M4 (\u00D75) + M6 \u00B7 ONNX dentro de Oracle";}
function pintarTarjeta(m,fij){
  var c=capaDef(CAPA);var v=capaVal(m);var col=(num(v)>0)?"pos":(num(v)<0)?"neg":"";
  var cuerpo=(CAPA==="lim")
    ? "<div class=\"f\" style=\"grid-column:1/-1\"><div>Factor limitante "+ANIO+"</div><b>"+esc(m.factor_limitante)+"</b></div>"
    : "<div class=\"f\" style=\"grid-column:1/-1\"><div>"+esc(c.label)+"</div><b class=\""+col+"\">"+(num(v)>0?"+":"")+fmt(v,c.dec)+"</b></div>";
  var filas=[
    ["Poblaci\u00f3n",fmt(m.pob_2025)+" \u2192 "+fmt(m.pob_y)],
    ["\u0394Poblaci\u00f3n",(m.d_pob>0?"+":"")+fmt(m.d_pob)+" ("+fmt(m.d_pob_pct,2)+"%)"],
    ["\u00CDndice",fmt(m.indice_2025,1)+" \u2192 "+fmt(m.indice_y,1)],
    ["Banda M3",fmt(m.p10)+" / "+fmt(m.p90)],
    ["Salud/10k",fmt(m.salud_10k_2025,2)+" \u2192 "+fmt(m.salud_10k_y,2)],
    ["Escuelas/1k",fmt(m.escuelas_1000_2025,3)+" \u2192 "+fmt(m.escuelas_1000_y,3)],
    ["Paradas/1k",fmt(m.paradas_1000_2025,3)+" \u2192 "+fmt(m.paradas_1000_y,3)],
    ["Viviendas/1k",fmt(m.viv_1000_2025,1)+" \u2192 "+fmt(m.viv_1000_y,1)],
    ["Valor catastral",fmt(m.valor_2025)+" \u2192 "+fmt(m.valor_y)+" \u20AC"],
    ["\u0394Valor",fmt(m.d_valor_pct,2)+" %"]
  ];
  var grid=filas.map(function(x){return "<div class=\"f\"><div>"+x[0]+"</div><b>"+x[1]+"</b></div>";}).join("");
  $("mvTarjeta").innerHTML="<b class=\"t\">"+esc(m.nombre)+"</b><div class=\"an\">cod "+m.cod+" \u00B7 a\u00F1o "+ANIO+" \u00B7 base 2025</div>"
   +"<div class=\"filas\">"+cuerpo+grid+"</div>"
   +"<div class=\"cierre\">Factor limitante: <b>"+esc(m.factor_limitante)+"</b> \u00B7 M3+M4+M6 ONNX en Oracle \u00B7 salida ef\u00EDmera</div>";
  $("mvTarjeta").style.display="block";
}
function cerrarTarjeta(){$("mvTarjeta").style.display="none";}
function run(){
  if($("mvBtn").disabled)return;
  $("mvErr").style.display="none";
  $("mvBtn").disabled=true;$("mvSpin").style.display="block";
  ANIO=Number($("mvAnio").value)||2030;$("mvV").textContent=String(ANIO);
  api("PRED",{x01:ANIO},function(d){
   $("mvBtn").disabled=false;$("mvSpin").style.display="none";
   RESULT=d;DATA=d.municipios||[];M={};DATA.forEach(function(m){M[m.cod]=m;});
   $("mvStage").classList.remove("locked");$("mvOverlay").style.display="none";
   calcularMax();render();
  });
}
function pintaGeo(){
  if(geoLayer)MAP.removeLayer(geoLayer);
  geoLayer=L.geoJSON(GEO,{
    style:function(f){return {color:"#fff",weight:1,fillColor:colorCapa(M[f.properties.cod]||{}),fillOpacity:.85};},
    onEachFeature:function(f,l){l.__cod=f.properties.cod;
     l.on("mouseover",function(){l.setStyle({weight:2.5,color:"#232323"});if(M[f.properties.cod])pintarTarjeta(M[f.properties.cod],false);});
     l.on("mouseout",function(){l.setStyle({weight:1,color:"#fff"});if(SEL!==f.properties.cod)cerrarTarjeta();});
     l.on("click",function(){if(M[f.properties.cod]){SEL=f.properties.cod;pintarTarjeta(M[SEL],true);}});
    }
  }).addTo(MAP);
}
function dibujarSueltos(){
  if(!suelto)return;suelto.clearLayers();
  DATA.forEach(function(m){ if(GEO_MUNS[m.cod])return;
   var mk=L.circleMarker([m.lat,m.lon],{radius:7,fillColor:colorCapa(m),fillOpacity:.85,color:"#fff",weight:1.5});
   mk.__cod=m.cod;
   mk.on("click",function(){SEL=m.cod;pintarTarjeta(m,true);});
   mk.on("mouseover",function(){pintarTarjeta(m,false);});
   mk.on("mouseout",function(){if(SEL!==m.cod)cerrarTarjeta();});
   suelto.addLayer(mk);
  });
}
function boot(){
  MAP=L.map("mvMap",{center:[40.55,-3.65],zoom:9,minZoom:8,maxZoom:13,zoomControl:false});
  L.control.zoom({position:"bottomright"}).addTo(MAP);
  MAP.on("click",function(){SEL=null;cerrarTarjeta();});
  var TILES={
   ign:{url:"https://www.ign.es/wmts/ign-base?service=WMTS&request=GetTile&version=1.0.0&Format=image/png&layer=IGNBaseTodo&style=default&tilematrixset=GoogleMapsCompatible&TileMatrix={z}&TileRow={y}&TileCol={x}",opt:{maxZoom:18,attribution:"\u00A9 IGN Espa\u00F1a / CNIG"}},
   street:{url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",opt:{maxZoom:18,attribution:"Tiles \u00A9 Esri"}},
   sat:{url:"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",opt:{maxZoom:19,attribution:"Tiles \u00A9 Esri, Maxar"}}
  };
  function setTile(k){if(TILE)MAP.removeLayer(TILE);TILE=L.tileLayer(TILES[k].url,TILES[k].opt).addTo(MAP);TILE.bringToBack();
   Array.prototype.forEach.call(document.querySelectorAll(".mv-pill"),function(b){b.classList.toggle("on",b.getAttribute("data-tile")===k);});}
  Array.prototype.forEach.call(document.querySelectorAll(".mv-pill"),function(b){b.addEventListener("click",function(){setTile(b.getAttribute("data-tile"));});});
  setTile("ign");
  L.geoJSON(window.__MV_LIMITE,{style:{color:"#0078A8",weight:2,dashArray:"3, 4",fillColor:"#0078A8",fillOpacity:0.04},interactive:false}).addTo(MAP);
  suelto=L.layerGroup().addTo(MAP);
  $("mvCapas").innerHTML=CAPAS.map(function(c){return "<label class=\"capa"+(c.k===CAPA?" on":"")+"\"><input type=\"radio\" name=\"mvcapa\" value=\""+c.k+"\""+(c.k===CAPA?" checked":"")+">"+esc(c.label)+"</label>";}).join("");
  Array.prototype.forEach.call(document.querySelectorAll('input[name=mvcapa]'),function(r){r.addEventListener("change",function(){CAPA=r.value;render();});});
  window.addEventListener("resize",function(){MAP.invalidateSize();});
  api("GEO",{},function(fc){GEO=fc;GEO_MUNS={};(fc.features||[]).forEach(function(f){GEO_MUNS[f.properties.cod]=true;});pintaGeo();dibujarSueltos();render();});
  setTimeout(function(){MAP.invalidateSize();},300);
  READY=true;
}
// ── listeners básicos (sin Leaflet) ──
$("mvAnio").addEventListener("input",function(){$("mvV").textContent=this.value;});
$("mvBtn").addEventListener("click",function(){ if(READY)run(); });
document.addEventListener("keydown",function(e){ if(e.key==="Enter"&&READY&&!$("mvBtn").disabled){ e.preventDefault(); run(); } });
// ── arranque: espera Leaflet + apex, luego boot ──
var _intentos=0;
(function _w(){ _intentos++;
 if(_intentos>300)return;
 if(window.apex&&window.apex.server&&window.L&&window.__MV_LIMITE){setTimeout(boot,150);} else {setTimeout(_w,100);}
})();
})();
</script>"""

# contorno de la Comunidad de Madrid embebido (boot usa window.__MV_LIMITE)
FRONT_MAPA = FRONT_MAPA.replace('__LIMITE_JSON__', LIMITE_JSON)

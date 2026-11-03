"""Front de la página 50 — Comparador de municipios.

Basado en el prototipo de `doc/legacy/interfaz.html` (sección VIEW 3:
"Comparador Multidimensional": chips de municipios + radar de 5 dimensiones +
tabla comparativa) con el mismo lenguaje visual del Mapa (.mv) y el Simulador
(.sw): cabecera teal, tarjetas, tablas y estado de carga.

Estructura:
  CABECERA_COMPARADOR -> primer HTP.P (estilos .t-Header, igual que los demás)
  FRONT_COMPARADOR    -> segundo HTP.P (CSS + HTML + JS; sin librerías)

Procesos AJAX de la propia página:
  DATOS -> lista de municipios (mismo proceso que el Simulador)
  CMP   -> PV_MAPA(año, cod): LAS métricas del mapa con EXACTAMENTE el mismo
           pipeline (PV_BASE_MODELOS + M1/M2/M3/M4), pero SOLO ese municipio.

Flujo si se abre directamente: año objetivo + lista de municipios a comparar
(chips, sin límite) → botón "Comparar" → CMP una vez por municipio → tabla +
radar. Si sessionStorage trae "pvCmpList" (la escribirá el Mapa en la
integración futura), se preseleccionan esos municipios y se limpia la clave.
"""

CABECERA_COMPARADOR = (
    "<style>\n"
    ".t-Header,.t-Header .t-Header-branding,.t-Header .t-Header-navBar{background:#0f766e!important}\n"
    ".t-Header .a-Logo,.t-Header .a-Logo .a-Logo-text,.t-Header .t-Header-branding .a-Logo span{color:#fff!important}\n"
    ".t-Header .a-Logo:hover{color:#5eead4!important}\n"
    "</style>"
)

FRONT_COMPARADOR = r"""<style>
.cp{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#0f172a;max-width:1400px;margin:0 auto;padding:8px}
.cp h1{font-size:26px;line-height:1.15;margin:6px 0 2px;color:#0f2a44}
.cp .sub{font-size:13px;color:#5b6b7c;margin:0 0 10px}
.cp .topbar{display:flex;gap:14px;align-items:flex-end;margin:0 0 12px;flex-wrap:wrap}
.cp .topbar label{display:block;font-size:12px;font-weight:700;color:#334155;margin:0 0 4px}
.cp .topbar input[type=range]{width:200px;accent-color:#0f766e}
.cp .btnrun{background:#0f766e;color:#fff;border:0;border-radius:9px;padding:10px 16px;font-weight:800;cursor:pointer;font-size:13px;height:38px}
.cp .btnrun:hover{filter:brightness(1.08)}
.cp .btnrun[disabled]{opacity:.6;cursor:wait}
.cp .btn2{background:#fff;border:1px solid #cbd5e1;color:#0f766e;font-weight:800;border-radius:8px;padding:8px 14px;cursor:pointer;font-size:12px}
.cp .btn2:hover{filter:brightness(1.05)}
.cp .btn2[disabled]{opacity:.45;cursor:not-allowed}
.cp .sec{background:#fff;border:1px solid #dbe3ea;border-radius:14px;padding:14px;margin-bottom:14px}
.cp .sec h4{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#5b6b7c;margin:0 0 10px}
.cp .chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 10px}
.cp .chip{display:inline-flex;align-items:center;gap:6px;background:#f6f9fb;border:1px solid #dbe3ea;border-radius:99px;padding:5px 12px;font-size:12px;font-weight:700;color:#334155}
.cp .chip b{color:#0f766e}
.cp .chip button{border:0;background:transparent;cursor:pointer;font-weight:800;color:#94a3b8;font-size:13px;padding:0 2px}
.cp .chip button:hover{color:#b91c1c}
.cp .addrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.cp .addrow select{min-width:280px;padding:8px 9px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;background:#fff}
.cp .mu{font-size:11.5px;color:#64748b}
.cp .err{display:none;margin:0 0 10px;font-size:12px;color:#92400e;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:8px}
.cp .stage{position:relative;min-height:520px;border:1px solid #dbe3ea;border-radius:14px;background:#fff;overflow:hidden}
.cp .stage.locked .cpBlur{filter:blur(7px);pointer-events:none;user-select:none}
.cp #cpOverlay{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:rgba(250,252,253,.72);color:#475569;font-weight:800;font-size:16px;z-index:60;text-align:center;padding:20px;display:none}
.cp #cpOverlay .spin{width:26px;height:26px;border-radius:50%;border:3px solid #cbd5e1;border-top-color:#0f766e;animation:cpspin .9s linear infinite}
@keyframes cpspin{to{transform:rotate(360deg)}}
.cp .grid{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:14px;align-items:start}
.cp .rad-box{border:1px solid #dbe3ea;border-radius:12px;padding:10px;background:#fcfdfe}
.cp table{width:100%;border-collapse:collapse;font-size:12.5px}
.cp th{text-align:right;color:#5b6b7c;font-size:10px;text-transform:uppercase;letter-spacing:.05em;background:#f6f9fb;padding:8px 6px;border-bottom:1px solid #dbe3ea}
.cp th:first-child{text-align:left}
.cp td{padding:7px 6px;border-bottom:1px solid #eef2f6;text-align:right;font-variant-numeric:tabular-nums;color:#0f2a44}
.cp td:first-child{text-align:left;font-weight:700;color:#334155}
.cp .pos{color:#0f766e}.cp .neg{color:#b91c1c}.cp .mu{color:#94a3b8}
.cp .colhead{display:inline-flex;align-items:center;gap:6px}
.cp .dot{width:10px;height:10px;border-radius:50%;display:inline-block}
.cp #cpLeyenda{display:flex;gap:10px;flex-wrap:wrap;margin:8px 0 4px;font-size:11px;color:#5b6b7c}
@media(max-width:1000px){.cp .grid{grid-template-columns:1fr}}
</style>
<div class="cp">
 <h1>Comparador de municipios</h1>
 <div class="sub">Proyecci&oacute;n del a&ntilde;o objetivo para los municipios que elijas, con las mismas m&eacute;tricas del mapa &mdash; el modelo se ejecuta una vez por municipio.</div>
 <div class="topbar">
  <div><label>A&ntilde;o: <span id="cpV">2030</span></label><input id="cpAnio" type="range" min="2025" max="2035" step="1" value="2030"></div>
  <div><button id="cpBtn" type="button" class="btnrun" disabled>Comparar</button></div>
 </div>
 <div id="cpErr" class="err"></div>
 <div class="sec">
  <h4>Municipios en la comparativa (sin l&iacute;mite)</h4>
  <div class="chips" id="cpChips"></div>
  <div class="addrow">
   <select id="cpSel" disabled><option value="">Cargando municipios&hellip;</option></select>
   <button id="cpAdd" type="button" class="btn2" disabled>+ A&ntilde;adir</button>
   <button id="cpClr" type="button" class="btn2" disabled>Vaciar</button>
   <span class="mu" id="cpEstado">&mdash;</span>
  </div>
 </div>
 <div class="stage locked" id="cpStage">
  <div id="cpOverlay"><div id="cpSpin" class="spin" style="display:none"></div>Cargando&hellip;</div>
  <div class="cpBlur">
   <div class="grid">
    <div>
     <div class="sec"><h4>Comparativa (base 2025 &rarr; a&ntilde;o objetivo)</h4><table id="cpTab"></table></div>
    </div>
    <div>
     <div class="sec"><h4>Perfil radar de las 5 dimensiones</h4>
      <div class="rad-box"><svg id="cpRadar" width="100%" height="320" viewBox="0 0 360 320"></svg></div>
      <div id="cpLeyenda"></div>
     </div>
    </div>
   </div>
  </div>
 </div>
</div>
<script>
(function(){
"use strict";
var MUNIS=[], BYCODE={}, SEL=[], RES=[], FIFO=[], BUSY=false, ANIO=2030;
var PALETA=["#0f766e","#B7791F","#0078A8","#7C3AED","#D69E2E","#b91c1c","#38A169","#232649","#0ea5e9","#f59e0b"];
var DIMS=[["Demograf\u00eda","dim_dem"],["Vivienda","dim_viv"],["Servicios","dim_ser"],["Accesibilidad","dim_acc"],["Empleo","dim_emp"]];
var METRICAS=[
  ["Poblaci\u00f3n 2025 \u2192 a\u00f1o", function(m){return fmt(m.pob_2025,0)+" \u2192 "+fmt(m.pob_y,0);}],
  ["\u0394Poblaci\u00f3n (%)", function(m){return pct(m.d_pob_pct);}],
  ["\u00CDndice 2025 \u2192 a\u00f1o", function(m){return fmt(m.indice_2025,1)+" \u2192 "+fmt(m.indice_y,1);}],
  ["\u0394\u00CDndice de vitalidad", function(m){var n=Number(m.d_indice);var cls=(n>0)?"pos":(n<0)?"neg":"mu";return "<span class=\""+cls+"\">"+pct(m.d_indice,1)+"</span>";}],
  ["Factor limitante (a\u00f1o)", function(m){return esc(m.factor_limitante);}],
  ["Salud /10k hab.", function(m){return fmt(m.salud_10k_2025,2)+" \u2192 "+fmt(m.salud_10k_y,2);}],
  ["Escuelas /1k hab.", function(m){return fmt(m.escuelas_1000_2025,3)+" \u2192 "+fmt(m.escuelas_1000_y,3);}],
  ["Paradas /1k hab.", function(m){return fmt(m.paradas_1000_2025,3)+" \u2192 "+fmt(m.paradas_1000_y,3);}],
  ["Viviendas /1k hab.", function(m){return fmt(m.viv_1000_2025,1)+" \u2192 "+fmt(m.viv_1000_y,1);}],
  ["Valor catastral (\u20AC)", function(m){return fmt(m.valor_2025,0)+" \u2192 "+fmt(m.valor_y,0);}],
  ["\u0394Valor (%)", function(m){var n=Number(m.d_valor_pct);var cls=(n>0)?"pos":(n<0)?"neg":"mu";return "<span class=\""+cls+"\">"+pct(m.d_valor_pct,2)+"</span>";}]
];
function $(i){return document.getElementById(i);}
function esc(s){return (s==null?"":(""+s)).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function fmt(n,d){return (n==null||isNaN(Number(n)))?"--":Number(n).toLocaleString("es-ES",{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}
function pct(v,d){var n=Number(v);return isNaN(n)?"--":(n>0?"+":"")+fmt(n,d||2)+"%";}
function colorOf(cod){for(var k=0;k<FIFO.length;k++)if(FIFO[k]===cod)return PALETA[k%PALETA.length];return PALETA[0];}
function api(n,p,cb){apex.server.process(n,p,{dataType:"json",success:cb,error:function(){var e=$("cpErr"),b=$("cpBtn"),o=$("cpOverlay"),s=$("cpSpin");if(e){e.style.display="block";e.textContent="El servidor respondio con error; revisa el log de la base.";}if(b)b.disabled=false;if(s)s.style.display="none";if(o)o.style.display="none";BUSY=false;}});}

function dibujaChips(){
  $("cpChips").innerHTML=SEL.map(function(cod){
    var m=BYCODE[cod]||{nombre:cod};
    return "<span class=\"chip\"><b>"+esc(cod)+"</b> "+esc(m.nombre)+" <button type=\"button\" data-x=\""+cod+"\" title=\"Quitar\">&times;</button></span>";
  }).join("");
  Array.prototype.forEach.call($("cpChips").querySelectorAll("button"),function(b){
    b.onclick=function(){var x=b.getAttribute("data-x");
      SEL=SEL.filter(function(c){return c!==x;});
      FIFO=FIFO.filter(function(c){return c!==x;});
      dibujaChips();};
  });
  $("cpClr").disabled=SEL.length===0;
  $("cpBtn").disabled=(SEL.length===0||BUSY);
  $("cpEstado").innerHTML=SEL.length?("<b>"+SEL.length+"</b> municipio(s) en cola"):"&mdash;";
}
function addSel(){
  var cod=$("cpSel").value;
  if(!cod||SEL.indexOf(cod)>=0)return;
  SEL.push(cod);FIFO.push(cod);
  RES=[];dibujaChips();
}
function limpiar(){SEL=[];FIFO=[];RES=[];dibujaChips();}
function run(){
  if(BUSY||SEL.length===0)return;
  $("cpErr").style.display="none";
  BUSY=true;$("cpBtn").disabled=true;$("cpSpin").style.display="block";$("cpOverlay").style.display="flex";
  ANIO=Number($("cpAnio").value)||2030;$("cpV").textContent=String(ANIO);
  RES=[];
  var pend=FIFO.slice();
  function paso(){
    var cod=pend.shift();
    if(!cod){BUSY=false;$("cpSpin").style.display="none";$("cpOverlay").style.display="none";render();dibujaChips();return;}
    api("CMP",{x01:ANIO,x02:cod},function(d){
      var arr=(d&&d.municipios)||[];
      if(arr.length)RES.push(arr[0]);
      paso();
    });
  }
  paso();
}
function dibujaTab(){
  var h="<tr><th>M\u00e9trica</th>"+RES.map(function(r){var c=colorOf(r.cod);
    return "<th><span class=\"colhead\"><span class=\"dot\" style=\"background:"+c+"\"></span>"+esc(r.nombre||r.cod)+"</span></th>";}).join("")+"</tr>";
  var filas=METRICAS.map(function(f){
    return "<tr><td>"+f[0]+"</td>"+RES.map(function(r){return "<td>"+f[1](r)+"</td>";}).join("")+"</tr>";
  }).join("");
  $("cpTab").innerHTML=h+filas;
}
function dibujaRadar(){
  var C=180,CY=160,R=110;
  function pt(i,v){var a=-Math.PI/2+i*2*Math.PI/DIMS.length;var r=R*(Math.max(0,Math.min(100,v||0))/100);return [C+r*Math.cos(a),CY+r*Math.sin(a)];}
  var s='<g stroke="#dbe3ea" fill="none">';
  [25,50,75,100].forEach(function(q){var p="";for(var i=0;i<DIMS.length;i++){var xy=pt(i,q);p+=xy[0].toFixed(1)+","+xy[1].toFixed(1)+" ";}s+='<polygon points="'+p+'"/>';});
  for(var i=0;i<DIMS.length;i++){var ei=pt(i,112);var li=pt(i,131);
    s+='<line x1="180" y1="160" x2="'+ei[0].toFixed(1)+'" y2="'+ei[1].toFixed(1)+'"/>'+
       '<text x="'+li[0].toFixed(1)+'" y="'+li[1].toFixed(1)+'" text-anchor="middle" font-size="10" fill="#5b6b7c">'+DIMS[i][0]+'</text>';}
  s+='</g>';
  RES.forEach(function(r){
    var pts="";DIMS.forEach(function(d,i){var xy=pt(i,r[d[1]+"_y"]||0);pts+=xy[0].toFixed(1)+","+xy[1].toFixed(1)+" ";});
    var col=colorOf(r.cod);
    s+='<polygon points="'+pts+'" fill="'+col+'" fill-opacity="0.10" stroke="'+col+'" stroke-width="2"/>';
  });
  $("cpRadar").innerHTML=s;
  $("cpLeyenda").innerHTML=RES.map(function(r){var c=colorOf(r.cod);
    return "<span class=\"colhead\"><span class=\"dot\" style=\"background:"+c+"\"></span>"+esc(r.nombre||r.cod)+"</span>";}).join("");
}
function render(){
  if(!RES.length){$("cpStage").classList.add("locked");return;}
  dibujaTab();dibujaRadar();
  $("cpStage").classList.remove("locked");
}
function boot(){
  var o="",y;
  for(y=2025;y<=2035;y++){o+="<option value=\""+y+"\">"+y+"</option>";}
  api("DATOS",{},function(rows){
    MUNIS=rows||[];
    MUNIS.sort(function(a,b){return (a.nombre<b.nombre?-1:(a.nombre>b.nombre?1:0));});
    $("cpSel").innerHTML=MUNIS.map(function(x){return "<option value=\""+esc(x.cod)+"\">"+esc(x.nombre)+" ("+esc(x.cod)+")</option>";}).join("");
    $("cpSel").disabled=false;$("cpAdd").disabled=false;$("cpClr").disabled=(SEL.length===0);
    // preselección futura desde el Mapa (sessionStorage pvCmpList)
    var pv=null;try{pv=JSON.parse(sessionStorage.getItem("pvCmpList")||"null");}catch(e){pv=null;}
    if(pv&&pv.length){pv.forEach(function(cod){if(BYCODE[cod]&&SEL.indexOf(cod)<0){SEL.push(cod);FIFO.push(cod);}});sessionStorage.removeItem("pvCmpList");dibujaChips();}
  });
  $("cpAnio").addEventListener("input",function(){$("cpV").textContent=this.value;});
  $("cpAdd").addEventListener("click",addSel);
  $("cpClr").addEventListener("click",limpiar);
  $("cpBtn").addEventListener("click",run);
  $("cpSel").addEventListener("keydown",function(e){
    if(e.key==="Enter"){e.preventDefault();addSel();}
    else if(e.key==="Backspace"||e.key==="Delete"){limpiar();}
  });
  document.addEventListener("keydown",function(e){ if(e.key==="Enter"&&!BUSY&&SEL.length){ e.preventDefault(); run(); } });
  dibujaChips();
}
(function w(){ if(window.apex&&window.apex.server){setTimeout(boot,400);} else {setTimeout(w,100);} })();
})();
</script>"""

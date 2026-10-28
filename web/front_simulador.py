"""Front de la página 10 — Simulador What-If (dos fases).

Texto EJECUTABLE (comillas simples; el export las dobla — este fichero
hace el des-escape). Canonizado del estado vivo (menú de descarga/import
incluido) + parche AUTO-JUGADA desde el Mapa: si sessionStorage trae
"pvWiJugada" ({cod, anio}), la pág. 10 preselecciona el municipio (tras
rellenar el select con DATOS) y ejecuta la FASE 1 (SIMULAR con sliders
a 0) sin interacción. La clave se limpia después (refresh no re-juega).

CABECERA_SIM -> primer HTP.P (estilos .t-Header del Simulador)
FRONT_SIM    -> segundo HTP.P (CSS + HTML + JS del Simulador)
Aplicar con: python web/actualizar_front_simulador.py
"""

from pathlib import Path

CABECERA_SIM = r"""<style>
.t-Header,.t-Header .t-Header-branding,.t-Header .t-Header-navBar{background:#0f766e!important}
.t-Header .a-Logo,.t-Header .a-Logo .a-Logo-text,.t-Header .t-Header-branding .a-Logo span{color:#fff!important}
.t-Header .a-Logo:hover{color:#5eead4!important}
</style>
</style>"""

FRONT_SIM = r"""<style>
.sw{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#0f172a;max-width:1280px;margin:0 auto;padding:8px}
.sw .bar{display:flex;gap:8px;align-items:center;margin:0 0 0 auto}
.sw .dldrop{position:relative;margin-left:auto;display:flex;gap:8px;align-items:center}
.sw .dlmenu{display:none;position:absolute;right:0;top:calc(100% + 4px);background:#fff;border:1px solid #cbd5e1;border-radius:9px;box-shadow:0 8px 22px rgba(15,42,68,.14);z-index:20;min-width:150px;overflow:hidden}
.sw .dlmenu button{display:block;width:100%;text-align:left;background:#fff;border:0;padding:9px 12px;font:inherit;font-size:12px;font-weight:700;color:#334155;cursor:pointer}
.sw .dlmenu button:hover{background:#f4f7fa;color:#0f766e}
.sw .btn2{background:#fff;border:1px solid #cbd5e1;color:#0f766e;font-weight:800;border-radius:8px;padding:8px 14px;cursor:pointer;font-size:12px}
.sw .btn2:hover{filter:brightness(1.05)}
.sw .btn2[disabled]{opacity:.45;cursor:not-allowed}
.sw h1{font-size:26px;line-height:1.15;margin:6px 0 2px;color:#0f2a44}
.sw .sub{font-size:13px;color:#5b6b7c;margin:0 0 8px}
.sw .topbar{display:flex;gap:12px;align-items:flex-end;margin:0 0 16px;flex-wrap:wrap}
.sw .topbar>div:not(.dldrop){min-width:200px}
.sw .topbar label{margin:0 0 4px}
.sw .btnrun{background:#0f766e;color:#fff;border:0;border-radius:9px;padding:10px 16px;font-weight:800;cursor:pointer;font-size:13px;height:38px}
.sw .btnrun:hover{filter:brightness(1.08)}
.sw .btnrun[disabled]{opacity:.6;cursor:wait}
.sw .wrap{display:grid;grid-template-columns:300px minmax(0,1fr);gap:16px;align-items:start}
.sw .panel{background:#fff;border:1px solid #dbe3ea;border-radius:14px;padding:15px;position:sticky;top:12px}
.sw .panel h2{font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:#5b6b7c;margin:0 0 12px}
.sw label{display:block;font-size:12px;font-weight:700;color:#334155;margin:10px 0 4px}
.sw input,.sw select{width:100%;padding:8px 9px;border:1px solid #cbd5e1;border-radius:8px;font:inherit;background:#fff}
.sw input[type=number]{font-variant-numeric:tabular-nums}
.sw input[disabled],.sw select[disabled]{background:#f4f7fa;color:#94a3b8}
.sw .note{font-size:11px;color:#5b6b7c;line-height:1.45;margin-top:12px;background:#f4f7fa;border:1px solid #e2e8f0;border-radius:9px;padding:9px}
.sw .err{display:none;margin-top:10px;font-size:12px;color:#92400e;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:8px}
.sw .stage{position:relative;min-height:560px;border:1px solid #dbe3ea;border-radius:14px;background:#fff;overflow:hidden}
.sw .stage.locked #swRes{filter:blur(7px);pointer-events:none;user-select:none}
.sw #swOverlay{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:rgba(250,252,253,.72);color:#475569;font-weight:800;font-size:16px;z-index:5;text-align:center;padding:20px}
.sw #swOverlay .spin{width:26px;height:26px;border-radius:50%;border:3px solid #cbd5e1;border-top-color:#0f766e;animation:swspin .9s linear infinite}
@keyframes swspin{to{transform:rotate(360deg)}}
.sw .kpis{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:14px}
.sw .kpi{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:12px 14px}
.sw .kpi .l{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#5b6b7c;font-weight:800}
.sw .kpi b{display:block;font-size:24px;color:#0f2a44;margin-top:3px;letter-spacing:-.02em}
.sw .kpi .s{font-size:11px;color:#5b6b7c}
.sw .card{background:#fff;border:1px solid #dbe3ea;border-radius:12px;padding:14px;margin-bottom:12px}
.sw h3{font-size:13px;margin:0 0 10px;color:#0f2a44}
.sw .dim{display:grid;grid-template-columns:96px 1fr 1fr 84px;gap:7px;align-items:center;font-size:11px;margin:8px 0}
.sw .dim span{font-weight:700;color:#334155}
.sw .track{height:8px;background:#eef2f6;border-radius:99px;overflow:hidden}
.sw .track i{display:block;height:100%;border-radius:99px}
.sw .track .before{background:#cbd5e1}.sw .track .after{background:#14b8a6}
.sw .dim b{text-align:right;font-variant-numeric:tabular-nums;color:#0f2a44}
.sw table{width:100%;border-collapse:collapse;font-size:12px}
.sw th{text-align:left;color:#5b6b7c;font-size:10px;text-transform:uppercase;letter-spacing:.05em;background:#f6f9fb;padding:7px 6px;border-bottom:1px solid #dbe3ea}
.sw td{padding:6px;border-bottom:1px solid #eef2f6}
.sw .num{text-align:right;font-variant-numeric:tabular-nums}
.sw label .difval{float:right;font-variant-numeric:tabular-nums;font-weight:800}
.sw .difval.pos{color:#0f766e}.sw .difval.neg{color:#b91c1c}.sw .difval.zero{color:#94a3b8}
.sw input[type=range]{accent-color:#0f766e;padding:0}
@media(max-width:980px){.sw .wrap,.sw .kpis{grid-template-columns:1fr}.sw .panel{position:static}}
</style>
<div class="sw">
<h1>Simulador What-If</h1>
 <div class="topbar">
  <div><label>Municipio</label><select id="swCod"></select></div>
  <div><label>A&ntilde;o de predicci&oacute;n</label><select id="swAnio"></select></div>
  <div><button id="swBtn" type="button" class="btnrun">Ejecutar Simulaci&oacute;n</button></div>
  <div class="dldrop">
   <button id="swBtnDl" type="button" class="btn2" disabled>Descargar</button>
   <button id="swBtnImp" type="button" class="btn2">Importar JSON</button>
   <div class="dlmenu" id="swDlMenu" style="display:none">
    <button type="button" data-fmt="json">JSON (.json)</button>
    <button type="button" data-fmt="csv">CSV (.csv)</button>
   </div>
   <input id="swFile" type="file" accept=".json,application/json" style="display:none">
  </div>
 </div>
 <div class="wrap">
  <div class="panel">
   <h2>Diferenciales del escenario (What-If)</h2>
   <label>Diferencial de residentes <span id="swPopV" class="difval zero">0</span></label>
   <input id="swPop" type="range" step="1" value="0" disabled>
   <label>Diferencial de viviendas <span id="swVivV" class="difval zero">0</span></label>
   <input id="swViv" type="range" step="1" value="0" disabled>
   <label>Diferencial de centros de salud <span id="swSalV" class="difval zero">0</span></label>
   <input id="swSal" type="range" step="1" value="0" disabled>
   <label>Diferencial de escuelas <span id="swEscV" class="difval zero">0</span></label>
   <input id="swEsc" type="range" step="1" value="0" disabled>
   <label>Diferencial de paradas <span id="swParV" class="difval zero">0</span></label>
   <input id="swPar" type="range" step="1" value="0" disabled>
   <div id="swErr" class="err"></div>
   <div class="note">Se emplean los modelos <b>M1</b> (proyeccion base al a&ntilde;o seleccionado), <b>M2</b> (5 dimensiones del estado) y <b>M4</b> (stocks proyectados: viviendas/salud/paradas + escuelas esperadas)</div>
  </div>
  <div class="stage locked" id="swStage">
   <div id="swOverlay"><span id="swSpin" class="spin" style="display:none"></span>Ejecuta la simulaci&oacute;n para visualizar</div>
   <div id="swRes" style="padding:16px">
    <div class="kpis">
     <div class="kpi"><div class="l">&Iacute;ndice antes &rarr; escenario</div><b><span id="swIdxA">--</span> &rarr; <span id="swIdxB">--</span></b><div class="s"><span id="swDelta"></span> <span id="swLimit" style="color:#64748b"></span></div></div>     <div class="kpi"><div class="l">Poblaci&oacute;n proyectada M1</div><b id="swPobBase">--</b><div class="s">banda <span id="swBand">--</span> &middot; factor <span id="swFactor">--</span></div></div>
     <div class="kpi"><div class="l">Poblaci&oacute;n escenario</div><b id="swPob">--</b><div class="s" id="swPobS"></div></div>
    </div>
    <div class="card">
     <h3>Cinco dimensiones (0-100)</h3>
     <div id="swDims"></div>
    </div>
    <div class="card">
     <h3>Ratios de saturaci&oacute;n</h3>
     <table id="swRatios"></table>
    </div>
    <div class="card">
     <h3>Choque aplicado</h3>
     <table id="swChoques"></table>
    </div>
   </div>
  </div>
 </div>
</div>
<script>
(function(){
 var RESULT=null, BASE=false;
 function $(i){return document.getElementById(i);}
 function esc(s){return (s==null?"":(""+s)).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
 function num(v,d){return (v==null||v==="")?"--":Number(v).toFixed(d==null?0:d);}
 function api(n,p,cb){apex.server.process(n,p,{dataType:"json",success:cb,error:function(){$("swErr").style.display="block";$("swErr").textContent="El servidor respondio con error; revisa el log de la base.";$("swBtn").disabled=false;$("swSpin").style.display="none";}});}
 function fmtDif(n){var x=Math.round(Number(n)||0);return x>0?"+"+x.toLocaleString("es-ES"):x<0?x.toLocaleString("es-ES"):"0";}
 function pintaDif(id,n){var el=$(id+"V");var x=Math.round(Number(n)||0);el.textContent=fmtDif(x);el.className="difval"+(x>0?" pos":x<0?" neg":" zero");}
 function ponSlider(id,min,max){var el=$(id);var v=Math.round(Number(el.value)||0);min=Math.round(min);max=Math.round(max);if(min>max){var m=min;min=max;max=m;}el.min=min;el.max=max;el.step=1;el.value=Math.min(Math.max(v,min),max);pintaDif(id,el.value);}
 function actualizarLimites(r){
  var d={pop:Number($("swPop").value)||0,viv:Number($("swViv").value)||0,sal:Number($("swSal").value)||0,esc:Number($("swEsc").value)||0,par:Number($("swPar").value)||0};
  var base={pop:Math.max(0,Number(r.poblacion_base_anio)||0),viv:Math.max(0,(Number(r.viviendas_despues)||0)-d.viv),sal:Math.max(0,(Number(r.centros_salud_despues)||0)-d.sal),esc:Math.max(0,(Number(r.escuelas_despues)||0)-d.esc),par:Math.max(0,(Number(r.paradas_despues)||0)-d.par)};
  ponSlider("swPop",-base.pop,3*base.pop);
  ["swViv","swSal","swEsc","swPar"].forEach(function(id){var b=base[id.slice(2).toLowerCase()];ponSlider(id,-b,Math.max(3*b,20));});
 }
 function colMej(a,b){var x=Number(b)-Number(a);return x>0?"#0f766e":x<0?"#b91c1c":"#64748b";}
 function fila(t,a,b,dec,col){return "<tr><td>"+t+"</td><td class=\"num\">"+num(a,dec)+"</td><td class=\"num\""+(col?" style=\"color:"+col+"\"":"")+">"+num(b,dec)+"</td></tr>";}
 function render(r){
  if(!r||typeof r!=="object"||!("indice_despues" in r)){$("swErr").style.display="block";$("swErr").textContent="El JSON no parece una respuesta del simulador.";return;}
  RESULT=r;$("swBtnDl").disabled=false;
  $("swStage").classList.remove("locked");$("swOverlay").style.display="none";
  $("swIdxA").textContent=num(r.indice_antes,1);$("swIdxB").textContent=num(r.indice_despues,1);
  var d=num(r.delta_indice,1);var deltaN=Number(r.delta_indice);$("swDelta").textContent=(deltaN>0?"+ ":"")+d+(deltaN>0?" (mejora)":deltaN<0?" (caida)":"");
   $("swDelta").style.color=deltaN>=0?"#0f766e":"#b91c1c";
   $("swIdxB").style.color=deltaN>0?"#0f766e":deltaN<0?"#b91c1c":"";
  $("swLimit").textContent="factor limitante: "+esc(r.factor_limitante);
  $("swPobBase").textContent=num(r.poblacion_base_anio,0);
  $("swBand").textContent=num(r.poblacion_anio_p10,0)+" - "+num(r.poblacion_anio_p90,0);
  $("swFactor").textContent="x"+num(r.factor_m3,4);
  $("swPob").textContent=num(r.poblacion_despues,0);
  $("swPobS").textContent=num(r.poblacion_antes,0)+" -> "+num(r.poblacion_despues,0)+" hab.";
  var dims=[["Demografia","dem"],["Vivienda","viv"],["Servicios","ser"],["Accesibilidad","acc"],["Empleo","emp"]];
  $("swDims").innerHTML=dims.map(function(x){var a=r["dim_"+x[1]+"_antes"],b=r["dim_"+x[1]+"_despues"];
   var col=colMej(a,b);
   return "<div class=\"dim\"><span>"+x[0]+"</span><span class=\"track\"><i class=\"before\" style=\"width:"+num(a)+"%\"></i></span><span class=\"track\"><i class=\"after\" style=\"width:"+num(b)+"%;background:"+col+"\"></i></span><b>"+num(a,1)+" <span style=\"color:"+col+"\">&rarr; "+num(b,1)+"</span></b></div>";
  }).join("");
  $("swRatios").innerHTML="<thead><tr><th>Ratio</th><th class=\"num\">Antes</th><th class=\"num\">Escenario</th></tr></thead><tbody>"
   +fila("Centros de salud por 10.000 hab.",r.salud_10k_antes,r.salud_10k_despues,2,colMej(r.salud_10k_antes,r.salud_10k_despues))
   +fila("Escuelas por 1.000 hab.",r.escuelas_1000_antes,r.escuelas_1000_despues,3,colMej(r.escuelas_1000_antes,r.escuelas_1000_despues))
   +fila("Paradas por 1.000 hab.",r.paradas_1000_antes,r.paradas_1000_despues,3,colMej(r.paradas_1000_antes,r.paradas_1000_despues))
   +fila("Viviendas por 1.000 hab.",r.viv_1000_antes,r.viv_1000_despues,1,colMej(r.viv_1000_antes,r.viv_1000_despues))
   +"</tbody>";
  $("swChoques").innerHTML="<thead><tr><th>Recurso</th><th class=\"num\">Antes</th><th class=\"num\">Escenario</th></tr></thead><tbody>"
   +fila("Poblacion",r.poblacion_antes,r.poblacion_despues,0)
   +fila("Viviendas",r.viviendas_antes,r.viviendas_despues,0)
   +fila("Centros de salud",r.centros_salud_antes,r.centros_salud_despues,0)
   +fila("Escuelas",r.escuelas_antes,r.escuelas_despues,0)
   +fila("Paradas",r.paradas_antes,r.paradas_despues,0)
   +"</tbody>";
  actualizarLimites(r);
 }
 function run(){
  if($("swBtn").disabled)return;
  $("swErr").style.display="none";
  $("swBtn").disabled=true;$("swSpin").style.display="block";
  api("SIMULAR",{x01:$("swCod").value,x02:$("swAnio").value,x03:$("swPop").value||0,x04:$("swViv").value||0,x05:$("swSal").value||0,x06:$("swEsc").value||0,x07:$("swPar").value||0},function(r){
   $("swBtn").disabled=false;$("swSpin").style.display="none";
   render(r);
   if(!BASE){
    BASE=true;
    ["swPop","swViv","swSal","swEsc","swPar"].forEach(function(id){$(id).disabled=false;});
    $("swBtn").textContent="Reejecutar Simulaci\u00f3n";
   }
  });
 }
 function aCsv(o){
  var ks=Object.keys(o),lin=[ks.join(";")];
  lin.push(ks.map(function(k){var v=o[k];if(v==null)return "";v=""+v;return (v.indexOf(";")>=0||v.indexOf("\"")>=0||v.indexOf("\n")>=0)?"\""+v.replace(/"/g,"\"\"")+"\"":v;}).join(";"));
  return "\uFEFF"+lin.join("\n");
 }
 function descargar(fmt){
  if(!RESULT)return;
  var nom="simulador-"+(RESULT.cod||"escenario")+"-"+(RESULT.anio_simulado||"");
  var blob,ext;
  if(fmt==="csv"){blob=new Blob([aCsv(RESULT)],{type:"text/csv;charset=utf-8"});ext="csv";}
  else{blob=new Blob([JSON.stringify(RESULT,null,1)],{type:"application/json"});ext="json";}
  var u=URL.createObjectURL(blob);
  var a=document.createElement("a");
  a.href=u;a.download=nom+"."+ext;
  document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(u);
 }
 $("swFile").addEventListener("change",function(){
  var f=this.files&&this.files[0];if(!f)return;
  var rd=new FileReader();
  rd.onload=function(){
   try{var r=JSON.parse(rd.result);$("swErr").style.display="none";render(r);
    if(!BASE){BASE=true;["swPop","swViv","swSal","swEsc","swPar"].forEach(function(id){$(id).disabled=false;});$("swBtn").textContent="Reejecutar Simulaci\u00f3n";}
   }
   catch(e){$("swErr").style.display="block";$("swErr").textContent="El fichero no es un JSON valido.";}
  };
  rd.readAsText(f);this.value="";
 });
 function boot(){
  var o="",y;for(y=2025;y<=2035;y++){o+="<option value=\""+y+"\">"+y+"</option>";}
  $("swAnio").innerHTML=o;$("swAnio").value="2030";
  api("DATOS",{},function(rows){
   var m=rows||[];
   $("swCod").innerHTML=m.map(function(x){return "<option value=\""+esc(x.cod)+"\">"+esc(x.nombre)+"</option>";}).join("");
   var pre=null;try{pre=JSON.parse(sessionStorage.getItem('pvWiJugada')||"null");}catch(e){pre=null;}
   if(pre&&pre.cod){var sel=$("swCod");var hay=false;Array.prototype.forEach.call(sel.options,function(o){if(o.value===String(pre.cod))hay=true;});
    if(hay){sel.value=String(pre.cod);$("swAnio").value=String(pre.anio||"2030");sessionStorage.removeItem('pvWiJugada');run();}else{sessionStorage.removeItem('pvWiJugada');}}
  });
  ["swPop","swViv","swSal","swEsc","swPar"].forEach(function(id){$(id).addEventListener("input",function(){pintaDif(id,this.value);});});
  $("swBtnDl").addEventListener("click",function(ev){ev.stopPropagation();var m=$("swDlMenu");m.style.display=(m.style.display==="block")?"none":"block";});
  document.querySelectorAll("#swDlMenu button").forEach(function(b){b.addEventListener("click",function(ev){ev.stopPropagation();descargar(b.getAttribute("data-fmt"));$("swDlMenu").style.display="none";});});
  document.addEventListener("click",function(){$("swDlMenu").style.display="none";});
  $("swBtnImp").addEventListener("click",function(){$("swFile").click();});
  $("swBtn").addEventListener("click",run);
  document.addEventListener("keydown",function(e){ if(e.key==="Enter"){ e.preventDefault(); run(); } });
 }
 (function w(){ if(window.apex&&window.apex.server){setTimeout(boot,400);} else {setTimeout(w,100);} })();
})();
</script>
</script>"""
# (referencia para herramientas futuras)
LIMITE_PATH = Path(__file__).resolve().parents[1] / "web" / "limite_madrid.json"

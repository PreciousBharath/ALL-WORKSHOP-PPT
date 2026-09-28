const S=window.APP,KEY=location.pathname.split('/').pop(),HK='hist_'+KEY;
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const inr=v=>v>=100?'₹ '+(v/100).toFixed(2)+' Cr':'₹ '+v.toFixed(2)+' Lakh';
const full=v=>'₹ '+Math.round(v*1e5).toLocaleString('en-IN');
const state={};let charts={},last=null;
// ---------- form ----------
function build(){const box=$('#fields');S.fields.forEach(f=>{const d=document.createElement('div');d.className='field';
 if(f.type==='select'){d.innerHTML=`<label>${f.label}</label><select id="f_${f.name}">${f.options.map(o=>`<option ${o==f.default?'selected':''}>${o}</option>`).join('')}</select>`}
 else{d.innerHTML=`<label>${f.label}<output id="o_${f.name}"></output></label><input type="range" id="f_${f.name}" min="${f.min}" max="${f.max}" step="${f.step}" value="${f.default}">`;}
 if(f.hint)d.innerHTML+=`<small>${f.hint}</small>`;box.appendChild(d);
 const el=$('#f_'+f.name);const upd=()=>{if(f.type!=='select')$('#o_'+f.name).textContent=(+el.value).toLocaleString('en-IN')+(f.unit?' '+f.unit:'')};el.oninput=upd;upd()})}
const vals=()=>Object.fromEntries(S.fields.map(f=>[f.name,$('#f_'+f.name).value]));
function setVals(v){S.fields.forEach(f=>{const el=$('#f_'+f.name);if(v[f.name]!==undefined){el.value=v[f.name];el.dispatchEvent(new Event('input'))}})}
$('#sample').onclick=()=>{setVals(S.sample);run()};
$('#rand').onclick=()=>{const v={};S.fields.forEach(f=>{v[f.name]=f.type==='select'?f.options[Math.floor(Math.random()*f.options.length)]:+(f.min+Math.random()*(f.max-f.min)).toFixed(f.step<1?3:0)});setVals(v);run()};
// ---------- predict ----------
async function post(u,b){const r=await fetch(u+KEY,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});const j=await r.json();if(!r.ok)throw Error(j.error||'Error');return j}
async function run(){const b=$('#go');b.textContent='Thinking…';try{const v=vals(),r=await post('/api/predict/',v);last={v,r};render(r);save(v,r);whatif(v,r)}catch(e){alert(e.message)}b.textContent='🔮 Predict'}
$('#go').onclick=run;
function render(r){$('#empty').hidden=true;const o=$('#out');o.hidden=false;o.style.animation='none';o.offsetHeight;o.style.animation='';
 if(S.task==='clf'){const p=r.prob,col=S.tone==='rain'?css('--a'):p<.25?css('--ok'):p<.5?css('--warn'):css('--bad');
  o.innerHTML=`<svg class="gauge" viewBox="0 0 200 120"><path class="bg" d="M20 100A80 80 0 0 1 180 100" pathLength="100"/><path class="fg" id="arc" d="M20 100A80 80 0 0 1 180 100" pathLength="100" stroke="${col}" stroke-dashoffset="100"/><text x="100" y="92" id="pv">0%</text></svg>
  <div class="verdict">${r.label}</div><div class="center"><span class="badge" style="background:${col}">${r.level}</span></div>
  <ul class="tips">${r.tips.map(t=>`<li>${t}</li>`).join('')}</ul><p class="note">${S.disclaimer}</p>`;
  requestAnimationFrame(()=>$('#arc').setAttribute('stroke-dashoffset',100-p*100));countTo($('#pv'),p*100,1200,v=>v.toFixed(0)+'%')}
 else{o.innerHTML=`<p class="center">Estimated ${S.what}</p><div class="price" id="pv">₹ 0</div><p class="center" id="pf">${full(r.value)}</p>
  <div class="range"><i></i></div><p class="center">Likely range: <b>${inr(r.low)}</b> – <b>${inr(r.high)}</b></p>
  ${r.per_sqft?`<p class="center">≈ ₹ ${Math.round(r.per_sqft).toLocaleString('en-IN')} per sq ft</p>`:''}
  <div class="emi"><h4>💳 EMI planner</h4><div class="fields">
  <div class="field"><label>Down %<output id="e1"></output></label><input type="range" id="dp" min="0" max="80" step="5" value="${S.emi.dp}"></div>
  <div class="field"><label>Rate %<output id="e2"></output></label><input type="range" id="rt" min="6" max="16" step="0.25" value="${S.emi.rate}"></div>
  <div class="field"><label>Years<output id="e3"></output></label><input type="range" id="yr" min="1" max="30" step="1" value="${S.emi.years}"></div></div><big id="emi"></big><p class="center" id="emi2"></p></div>
  <p class="note">${S.disclaimer}</p>`;
  countTo($('#pv'),r.value,1200,v=>inr(v));const calc=()=>{const dp=+$('#dp').value,rt=+$('#rt').value,yr=+$('#yr').value;$('#e1').textContent=dp;$('#e2').textContent=rt;$('#e3').textContent=yr;
   const P=r.value*1e5*(1-dp/100),i=rt/1200,n=yr*12,e=i?P*i*Math.pow(1+i,n)/(Math.pow(1+i,n)-1):P/n;$('#emi').textContent='₹ '+Math.round(e).toLocaleString('en-IN')+' / month';$('#emi2').textContent='Total interest ≈ '+inr((e*n-P)/1e5)};
  ['dp','rt','yr'].forEach(i=>$('#'+i).oninput=calc);calc()}}
// ---------- charts ----------
const gridc=()=>({color:css('--line')}),tick=()=>({color:css('--muted')});
function chart(id,cfg){charts[id]?.destroy();const el=$('#'+id);if(!el)return;cfg.options={...cfg.options,responsive:true,animation:{duration:900},plugins:{legend:{labels:{color:css('--muted')}},...(cfg.options?.plugins||{})}};charts[id]=new Chart(el,cfg)}
async function whatif(v,r){const w=await post('/api/whatif/',v),isC=S.task==='clf';
 chart('whatif',{type:'line',data:{labels:w.x,datasets:[{label:isC?'Probability (%)':'Price (₹ lakh)',data:w.y.map(y=>isC?y*100:y),borderColor:css('--a'),backgroundColor:css('--a')+'33',fill:true,tension:.4,pointRadius:3}]},options:{scales:{x:{title:{display:true,text:w.label,color:css('--muted')},ticks:tick(),grid:gridc()},y:{ticks:tick(),grid:gridc()}}}})}
async function insights(){const d=await (await fetch('/api/insights/'+KEY)).json();window._ins=d;
 chart('imp',{type:'bar',data:{labels:d.importance.map(x=>x[0]),datasets:[{label:'Importance',data:d.importance.map(x=>+(x[1]*100).toFixed(1)),backgroundColor:css('--b')}]},options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:tick(),grid:gridc()},y:{ticks:tick(),grid:{display:false}}}}});
 if(d.task==='clf'){const c=d.confusion,L=d.classes;$('#second').innerHTML=`<table style="width:100%;text-align:center;border-collapse:separate;border-spacing:8px"><tr><td></td><td><small>Pred: ${L[0]}</small></td><td><small>Pred: ${L[1]}</small></td></tr>${c.map((r,i)=>`<tr><td><small>Actual: ${L[i]}</small></td>${r.map((n,j)=>`<td style="border-radius:14px;padding:22px 6px;font:800 1.8rem 'Bricolage Grotesque';background:${i==j?css('--a')+'55':css('--bad')+'33'}">${n}</td>`).join('')}</tr>`).join('')}</table>`}
 else{const mx=Math.max(...d.scatter.map(p=>p[0]));chart('c2',{type:'scatter',data:{datasets:[{label:'Test samples',data:d.scatter.map(p=>({x:p[0],y:p[1]})),backgroundColor:css('--a')},{label:'Perfect fit',type:'line',data:[{x:0,y:0},{x:mx,y:mx}],borderColor:css('--b'),pointRadius:0}]},options:{scales:{x:{title:{display:true,text:'Actual',color:css('--muted')},ticks:tick(),grid:gridc()},y:{title:{display:true,text:'Predicted',color:css('--muted')},ticks:tick(),grid:gridc()}}}})}}
window.onTheme=()=>{insights();last&&(render(last.r),whatif(last.v,last.r))};
// ---------- history ----------
const H=()=>JSON.parse(localStorage.getItem(HK)||'[]');
function save(v,r){const s=S.task==='clf'?`${r.label} (${(r.prob*100).toFixed(0)}%)`:inr(r.value),h=H();h.unshift({t:new Date().toLocaleString('en-IN'),s,v});localStorage.setItem(HK,JSON.stringify(h.slice(0,25)));drawHist()}
function drawHist(){const h=H();$('#hist').innerHTML=h.length?h.map((x,i)=>`<div><span><b>${x.s}</b><br><small>${x.t}</small></span><a data-i="${i}">Reload</a></div>`).join(''):'<p class="center">No predictions yet.</p>';$$('#hist a').forEach(a=>a.onclick=()=>{setVals(H()[+a.dataset.i].v);window.scrollTo({top:0,behavior:'smooth'})})}
$('#clr').onclick=()=>{localStorage.removeItem(HK);drawHist()};
$('#exp').onclick=()=>{const rows=[['time','result',...S.fields.map(f=>f.name)],...H().map(x=>[x.t,x.s,...S.fields.map(f=>x.v[f.name])])];const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([rows.map(r=>r.map(c=>`"${c}"`).join(',')).join('\n')],{type:'text/csv'}));a.download=KEY+'_history.csv';a.click()};
build();drawHist();insights();

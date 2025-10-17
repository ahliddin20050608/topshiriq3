from django.shortcuts import render
from django.http import HttpResponse

def calculator(request):
    return HttpResponse("""
    <!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Calculator — Hisoblagich</title>
<style>
  :root{
    --bg:#f4f7fb; --card:#ffffff; --muted:#6b7280; --accent:#2563eb;
    --btn:#e6eefb; --danger:#ef4444; --glass:rgba(255,255,255,0.6);
    --radius:14px; --shadow: 0 12px 30px rgba(2,6,23,0.08);
  }
  *{box-sizing:border-box}
  body{
    margin:0; font-family:Inter, ui-sans-serif, system-ui, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    background: linear-gradient(180deg,#eef6ff 0%, #fbfdff 100%); color:#08122a; min-height:100vh; display:flex;align-items:center;justify-content:center;padding:28px;
  }

  .wrap{
    width:100%; max-width:980px;
    display:grid; grid-template-columns: 1fr 360px; gap:24px;
    align-items:start;
  }
  @media (max-width:900px){
    .wrap{grid-template-columns:1fr; padding:0 12px}
  }

  /* Left - Intro + history */
  .panel{
    background:var(--card); border-radius:var(--radius); box-shadow:var(--shadow); padding:20px;
  }
  .brand{display:flex;gap:12px;align-items:center;margin-bottom:12px}
  .logo{width:54px;height:54px;border-radius:12px;background:linear-gradient(135deg,var(--accent),#06b6d4);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:18px}
  h1{margin:0;font-size:20px}
  p.lead{margin:8px 0 16px;color:var(--muted);font-size:14px}

  .history{
    margin-top:8px; max-height:420px; overflow:auto; padding:10px; border-radius:10px; background:linear-gradient(180deg, #fbfdff, #ffffff);
    border:1px solid #eef4ff;
  }
  .hist-empty{color:var(--muted);text-align:center;padding:28px 6px}
  .hist-item{display:flex;justify-content:space-between;padding:10px;border-radius:8px;margin-bottom:8px;background:#fbfdff;border:1px solid #f1f7ff}
  .hist-item .expr{color:#334155;font-weight:600}
  .hist-item .res{color:var(--accent);font-weight:800}

  /* Right - Calculator */
  .calc{
    background: linear-gradient(180deg,#ffffff,#fbfdff); border-radius:var(--radius); box-shadow:var(--shadow);
    padding:18px; width:100%;
  }

  .display{
    background:var(--glass); border-radius:12px; padding:14px; margin-bottom:12px; position:relative; overflow:hidden;
    border:1px solid rgba(37,99,235,0.08);
  }
  .toprow{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:6px}
  .mode{
    display:flex;gap:8px;align-items:center;font-size:13px;color:var(--muted)
  }
  .small{font-size:13px;color:var(--muted)}
  .value{font-size:28px;font-weight:700;color:#061226; text-align:right; word-break:break-all}
  .subvalue{font-size:13px;color:var(--muted); text-align:right; margin-top:6px}

  .keys{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
  button.k{padding:14px;border-radius:10px;border:0;background:var(--btn);font-weight:700;cursor:pointer;box-shadow:inset 0 -2px 0 rgba(0,0,0,0.02)}
  button.k:active{transform:translateY(1px)}
  .op{background:linear-gradient(90deg,var(--accent),#06b6d4);color:#fff}
  .wide{grid-column:span 2}
  .danger{background:var(--danger);color:#fff}
  .muted{background:#fff;border:1px solid #eef4ff}

  .footer-note{margin-top:12px;font-size:13px;color:var(--muted);text-align:center}
  /* focus for accessibility */
  button.k:focus{outline:3px solid rgba(37,99,235,0.12)}
</style>
</head>
<body>
  <div class="wrap">
    <div class="panel">
      <div class="brand">
        <div class="logo">CALC</div>
        <div>
          <h1>Smart Calculator</h1>
          <div class="small">Tez va ishonchli hisoblashlar — oddiy interfeys</div>
        </div>
      </div>

      <p class="lead">Quyida hisoblash tarixini va soʻnggi natijalarni koʻrishingiz mumkin. Klaviatura bilan ham ishlaydi (0-9, + - * / . Enter = Backspace).</p>

      <div class="history" id="history">
        <div class="hist-empty" id="histEmpty">Hech qanday hisob yo'q — hisobni boshlang.</div>
      </div>
    </div>

    <div class="calc" role="application" aria-label="Calculator">
      <div class="display" aria-live="polite">
        <div class="toprow">
          <div class="mode"><span id="memIndicator" style="display:none;background:#fff;color:var(--accent);padding:4px 8px;border-radius:8px;font-weight:700">M</span></div>
          <div class="small">Scientific-lite</div>
        </div>

        <div id="expr" class="subvalue" aria-hidden="true"></div>
        <div id="display" class="value">0</div>
        <div id="preview" class="subvalue"></div>
      </div>

      <div class="keys" id="keys">
        <!-- Row 1 -->
        <button class="k muted" data-action="clear">AC</button>
        <button class="k muted" data-action="back">⌫</button>
        <button class="k muted" data-action="percent">%</button>
        <button class="k op" data-action="op" data-value="/">÷</button>

        <!-- Row 2 -->
        <button class="k" data-value="7">7</button>
        <button class="k" data-value="8">8</button>
        <button class="k" data-value="9">9</button>
        <button class="k op" data-action="op" data-value="*">×</button>

        <!-- Row 3 -->
        <button class="k" data-value="4">4</button>
        <button class="k" data-value="5">5</button>
        <button class="k" data-value="6">6</button>
        <button class="k op" data-action="op" data-value="-">−</button>

        <!-- Row 4 -->
        <button class="k" data-value="1">1</button>
        <button class="k" data-value="2">2</button>
        <button class="k" data-value="3">3</button>
        <button class="k op" data-action="op" data-value="+">+</button>

        <!-- Row 5 -->
        <button class="k wide" data-value="0">0</button>
        <button class="k" data-value=".">.</button>
        <button class="k danger" data-action="equals">=</button>
      </div>

      <div class="footer-note">Maslahat: Katta ifodalar uchun (parenthesis) klaviaturadan `(` va `)` ni ishlating.</div>
    </div>
  </div>

<script>
(() => {
  const displayEl = document.getElementById('display');
  const exprEl = document.getElementById('expr');
  const previewEl = document.getElementById('preview');
  const historyEl = document.getElementById('history');
  const histEmpty = document.getElementById('histEmpty');

  let expr = '';     // raw expression shown above
  let lastResult = null;
  let history = [];

  // helpers
  function updateUI(){
    exprEl.textContent = expr || '';
    displayEl.textContent = expr === '' ? '0' : expr;
    previewEl.textContent = ''; // reserved for future
    renderHistory();
  }

  function sanitizeExpression(s){
    // allow digits, operators, parentheses, dot and spaces
    // also convert unicode operators to JS ones
    s = s.replace(/÷/g, '/').replace(/×/g, '*').replace(/−/g,'-');
    // remove any disallowed characters
    s = s.replace(/[^0-9+\-*/().% ]/g, '');
    return s;
  }

  function evaluateExpression(s){
    s = s.replace(/%/g, '/100'); // simple percent handling
    s = sanitizeExpression(s);
    if(!s) return 0;
    try{
      // Use Function constructor instead of eval (slightly safer)
      // still: don't evaluate untrusted input on public servers
      const fn = new Function('return (' + s + ')');
      const res = fn();
      if(typeof res === 'number' && !Number.isFinite(res)) throw new Error('NaN or Infinite');
      return res;
    } catch(e){
      return 'Error';
    }
  }

  function pushHistory(expression, result){
    const item = { expression, result, time: new Date().toISOString() };
    history.unshift(item);
    if(history.length > 30) history.pop();
  }

  function renderHistory(){
    // Clear previous history except empty placeholder
    historyEl.querySelectorAll('.hist-item').forEach(n=>n.remove());
    if(history.length === 0){
      histEmpty.style.display = 'block';
      return;
    }
    histEmpty.style.display = 'none';
    history.forEach(h=>{
      const node = document.createElement('div');
      node.className = 'hist-item';
      node.innerHTML = `<div class="expr">${h.expression}</div><div class="res">${formatNumber(h.result)}</div>`;
      node.addEventListener('click', ()=> {
        expr = h.expression;
        updateUI();
      });
      historyEl.appendChild(node);
    });
  }

  function formatNumber(n){
    if(n === 'Error') return 'Error';
    if(typeof n === 'number') {
      // show integer without decimals where possible
      if(Number.isInteger(n)) return n.toLocaleString('ru-RU');
      return n.toLocaleString('ru-RU', {maximumFractionDigits:10});
    }
    return String(n);
  }

  // button handlers
  document.getElementById('keys').addEventListener('click', (e)=>{
    const btn = e.target.closest('button.k');
    if(!btn) return;
    const val = btn.getAttribute('data-value');
    const action = btn.getAttribute('data-action');

    if(action === 'clear'){
      expr = '';
      lastResult = null;
      updateUI();
      return;
    }
    if(action === 'back'){
      expr = expr.slice(0, -1);
      updateUI();
      return;
    }
    if(action === 'percent'){
      expr += '%';
      updateUI();
      return;
    }
    if(action === 'op'){
      const op = btn.getAttribute('data-value');
      expr += op;
      updateUI();
      return;
    }
    if(action === 'equals'){
      const sanitized = sanitizeExpression(expr);
      const result = evaluateExpression(sanitized);
      if(result === 'Error'){
        displayEl.textContent = 'Error';
      } else {
        pushHistory(expr || '0', result);
        lastResult = result;
        displayEl.textContent = formatNumber(result);
        expr = String(result);
      }
      updateUI();
      return;
    }

    // default: numeric or dot
    if(val){
      // avoid multiple dots in a single number segment
      if(val === '.'){
        // find last token after operator
        const lastToken = expr.split(/[\+\-\*\/\(\)]/).pop();
        if(lastToken.includes('.')) return; // ignore second dot
        if(lastToken === '') expr += '0'; // start decimal with 0
      }
      expr += val;
      updateUI();
    }
  });

  // keyboard support
  window.addEventListener('keydown', (e)=>{
    const key = e.key;
    if((/^[0-9]$/).test(key) || key === '.' ) {
      // numeric
      const simulated = document.querySelector(`button.k[data-value="${key}"]`);
      if(simulated) simulated.click();
      return;
    }
    if(key === 'Enter' || key === '='){
      e.preventDefault();
      document.querySelector('button.k[data-action="equals"]').click();
      return;
    }
    if(key === 'Backspace'){
      document.querySelector('button.k[data-action="back"]').click();
      return;
    }
    if(key === 'Escape'){
      document.querySelector('button.k[data-action="clear"]').click();
      return;
    }
    if(key === '+' || key === '-' || key === '*' || key === '/'){
      // operators
      const btn = document.querySelector(`button.k[data-action="op"][data-value="${key}"]`);
      if(btn){ btn.click(); e.preventDefault(); }
      return;
    }
    if(key === '%'){
      document.querySelector('button.k[data-action="percent"]').click();
      return;
    }
    if(key === '(' || key === ')'){
      expr += key;
      updateUI();
      return;
    }
  });

  // initial render
  updateUI();

})();
</script>
</body>
</html>

""")

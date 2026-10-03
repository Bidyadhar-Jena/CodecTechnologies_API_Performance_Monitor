"""Runnable sample API with a small performance-monitoring dashboard."""
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from monitor import PerformanceMonitor

app = FastAPI(title="API Performance Monitor", version="1.0.0")
monitor = PerformanceMonitor()


@app.middleware("http")
async def collect_performance_metrics(request, call_next):
    path = request.url.path
    should_record = path not in {"/metrics", "/dashboard"}
    started = __import__("time").perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        elapsed_ms = (__import__("time").perf_counter() - started) * 1000
        if should_record:
            monitor.record(request.method, path, status_code, elapsed_ms)


@app.get("/")
async def home():
    return {"message": "API Performance Monitor is running", "docs": "/docs", "dashboard": "/dashboard"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(0.35)
    return {"message": "This endpoint intentionally responds slowly."}


@app.get("/error")
async def error_endpoint():
    raise HTTPException(status_code=500, detail="Intentional test error")


@app.get("/metrics")
async def get_metrics():
    """Return the current in-memory performance summary as JSON."""
    return monitor.snapshot()


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse("""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>API Performance Monitor</title>
<style>
body{font-family:system-ui,sans-serif;max-width:1000px;margin:36px auto;padding:0 16px;color:#172033}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.card{border:1px solid #d8deea;border-radius:12px;padding:16px;background:#f8faff}
.value{font-size:1.7rem;font-weight:700}table{border-collapse:collapse;width:100%;margin-top:20px}
th,td{text-align:left;border-bottom:1px solid #ddd;padding:10px}button{padding:9px 14px;cursor:pointer}
small{color:#596579}
</style></head><body>
<h1>API Performance Monitor</h1>
<p><small>Demo metrics are held in memory and reset when the server restarts.</small></p>
<button onclick="loadMetrics()">Refresh metrics</button>
<div class="cards" id="cards"></div>
<h2>Endpoint breakdown</h2>
<table><thead><tr><th>Endpoint</th><th>Requests</th><th>Errors</th><th>Average (ms)</th><th>P95 (ms)</th></tr></thead>
<tbody id="rows"></tbody></table>
<script>
async function loadMetrics(){
 const r=await fetch('/metrics'); const m=await r.json();
 const items=[
  ['Total requests',m.total_requests],['Errors',m.error_count],
  ['Error rate',m.error_rate_percent+'%'],['Average response',m.average_response_time_ms+' ms'],
  ['P95 response',m.p95_response_time_ms+' ms']
 ];
 document.getElementById('cards').innerHTML=items.map(x=>`<div class="card"><div>${x[0]}</div><div class="value">${x[1]}</div></div>`).join('');
 document.getElementById('rows').innerHTML=m.endpoints.map(e=>`<tr><td>${e.endpoint}</td><td>${e.requests}</td><td>${e.errors}</td><td>${e.average_response_time_ms}</td><td>${e.p95_response_time_ms}</td></tr>`).join('') || '<tr><td colspan="5">No requests recorded yet. Visit /health or /slow first.</td></tr>';
}
loadMetrics();
</script></body></html>
""")

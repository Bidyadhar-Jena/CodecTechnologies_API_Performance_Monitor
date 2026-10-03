# API Performance Monitor

A runnable Python/FastAPI demo that tracks API request counts, server errors, and response-time statistics, with a lightweight browser dashboard.

> The original `Main/` directory contains Apitally/OpenTelemetry framework integration code. The added `app.py` and `monitor.py` provide a separate, local demo that can be run independently. The demo does not send telemetry to an external service.

## Features

- Request count and server-error count
- Error-rate percentage
- Average and p95 response time
- Per-endpoint request and latency breakdown
- Browser dashboard at `/dashboard`
- JSON metrics endpoint at `/metrics`
- Sample health, slow, and intentional-error endpoints
- Basic automated tests

## Requirements

- Python 3.10 or later
- pip

## Run locally

```bash
python -m venv .venv
```

Activate the environment:

**Windows**
```powershell
.venv\\Scripts\\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app:app --reload
```

Open these URLs:

- API home: http://127.0.0.1:8000/
- Interactive API docs: http://127.0.0.1:8000/docs
- Dashboard: http://127.0.0.1:8000/dashboard
- JSON metrics: http://127.0.0.1:8000/metrics
- Health check: http://127.0.0.1:8000/health
- Slow sample endpoint: http://127.0.0.1:8000/slow
- Intentional error test: http://127.0.0.1:8000/error

Visit `/health`, `/slow`, and `/error`, then refresh the dashboard to see metrics.

## Run tests

```bash
pytest -v
```

## Important limitations

- Metrics are stored in memory and reset when the app restarts.
- This is a learning/demo implementation, not production monitoring infrastructure.
- Endpoint names currently use request paths, so dynamic IDs may appear as separate endpoint labels.
- The demo does not include authentication, persistent storage, alerting, or multi-process aggregation.
- The original `Main/` integration modules depend on the Apitally package internals and their corresponding OpenTelemetry dependencies. They are separate from this demo app.

## Security

Do not expose this demo dashboard or metrics endpoint publicly without access controls. Avoid collecting secrets, authorization headers, or personal data in monitoring output.

## License

See [LICENSE](LICENSE) for the license included with the original project.

## Author

Bidyadhar Jena

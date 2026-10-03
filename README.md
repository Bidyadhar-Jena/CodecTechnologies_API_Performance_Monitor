# API Performance Monitor

A Python-based API monitoring and instrumentation project designed to
help track API behavior across popular Python web frameworks. The code
in `Main/` contains framework-specific integrations and OpenTelemetry
helpers for collecting request traces, recording exceptions, and
identifying API routes.

## Features

-   **Multiple framework integrations:** includes modules for
    BlackSheep, Django, Django Ninja, Django REST Framework, FastAPI,
    Flask, Litestar, and Starlette.
-   **OpenTelemetry tracing:** provides helpers for tracing synchronous
    and asynchronous functions and creating custom spans.
-   **Error capture:** includes integration hooks for recording
    exceptions and server errors.
-   **Route discovery:** framework modules include logic for identifying
    API paths and HTTP methods.
-   **Database and client instrumentation helpers:** `Main/otel.py`
    includes optional helpers for instrumenting supported database
    clients and HTTP libraries.

> **Note:** This repository contains monitoring/instrumentation
> integration code, not a complete standalone dashboard or API server.
> The modules import `apitally` shared components and OpenTelemetry
> packages, so they need the corresponding package dependencies and
> configuration to run.

## Project Structure

``` text
.
├── Main/
│   ├── __init__.py
│   ├── blacksheep.py
│   ├── django.py
│   ├── django_ninja.py
│   ├── django_rest_framework.py
│   ├── fastapi.py
│   ├── flask.py
│   ├── litestar.py
│   ├── otel.py
│   └── starlette.py
├── Makefile
├── LICENSE
└── README.md
```

## Technologies

-   Python
-   OpenTelemetry
-   Python web frameworks (depending on the integration used)
-   `uv`, Ruff, and pytest for the development commands defined in the
    `Makefile`

## Getting Started

### 1. Get the repository

``` bash
git clone <your-repository-url>
cd <repository-folder>
```

Replace the placeholders with your repository URL and local folder name.

### 2. Install the project dependencies

Install the dependencies required by your chosen framework integration,
including the appropriate OpenTelemetry instrumentation packages and the
`apitally` components referenced by the source code.

This ZIP does not include a dependency manifest such as `pyproject.toml`
or `requirements.txt`, so the exact installation command depends on how
you intend to package or run the code.

### 3. Configure the integration

Choose the module that matches your Python web framework and follow the
relevant framework's setup instructions. The integration modules contain
references to the Apitally setup guides and SDK documentation:

-   [Apitally setup guides](https://docs.apitally.io/setup-guides)
-   [Apitally Python SDK
    reference](https://docs.apitally.io/sdk-reference/python)
-   [OpenTelemetry Python
    documentation](https://opentelemetry.io/docs/languages/python/)

Do not commit API tokens, write tokens, or other secrets to source
control. Store secrets in environment variables or a secrets manager.

## Development Commands

The included `Makefile` defines these commands, assuming the required
development dependencies and project configuration are available:

``` bash
make format
make check
make test
make test-coverage
```

-   `make format` runs Ruff import sorting and formatting.
-   `make check` runs Ruff checks, checks formatting, runs `ty`, and
    verifies the `uv` lockfile.
-   `make test` runs pytest.
-   `make test-coverage` runs pytest with coverage reporting.

The ZIP provided for this README does not include a `tests/` directory
or the project configuration/lock files, so these commands may require
additional files from the full project.

## Security and Privacy

Before enabling request or response capture in a real application,
review the monitoring configuration and ensure sensitive data such as
authorization headers, credentials, personal information, and secrets
are excluded or masked.

## License

See the [`LICENSE`](LICENSE) file for the license terms.

## Author

**Bidyadhar Jena**

This README describes the source files included in the provided project
archive. Update the setup instructions and repository links after adding
the project's dependency configuration and deployment details.

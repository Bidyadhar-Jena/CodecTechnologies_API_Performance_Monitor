"""Lightweight in-memory API performance monitoring middleware for the demo app."""
from collections import defaultdict
from threading import Lock
from time import perf_counter
from typing import Any


class PerformanceMonitor:
    """Collect request counts, errors, and response-time statistics in memory."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._total_requests = 0
        self._error_count = 0
        self._durations: list[float] = []
        self._endpoints: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"requests": 0, "errors": 0, "durations_ms": []}
        )

    def record(self, method: str, path: str, status_code: int, duration_ms: float) -> None:
        key = f"{method.upper()} {path}"
        with self._lock:
            self._total_requests += 1
            self._durations.append(duration_ms)
            endpoint = self._endpoints[key]
            endpoint["requests"] += 1
            endpoint["durations_ms"].append(duration_ms)
            if status_code >= 500:
                self._error_count += 1
                endpoint["errors"] += 1

    @staticmethod
    def _percentile(values: list[float], percentile: float) -> float:
        if not values:
            return 0.0
        ordered = sorted(values)
        index = min(len(ordered) - 1, max(0, int((percentile / 100) * len(ordered) + 0.999) - 1))
        return round(ordered[index], 2)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            durations = list(self._durations)
            endpoints_copy = {
                name: {
                    "requests": item["requests"],
                    "errors": item["errors"],
                    "durations_ms": list(item["durations_ms"]),
                }
                for name, item in self._endpoints.items()
            }
            total = self._total_requests
            errors = self._error_count

        endpoints = []
        for name, item in sorted(endpoints_copy.items()):
            samples = item["durations_ms"]
            endpoints.append({
                "endpoint": name,
                "requests": item["requests"],
                "errors": item["errors"],
                "average_response_time_ms": round(sum(samples) / len(samples), 2) if samples else 0.0,
                "p95_response_time_ms": self._percentile(samples, 95),
            })

        return {
            "total_requests": total,
            "error_count": errors,
            "error_rate_percent": round((errors / total) * 100, 2) if total else 0.0,
            "average_response_time_ms": round(sum(durations) / len(durations), 2) if durations else 0.0,
            "p95_response_time_ms": self._percentile(durations, 95),
            "endpoints": endpoints,
        }

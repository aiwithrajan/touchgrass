import time
from typing import Dict, Any, List
from backend.app.config import settings

class SentryAgentTracer:
    def __init__(self):
        self.traces: List[Dict[str, Any]] = []
        if settings.SENTRY_DSN and not settings.OFFLINE_MODE:
            try:
                import sentry_sdk
                sentry_sdk.init(
                    dsn=settings.SENTRY_DSN,
                    traces_sample_rate=1.0,
                    profiles_sample_rate=1.0
                )
                print("[SentryService] Initialized Sentry SDK.")
            except Exception as e:
                print(f"[SentryService] Sentry SDK init error: {e}")

    def trace_agent_execution(self, step_name: str, duration_ms: float, metadata: Dict[str, Any]):
        """Records agent span for observability inspection."""
        entry = {
            "step": step_name,
            "duration_ms": round(duration_ms, 2),
            "timestamp": time.time(),
            "metadata": metadata
        }
        self.traces.append(entry)
        if len(self.traces) > 50:
            self.traces.pop(0)

    def get_recent_traces(self) -> List[Dict[str, Any]]:
        return self.traces

sentry_tracer = SentryAgentTracer()

from backend.models.events import SentinelEvent, EventState

class CorrelationEngine:
    """
    Groups distinct events into a larger pattern (e.g. multiple failed logins -> Brute Force).
    """
    def correlate(self, event: SentinelEvent) -> SentinelEvent:
        if event.state == EventState.DETECTED:
            # Stub correlation: just pass it through
            event.state = EventState.CORRELATED
        return event

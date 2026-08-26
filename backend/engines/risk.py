from backend.models.events import SentinelEvent, Severity

class RiskEngine:
    """
    Assigns a dynamic risk score and severity based on IOCs, asset value, and event context.
    """
    def evaluate(self, event: SentinelEvent) -> SentinelEvent:
        if event.state.value in ["DETECTED", "CORRELATED"]:
            # Very basic risk scoring
            event.risk_score = 50
            event.severity = Severity.HIGH
        return event

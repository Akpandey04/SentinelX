from src.models.events import SentinelEvent, Severity

class RiskEngine:
    """
    Assigns a dynamic risk score and severity based on IOCs, asset value, and event context.
    """
    def evaluate(self, event: SentinelEvent) -> SentinelEvent:
        if event.state.value in ["DETECTED", "CORRELATED"]:
            
            if event.event_type == "BRUTE_FORCE_SUCCESS":
                event.risk_score = 95
                event.severity = Severity.CRITICAL
            elif event.event_type == "IMPOSSIBLE_TRAVEL":
                event.risk_score = 90
                event.severity = Severity.CRITICAL
            elif event.event_type == "PASSWORD_SPRAY":
                event.risk_score = 80
                event.severity = Severity.HIGH
            elif event.event_type == "OFF_HOUR_LOGIN":
                event.risk_score = 40
                event.severity = Severity.MEDIUM
            else:
                # Default for SSH_LOGIN_FAILED and others
                event.risk_score = 50
                event.severity = Severity.HIGH
        return event

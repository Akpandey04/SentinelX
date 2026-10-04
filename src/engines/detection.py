from src.models.events import SentinelEvent, EventState

class DetectionEngine:
    """
    Evaluates normalized events against YAML detection rules.
    """
    def __init__(self, rules_dir: str = "config/rules/"):
        self.rules_dir = rules_dir
        self.rules = self._load_rules()

    def _load_rules(self):
        # In a real implementation, parse YAML rules here.
        # For phase 1 stub, we use hardcoded simple rules.
        return []

    def detect(self, event: SentinelEvent) -> SentinelEvent:
        # Very simple stub detection for SSH failures
        if event.event_type == "SSH_LOGIN_FAILED":
            event.state = EventState.DETECTED
            event.tags.append("AuthFailure")
            
        elif event.event_type == "IMPOSSIBLE_TRAVEL":
            event.state = EventState.DETECTED
            event.tags.extend(["SuspiciousLogin", "ImpossibleTravel"])
            
        elif event.event_type == "PASSWORD_SPRAY":
            event.state = EventState.DETECTED
            event.tags.extend(["AuthFailure", "PasswordSpray"])
            
        elif event.event_type == "OFF_HOUR_LOGIN":
            event.state = EventState.DETECTED
            event.tags.extend(["AnomalousActivity", "OffHour"])
            
        elif event.event_type == "BRUTE_FORCE_SUCCESS":
            event.state = EventState.DETECTED
            event.tags.extend(["CompromisedAccount", "BruteForceSuccess"])
            
        return event

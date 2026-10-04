from src.models.events import SentinelEvent, EventState
from src.models.incidents import SentinelIncident
from src.database.storage_backend import StorageBackend

class IncidentEngine:
    """
    Maintains stateful incidents. Groups events into active incidents.
    """
    def __init__(self, storage: StorageBackend):
        self.storage = storage

    def process(self, event: SentinelEvent) -> SentinelEvent:
        if event.state.value in ["DETECTED", "CORRELATED"] and event.severity:
            
            attacker_ip = event.source_ip
            target_asset = event.destination_ip
            
            if attacker_ip and target_asset:
                active_incident = self.storage.get_active_incident(attacker_ip, target_asset)
                
                if active_incident:
                    # Update existing incident
                    active_incident.related_events.append(event.event_id)
                    # Increase risk score logic
                    active_incident.risk_score = max(active_incident.risk_score, event.risk_score)
                    self.storage.save_incident(active_incident)
                    event.state = EventState.INCIDENT
                    event.metadata["incident_id"] = active_incident.incident_id
                else:
                    # Create new incident
                    new_incident = SentinelIncident(
                        title=f"Suspicious Activity from {attacker_ip}",
                        description=f"Initial detection: {event.event_type}",
                        severity=event.severity,
                        risk_score=event.risk_score,
                        related_events=[event.event_id],
                        target_asset=target_asset,
                        attacker_ip=attacker_ip
                    )
                    self.storage.save_incident(new_incident)
                    event.state = EventState.INCIDENT
                    event.metadata["incident_id"] = new_incident.incident_id
                    
        return event

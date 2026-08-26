from elasticsearch import Elasticsearch
from typing import List, Optional
from backend.database.storage_backend import StorageBackend
from backend.models.events import SentinelEvent
from backend.models.incidents import SentinelIncident, IncidentStatus

class ElasticsearchAdapter(StorageBackend):
    def __init__(self, hosts=["http://localhost:9200"], index_prefix="sentinelx"):
        self.es = Elasticsearch(hosts)
        self.events_index = f"{index_prefix}-events"
        self.incidents_index = f"{index_prefix}-incidents"
        self._init_indices()

    def _init_indices(self):
        try:
            if not self.es.indices.exists(index=self.events_index):
                self.es.indices.create(index=self.events_index)
            if not self.es.indices.exists(index=self.incidents_index):
                self.es.indices.create(index=self.incidents_index)
        except Exception as e:
            print(f"Elasticsearch connection failed (this is expected if ES is not running): {e}")

    def save_event(self, event: SentinelEvent) -> None:
        try:
            self.es.index(index=self.events_index, id=event.event_id, document=event.dict())
        except Exception as e:
            pass # Silent fail if ES is down for this prototype

    def get_events(self, limit: int = 100) -> List[SentinelEvent]:
        # Stub implementation
        return []

    def save_incident(self, incident: SentinelIncident) -> None:
        try:
            self.es.index(index=self.incidents_index, id=incident.incident_id, document=incident.dict())
        except Exception as e:
            pass

    def get_active_incident(self, attacker_ip: str, target_asset: str) -> Optional[SentinelIncident]:
        # Stub implementation
        return None

    def get_incidents(self, limit: int = 100) -> List[SentinelIncident]:
        return []

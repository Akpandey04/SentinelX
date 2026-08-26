from abc import ABC, abstractmethod
from typing import List, Optional
from backend.models.events import SentinelEvent
from backend.models.incidents import SentinelIncident

class StorageBackend(ABC):
    """
    Abstract interface for SentinelX storage backends.
    Allows easy migration from SQLite to Elasticsearch/Postgres.
    """
    
    @abstractmethod
    def save_event(self, event: SentinelEvent) -> None:
        pass
        
    @abstractmethod
    def get_events(self, limit: int = 100) -> List[SentinelEvent]:
        pass
        
    @abstractmethod
    def save_incident(self, incident: SentinelIncident) -> None:
        pass
        
    @abstractmethod
    def get_active_incident(self, attacker_ip: str, target_asset: str) -> Optional[SentinelIncident]:
        pass
        
    @abstractmethod
    def get_incidents(self, limit: int = 100) -> List[SentinelIncident]:
        pass

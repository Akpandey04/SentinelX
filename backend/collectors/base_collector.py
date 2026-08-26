from abc import ABC, abstractmethod
import uuid
from backend.core.event_bus import EventBus

class BaseCollector(ABC):
    """
    Interface for all SentinelX Log Collectors.
    """
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.collector_id = f"COL-{uuid.uuid4().hex[:8].upper()}"

    @abstractmethod
    async def collect(self):
        """
        Continuously fetch/generate data and publish to event_bus.
        e.g., await self.event_bus.publish({"raw_log": "...", "collector_id": self.collector_id})
        """
        pass

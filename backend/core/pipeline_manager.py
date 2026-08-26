import asyncio
from backend.models.events import EventState
from backend.core.event_bus import EventBus
from backend.core.normalizer import Normalizer
from backend.engines.detection import DetectionEngine
from backend.engines.correlation import CorrelationEngine
from backend.engines.risk import RiskEngine
from backend.engines.incident import IncidentEngine
from backend.notifications.engine import NotificationEngine
from backend.database.storage_backend import StorageBackend

class PipelineManager:
    """
    Service Layer / Orchestrator for SentinelX.
    Reads from the Event Bus and pushes data through the pipeline.
    """
    def __init__(self, event_bus: EventBus, storage: StorageBackend):
        self.event_bus = event_bus
        self.storage = storage
        
        self.normalizer = Normalizer()
        self.detection = DetectionEngine()
        self.correlation = CorrelationEngine()
        self.risk = RiskEngine()
        self.incident = IncidentEngine(self.storage)
        self.notifier = NotificationEngine()

    async def run(self):
        print("Pipeline Manager started. Listening for events...")
        while True:
            raw_event = await self.event_bus.subscribe()
            try:
                # 1. Normalize
                event = self.normalizer.normalize(raw_event)
                
                # 2. Detection
                event = self.detection.detect(event)
                
                # 3. Correlation
                event = self.correlation.correlate(event)
                
                # 4. Risk Scoring
                event = self.risk.evaluate(event)
                
                # 5. Incident Generation (Stateful)
                event = self.incident.process(event)
                
                # 6. Storage (Save event after all processing)
                self.storage.save_event(event)
                
                # 7. Notify
                if event.state == EventState.INCIDENT:
                    self.notifier.notify(event)
                
            except Exception as e:
                print(f"Error processing event: {e}")
            finally:
                self.event_bus.task_done()

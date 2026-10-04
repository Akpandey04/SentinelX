import asyncio
from typing import Any

class EventBus:
    """
    Central message bus for SentinelX.
    Decouples collectors from the pipeline manager.
    Can be replaced with Kafka/RabbitMQ in the future.
    """
    def __init__(self):
        self._queue = asyncio.Queue()
        
    async def publish(self, raw_event: dict):
        """Publish a raw event dict to the bus."""
        await self._queue.put(raw_event)
        
    async def subscribe(self) -> dict:
        """Block and wait for the next raw event."""
        return await self._queue.get()
        
    def task_done(self):
        self._queue.task_done()

from src.models.events import SentinelEvent, EventState

class Normalizer:
    """
    Takes a raw event dictionary and normalizes it into a SentinelEvent.
    """
    def normalize(self, raw_event: dict) -> SentinelEvent:
        event = SentinelEvent(
            raw_message=raw_event.get("raw_message", ""),
            collector_id=raw_event.get("collector_id", "UNKNOWN"),
            timestamp=raw_event.get("timestamp"),
            source_ip=raw_event.get("source_ip"),
            destination_ip=raw_event.get("destination_ip"),
            event_type=raw_event.get("event_type", "UNKNOWN"),
            state=EventState.NORMALIZED
        )
        # We could add more complex parsing logic here for specific log types.
        # E.g., regex matching on raw_message if event_type is unknown.
        return event

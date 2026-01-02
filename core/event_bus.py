import logging
from core.events import Event
logger = logging.getLogger("engine.event_bus")


class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logger.info(
            "SUBSCRIBER_ADDED | event=%s total=%d", 
            event_type, len(self.subscribers[event_type])
        )

    async def publish(self, event: Event):
        logger.info("EVENT_PUBLISHED | %s", event)
        for callback in self.subscribers.get(event.type, []):
            try:
                await callback(event)
            except Exception:
                # Critical: isolate failure
                logger.exception(
                    "SUBSCRIBER_FAILED | subscriber=%s",
                    getattr(callback, "__name__", "unknown")
                )

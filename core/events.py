from enum import Enum
from dataclasses import dataclass

class EventType(Enum):
    MARKET_TICK = "MARKET_TICK"
    ORDER = "ORDER"
    SHUTDOWN = "SHUTDOWN"


@dataclass
class Event:
    type: EventType
    data: dict

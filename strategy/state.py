from enum import Enum

class StrategyState(Enum):
    CREATED = "CREATED"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    FORCE_CLOSED = "FORCE_CLOSED"

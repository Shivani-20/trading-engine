from core.events import EventType
import logging

from strategy.runtime import StrategyRuntime
logger = logging.getLogger("strategy.manager")

class StrategyManager:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.strategies = []

    def add_strategy(self, strategy: StrategyRuntime):
        self.strategies.append(strategy)
        self.event_bus.subscribe(
            EventType.MARKET_TICK,
            strategy.on_tick
        )
    
    async def shutdown_all(self, _):
        logger.info("Market Closed — Initiating Graceful Shutdown")
        for s in self.strategies:
            await s.shutdown()




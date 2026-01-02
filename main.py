import asyncio
import json

from core.event_bus import EventBus
from market.order_executor import Executor
from market.dummy_stocks_data_generator import Generator
from strategy.runtime import StrategyRuntime
from strategy.manager import StrategyManager
from core.events import EventType
from core.health import health_check
import sys
import json
from strategy.state import StrategyState
import logging

logging.basicConfig(
    level=logging.INFO,
    force=True,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%H:%M:%S"
)

def print_final_summary(manager: StrategyManager):
    total = len(manager.strategies)
    closed = 0
    force_closed = 0
    failed = 0

    for s in manager.strategies:
        if s.state == StrategyState.CLOSED:
            closed += 1
        elif s.state == StrategyState.FORCE_CLOSED:
            force_closed += 1
            failed += 1

    logging.info("\n===== FINAL SUMMARY =====")
    logging.info(f"Total strategies        : {total}")
    logging.info(f"Successfully completed  : {closed}")
    logging.info(f"Force-closed            : {force_closed}")
    logging.info(f"Failed strategies       : {failed}")
    logging.info("=========================\n")

async def main():

    if "--health" in sys.argv:
        with open("test_strategies.json") as f:
            strategies = json.load(f)

        # At startup, no failures yet
        snapshot = {
            "total": len(strategies),
            "inactive": 0
        }

        logging.info(
            health_check(
                total_strategies=snapshot["total"],
                inactive_strategies=snapshot["inactive"]
            )
        )
        return

    event_bus = EventBus()

    executor = Executor()
    event_bus.subscribe(EventType.ORDER, executor.on_order)

    manager = StrategyManager(event_bus)

    with open("test_strategies.json") as f:
        strategies = json.load(f)

    for s in strategies:
        manager.add_strategy(StrategyRuntime(s, event_bus))

    market = Generator(event_bus)
    await market.start()
    print_final_summary(manager)


if __name__ == "__main__":
    asyncio.run(main())


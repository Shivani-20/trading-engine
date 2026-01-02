import uuid
from core.events import Event, EventType
from strategy.state import StrategyState
from strategy.condition import evaluate
import logging

logger = logging.getLogger("strategy.runtime")

class StrategyRuntime:
    def __init__(self, definition, event_bus):
        self.id = definition["strategy_id"]
        self.instrument = definition["instrument"]
        self.entry_condition = definition["entry_condition"]
        self.exit_condition = definition["exit_condition"]
        self.qty = definition["quantity"]
        self.max_loss = definition["max_loss"]
        self.max_profit = definition["max_profit"]

        self.event_bus = event_bus
        self.state = StrategyState.CREATED

        self.entry_price = None
        self.pnl = 0
        self.failed= False
    
    async def shutdown(self):
        if self.state == StrategyState.OPEN:
            await self.sell(self.entry_price, forced=True)
            self.state = StrategyState.FORCE_CLOSED


    async def on_tick(self, event):
        try:
            tick = event.data

            if tick["instrument"] != self.instrument:
                return

            context = {
                "price": tick["price"],
                "time": tick["time"]
            }

            # ENTRY
            if self.state == StrategyState.CREATED:
                if evaluate(self.entry_condition, context):
                    await self.buy(tick["price"])
                    self.state = StrategyState.OPEN

            # EXIT
            elif self.state == StrategyState.OPEN:
                self.pnl = (tick["price"] - self.entry_price) * self.qty

                if self.pnl <= -self.max_loss:
                    logger.info(f"STOP_LOSS_HIT {self.id}")
                    await self.sell(tick["price"], forced=True)
                    self.state = StrategyState.FORCE_CLOSED

                elif self.pnl >= self.max_profit:
                    logger.info(f"TARGET_HIT {self.id}")
                    await self.sell(tick["price"], forced=True)
                    self.state = StrategyState.FORCE_CLOSED


                elif evaluate(self.exit_condition, context):
                    await self.sell(tick["price"])
                    self.state = StrategyState.CLOSED

        except Exception as e:
            self.failed = True
            logger.error(f"STRATEGY_ERROR: {str(e)}, {self.id}")


    async def buy(self, price):
        self.entry_price = price
        logger.info(f"ENTRY @ {price}, {self.id}")
        await self.emit_order("BUY", price)

    async def sell(self, price, forced=False):
        reason = "FORCED_EXIT" if forced else "NORMAL_EXIT"
        logger.info(f"EXIT @ {price} | {reason}, {self.id}")
        await self.emit_order(
            "SELL",
            price,
            forced=forced
        )

    async def emit_order(self, side, price, forced=False):
        await self.event_bus.publish(
            Event(
                EventType.ORDER,
                {
                    "order_id": str(uuid.uuid4()),
                    "strategy_id": self.id,
                    "instrument": self.instrument,
                    "side": side,
                    "price": price,
                    "qty": self.qty,
                    "forced": forced
                }
            )
        )

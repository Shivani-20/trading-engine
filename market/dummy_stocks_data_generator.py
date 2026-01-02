import asyncio
from datetime import datetime
import random
from core.events import Event, EventType
import os

class Generator:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.price = int(os.environ("DEFAULT_PRICE"))

    async def start(self):
        while True:
            self.price += random.randint(-int(os.environ.get("PRICE_FLUCTUATION")), int(os.environ.get("PRICE_FLUCTUATION")))
            current_time = datetime.now()
            tick = {
                "instrument": os.environ.get("DEFAULT_INDEX"),
                "price": self.price,
                "time": current_time.strftime("%H:%M:%S")
            }

            if current_time.time() >= datetime.strptime(os.environ.get("MARKET_CLOSE"), "%H:%M").time():
                await self.event_bus.publish(
                    Event(EventType.SHUTDOWN, {})
                )
                self.running = False
                break
            
            await self.event_bus.publish(
                Event(EventType.MARKET_TICK, tick)
            )
            await asyncio.sleep(1)

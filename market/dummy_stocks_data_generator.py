import asyncio
from datetime import datetime
import random
from core.events import Event, EventType
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()


class Generator:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.price = int(os.getenv("DEFAULT_PRICE"))

    async def start(self):
        while True:
            self.price += random.randint(-int(os.getenv("PRICE_FLUCTUATION")), int(os.getenv("PRICE_FLUCTUATION")))
            current_time = datetime.now()
            tick = {
                "instrument": os.getenv("DEFAULT_INDEX"),
                "price": self.price,
                "time": current_time.strftime("%H:%M:%S")
            }

            if current_time.time() >= datetime.strptime(os.getenv("MARKET_CLOSE"), "%H:%M").time():
                await self.event_bus.publish(
                    Event(EventType.SHUTDOWN, {})
                )
                self.running = False
                break
            
            await self.event_bus.publish(
                Event(EventType.MARKET_TICK, tick)
            )
            await asyncio.sleep(1)

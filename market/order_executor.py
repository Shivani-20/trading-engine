import logging
logger = logging.getLogger("market.order_executor")

class Executor:
    async def on_order(self, order):
        logger.info(
            f"[{order.data['strategy_id']}] {order.data['side']} @ {order.data['price']}"
        )

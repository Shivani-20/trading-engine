
### Architecture & Flow:
Market Data Generator ---> EventBus ---> Strategy Runtime(s)
                              \
                               ---> Order Executor

| Component        | Event      | Role  |
| ---------------- | ---------- | ----- |
| Market Generator | publishes  | TICK  |
| StrategyRuntime  | subscribes | TICK  |
| StrategyRuntime  | publishes  | ORDER |
| OrderExecutor    | subscribes | ORDER |


Folder-wise explanation:-

Core
>events.py to define the type of event in the queue
>

Market
>dummy_stocks_data_generator.py emits simulated price ticks
>order_executor.py logs simulated BUY / SELL orders 

The EventBus acts as a pub/sub system

Each StrategyRuntime evaluates entry, exit, and risk independently

Risk management is implemented inside the strategy/runtime.py and evaluated on every market tick. PnL is calculated in real time, and forced exits are triggered immediately when max loss or max profit thresholds are breached.



### Concurrency Model:
>Built using asyncio
>One event loop
>Multiple async tasks
>No threads or blocking calls

Key guarantees:
>Market feed never blocks
>Strategies run concurrently
>One strategy failure does not affect others

### How to run using Docker:
```bash
docker compose up --build
```

### Configuration handling:
>

### Logging & health checks:
>main.py has the configured root logger, 
    format: "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
>All loggers propagate to the root logger



### Production improvements you would add:

Condition evaluation:
>To adhere to security practices, I will replace eval() in condition.py with some specific DSL.
>I would enable/disable an order execution or strategy execution at runtime


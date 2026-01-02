def evaluate(condition: str, context: dict) -> bool:
    expr = condition.replace("OR", "or").replace("AND", "and")

    return eval(
        expr,
        {"__builtins__": {}},
        context
    )


def health_check(total_strategies, inactive_strategies):
    status = "healthy" if inactive_strategies == 0 else "unhealthy"
    return {
        "status": status,
        "total_strategies": total_strategies,
        "inactive_strategies": inactive_strategies
    }

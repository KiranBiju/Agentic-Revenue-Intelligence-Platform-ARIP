def validation_router(state):
    failed = any(
        item["status"] == "rejected"
        for item in state["validation_results"]
    )

    if failed and state["retries"] < 3:
        state["retries"] += 1
        return "executor"

    return "optimizer"
from app.agents.executor_agent import ExecutorAgent

executor = ExecutorAgent()


def executor_node(state):
    results = executor.run(
        leads=state["selected_leads"],
        strategy=state["strategy"]
    )

    state["results"] = results

    state["logs"].append("Executor node completed")

    return state
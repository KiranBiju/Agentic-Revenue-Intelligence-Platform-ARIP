from app.agents.planner_agent import PlannerAgent

planner = PlannerAgent()


def planner_node(state):
    strategy = planner.run(
        ranked_leads=state["selected_leads"]
    )

    state["strategy"] = strategy

    state["logs"].append("Planner node completed")

    return state
from app.agents.validator_agent import ValidatorAgent

validator = ValidatorAgent()


def validator_node(state):
    validation_results = validator.run(
        results=state["results"]
    )

    state["validation_results"] = validation_results

    state["logs"].append("Validator node completed")

    return state
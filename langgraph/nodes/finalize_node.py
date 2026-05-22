from app.core.logging import logger


def finalize_node(state):

    ranked_leads = state.get("ranked_leads", [])
    selected_leads = state.get("selected_leads", [])
    results = state.get("results", [])

    top_score = 0

    if ranked_leads:
        top_score = ranked_leads[0].get(
            "priority_score",
            0
        )

    logger.info("[FINALIZE] Campaign finalized")

    return {
        **state,

        "status": "completed",

        "total_leads": len(
            state.get("input_leads", [])
        ),

        "selected": len(selected_leads),

        "processed": len(results),

        "top_score": top_score,

        "ranked_leads": ranked_leads,

        "selected_leads": selected_leads,

        "results": results,

        "logs": state.get("logs", [])
    }
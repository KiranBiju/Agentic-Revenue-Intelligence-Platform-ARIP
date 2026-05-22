from langgraph.graph import StateGraph, END

from app.langgraph.state import ARIPState

from app.langgraph.nodes.planner_node import planner_node
from app.langgraph.nodes.executor_node import executor_node
from app.langgraph.nodes.validator_node import validator_node
from app.langgraph.nodes.optimizer_node import optimizer_node
from app.langgraph.nodes.finalize_node import finalize_node

from app.langgraph.routers import validation_router


workflow = StateGraph(ARIPState)


workflow.add_node(
    "planner",
    planner_node
)

workflow.add_node(
    "executor",
    executor_node
)

workflow.add_node(
    "validator",
    validator_node
)

workflow.add_node(
    "optimizer",
    optimizer_node
)

workflow.add_node(
    "finalize",
    finalize_node
)


workflow.set_entry_point("planner")


workflow.add_edge(
    "planner",
    "executor"
)

workflow.add_edge(
    "executor",
    "validator"
)

workflow.add_conditional_edges(
    "validator",
    validation_router,
    {
        "executor": "executor",
        "optimizer": "optimizer"
    }
)

workflow.add_edge(
    "optimizer",
    "finalize"
)

workflow.add_edge(
    "finalize",
    END
)

graph = workflow.compile()
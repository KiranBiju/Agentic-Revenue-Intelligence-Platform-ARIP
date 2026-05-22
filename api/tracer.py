from datetime import datetime, timezone


def add_trace(state, step, agent, action, status, metadata=None):
    if not hasattr(state, "agent_traces"):
        state.agent_traces = []

    state.agent_traces.append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": step,
            "agent": agent,
            "action": action,
            "status": status,
            "metadata": metadata or {},
        }
    )
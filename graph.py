"""Builds the two-agent Plan-and-Execute LangGraph."""
from typing import Union
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

from config import planner_llm
from state import PlanExecuteState
from thinking_agent import thinking_agent, Plan
from executing_agent import executing_agent


# --- Replanner: decides if we're done or need more steps ---

class Response(BaseModel):
    """Final response to the user."""
    response: str = Field(description="The final answer to the user's request.")


class Act(BaseModel):
    """The replanner's decision: either finalize or extend the plan."""
    action: Union[Response, Plan] = Field(
        description="If the task is complete, use Response. "
                    "If more steps are needed, use Plan."
    )


REPLANNER_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a replanner. Given the original goal, the plan, and what "
     "has been done so far, decide if the goal is achieved.\n\n"
     "If YES: return a final Response.\n"
     "If NO: return a Plan with only the remaining steps (do not repeat "
     "steps already done)."),
    ("user",
     "Original goal:\n{input}\n\n"
     "Current plan:\n{plan}\n\n"
     "Steps completed so far:\n{past_steps}"),
])

replanner = REPLANNER_PROMPT | planner_llm.with_structured_output(Act)


def replan_node(state: PlanExecuteState) -> dict:
    """Check progress and decide whether to continue or finalize."""
    if not state.get("plan"):
        output = replanner.invoke({
            "input": state["input"],
            "plan": "No remaining steps.",
            "past_steps": state["past_steps"],
        })
        if isinstance(output.action, Response):
            return {"response": output.action.response}
        return {"plan": output.action.steps}

    return {}


def should_continue(state: PlanExecuteState) -> str:
    """Route: if response is set, end; otherwise, execute next step."""
    if state.get("response"):
        return "end"
    return "execute"


# --- Build the graph ---

def build_graph():
    workflow = StateGraph(PlanExecuteState)

    workflow.add_node("think", thinking_agent)
    workflow.add_node("execute", executing_agent)
    workflow.add_node("replan", replan_node)

    workflow.add_edge(START, "think")
    workflow.add_edge("think", "execute")
    workflow.add_edge("execute", "replan")

    workflow.add_conditional_edges(
        "replan",
        should_continue,
        {
            "execute": "execute",
            "end": END,
        },
    )

    return workflow.compile()


app = build_graph()
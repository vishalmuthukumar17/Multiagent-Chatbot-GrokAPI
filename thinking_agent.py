"""The Thinking Agent: creates the plan."""
from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

from config import planner_llm
from state import PlanExecuteState


class Plan(BaseModel):
    """A plan consisting of ordered, actionable steps."""
    steps: List[str] = Field(
        description="Ordered list of 3-5 atomic steps to solve the task. "
                    "Each step must be executable on its own."
    )


PLANNER_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a planning expert. Break the user's objective into a simple "
     "step-by-step plan. Each step should be a single, actionable task. "
     "Do not add superfluous steps. The result of the final step should "
     "be the final answer."),
    ("user", "{input}"),
])

# Structured output via Groq's JSON mode
planner = PLANNER_PROMPT | planner_llm.with_structured_output(Plan)


def thinking_agent(state: PlanExecuteState) -> dict:
    """Plan the steps required to achieve the user's goal."""
    plan = planner.invoke({"input": state["input"]})
    print(f"\n[Thinking Agent] Generated plan with {len(plan.steps)} steps:")
    for i, step in enumerate(plan.steps, 1):
        print(f"  {i}. {step}")
    return {"plan": plan.steps}
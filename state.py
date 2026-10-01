"""Shared state for the Plan-and-Execute graph."""
import operator
from typing import Annotated, List, Tuple
from typing_extensions import TypedDict


class PlanExecuteState(TypedDict):
    """State flowing through the thinking and executing agents."""
    input: str                                              # Original user request
    plan: List[str]                                         # Remaining steps to execute
    past_steps: Annotated[List[Tuple[str, str]], operator.add]  # (step, result) history
    response: str                                           # Final answer
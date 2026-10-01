"""The Executing Agent: manual tool loop for Groq compatibility."""
from langchain_core.messages import HumanMessage, ToolMessage

from config import executor_llm
from tools import get_population, calculate, web_search
from state import PlanExecuteState


TOOLS = {
    "get_population": get_population,
    "calculate": calculate,
    "web_search": web_search,
}


def executing_agent(state: PlanExecuteState) -> dict:
    """Execute the first step of the current plan."""
    plan = state.get("plan", [])
    if not plan:
        return {}

    current_step = plan[0]
    print(f"\n[Executing Agent] Running step: {current_step}")

    # Bind tools to the model so it knows what's available
    llm_with_tools = executor_llm.bind_tools(list(TOOLS.values()))

    messages = [HumanMessage(content=current_step)]
    final_answer = ""

    # Manual agent loop (max 5 iterations to prevent infinite loops)
    for _ in range(5):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # No tool calls → this is the final answer
        if not response.tool_calls:
            final_answer = response.content
            break

        # Execute each tool call and append results
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print(f"  -> Calling tool: {tool_name}({tool_args})")

            if tool_name in TOOLS:
                try:
                    result = TOOLS[tool_name].invoke(tool_args)
                except Exception as e:
                    result = f"Tool error: {e}"
            else:
                result = f"Unknown tool: {tool_name}"

            messages.append(ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            ))
    else:
        # Loop exhausted without a final answer
        final_answer = response.content if response.content else "Max iterations reached."

    print(f"  -> Result: {final_answer[:100]}{'...' if len(final_answer) > 100 else ''}")

    return {
        "plan": plan[1:],
        "past_steps": [(current_step, final_answer)],
    }
"""Tools available to the executing agent."""
from langchain_core.tools import tool


@tool
def get_population(city: str) -> str:
    """Return the population of a given city."""
    data = {
        "tokyo": "approximately 14 million",
        "delhi": "approximately 32 million",
        "new york": "approximately 8.3 million",
        "paris": "approximately 2.1 million",
        "mumbai": "approximately 12.5 million",
    }
    return data.get(city.lower(), f"No population data available for {city}.")


@tool
def calculate(expression: str) -> str:
    """Evaluate a simple arithmetic expression (e.g. '12 * 5 + 3')."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: only numbers and + - * / ( ) are allowed."
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"


@tool
def web_search(query: str) -> str:
    """Search the web for factual information (mock)."""
    mock_db = {
        "france": "France is a country in Western Europe. Its capital is Paris.",
        "python": "Python is a programming language created by Guido van Rossum in 1991.",
        "langgraph": "LangGraph is a library for building stateful multi-agent applications.",
    }
    for key, value in mock_db.items():
        if key in query.lower():
            return value
    return f"No search results for: {query}"
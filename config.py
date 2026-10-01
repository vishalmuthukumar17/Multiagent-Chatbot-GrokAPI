"""Configuration using Groq's free tier."""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise EnvironmentError("GROQ_API_KEY is not set in .env file.")

# Thinking Agent: larger model for better planning
planner_llm = ChatGroq(
    model="openai/gpt-oss-120b",   # ← Changed from llama-3.3-70b-versatile
    temperature=0,
    max_retries=2,
)

# Executing Agent: faster model with higher rate limits
executor_llm = ChatGroq(
    model="openai/gpt-oss-20b",    # ← Changed from llama-3.1-8b-instant
    temperature=0,
    max_retries=2,
)
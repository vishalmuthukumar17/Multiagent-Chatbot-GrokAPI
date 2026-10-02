# 🤖 Multi-Agent Chatbot (Groq Free Tier)

> A two-agent Plan-and-Execute chatbot built with LangGraph and powered by Groq's free API

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-orchestration-orange)
![Groq](https://img.shields.io/badge/Groq-free%20tier-purple)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Description

A two-agent Plan-and-Execute chatbot where a Thinking Agent builds a step-by-step plan and an Executing Agent carries out each step using tools, powered by Groq's free API with LangGraph orchestration and conversation memory.

---

## 🏗️ Architecture

```
                ┌──────────────────┐
   User Query → │  Thinking Agent  │  (openai/gpt-oss-120b)
                │  Builds the plan │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Executing Agent  │  (openai/gpt-oss-20b)
                │  Runs one step   │  + tools
                │  at a time       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │    Replanner     │
                │  Goal reached?   │
                └────────┬─────────┘
                    No │  │ Yes
                       ▼  ▼
                    Loop  Final Answer
```

---

## ✨ Features

- ✅ **Free to run** — Groq's free tier (no credit card)
- ✅ **Two-agent architecture** — planning and execution decoupled
- ✅ **Tool use** — calculate, web search, population lookup
- ✅ **Conversation memory** — LangGraph checkpointing
- ✅ **Interactive CLI** — simple terminal chat loop
- ✅ **Modular design** — add tools or agents easily

---

## 🚀 Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/vishalmuthukumar17/Multiagent-chatbot-groq.git
cd Multiagent-chatbot-groq
```

### 2. Create virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a free Groq API key

1. Go to [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign in (Google or GitHub works)
3. Click **Create API Key**
4. Copy the key — it starts with `gsk_`

### 5. Create the `.env` file

```env
GROQ_API_KEY=gsk_your_actual_key_here
```

⚠️ **Never commit this file.** It's already listed in `.gitignore`.

### 6. Run the chatbot

```bash
python main.py
```

---

## 💬 Usage

```
============================================================
  Two-Agent Plan-and-Execute System (Groq - Free Tier)
  Thinking Agent  ->  plans the steps
  Executing Agent ->  carries them out
  Commands: 'quit' to exit
============================================================

You:
```

### Example queries

```
What is agentic AI?
```

```
What is the population of Tokyo multiplied by 2?
```

```
Calculate 245 * 37 + 100
```

```
Search for Python and write a one-sentence summary.
```

Type `quit` to exit.

---

## 📁 Project Structure

```
multi-agent-chatbot/
├── config.py              # Groq LLM configuration
├── state.py               # PlanExecuteState TypedDict
├── tools.py               # Tools: calculate, web_search, get_population
├── thinking_agent.py      # Planner node
├── executing_agent.py     # Executor node with manual tool loop
├── graph.py               # LangGraph assembly + replanner
├── main.py                # CLI entry point
├── requirements.txt       # Dependencies
├── .env                   # Your Groq API key (NOT committed)
├── .gitignore             # Excludes .env, .venv, __pycache__
└── README.md              # This file
```

---

## 🧠 How It Works

### 1. Planning

The Thinking Agent receives the user's request and returns a Pydantic-validated plan:

```python
class Plan(BaseModel):
    steps: List[str]  # e.g. ["Look up Tokyo population", "Multiply by 2"]
```

### 2. Execution

The Executing Agent runs **only the first step** each time, using a manual ReAct loop:

1. Send the step to `openai/gpt-oss-20b`
2. If the model requests a tool, run it and feed the result back
3. Repeat until the model returns a final answer for that step

> **Why a manual loop instead of `create_react_agent`?**
> Groq's API rejects requests where `tool_choice=none` is set but the model still calls a tool. LangChain's `create_react_agent` triggers this bug with `gpt-oss` models. The manual loop avoids it entirely by never sending `tool_choice`.

### 3. Replanning

After each step, the Replanner decides:
- **Goal reached?** → return the final answer
- **More work needed?** → generate remaining steps and loop

---

## 🛠️ Available Tools

| Tool | Description | Example input |
|---|---|---|
| `calculate` | Evaluates arithmetic expressions | `"245 * 37 + 100"` |
| `web_search` | Mock search (replace with real API in prod) | `"agentic ai"` |
| `get_population` | Returns population of a known city | `"Tokyo"` |

To add a new tool:

1. Define it in `tools.py` with the `@tool` decorator
2. Import it into `executing_agent.py` and add it to the `TOOLS` dict

---

## ⚙️ Configuration

Change the models in `config.py`:

```python
planner_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
executor_llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
```

### Free-tier rate limits (Groq)

| Model | Requests/day | Tokens/minute |
|---|---|---|
| `openai/gpt-oss-120b` | 1,000 | 8,000 |
| `openai/gpt-oss-20b` | 1,000 | 8,000 |

If you hit a `429 Too Many Requests` error, wait 60 seconds and retry.

### Check available Groq models

```bash
python -c "from dotenv import load_dotenv; load_dotenv(); import os; from groq import Groq; print([m.id for m in Groq(api_key=os.getenv('GROQ_API_KEY')).models.list().data])"
```

> **Note:** Groq retires older models periodically. If you get a `404 model_not_found` error, update the model IDs in `config.py`.

---

## 🔧 Extending the Project

### Add a new worker agent

1. Create `agents/new_agent.py` with its own `create_agent` call
2. Wrap it as a `@tool` function
3. Add that tool to your supervisor's tool list

### Swap Groq for another provider

Edit `config.py`:

```python
from langchain_openai import ChatOpenAI
planner_llm = ChatOpenAI(model="gpt-4o-mini")
executor_llm = ChatOpenAI(model="gpt-4o-mini")
```

### Use a real search API

Replace the mock `web_search` in `tools.py` with [Tavily](https://tavily.com/), [SerpAPI](https://serpapi.com/), or [Brave Search](https://brave.com/search/api/).

---

## 🐛 Troubleshooting

| Error | Fix |
|---|---|
| `GROQ_API_KEY is not set` | Create `.env` with `GROQ_API_KEY=gsk_...` |
| `404 model_not_found` | Model was retired — check `config.py` |
| `400 Tool choice is none...` | Use the manual loop version of `executing_agent.py` |
| `429 Too Many Requests` | Rate limit hit — wait 60 seconds |
| `ModuleNotFoundError: langchain_groq` | Activate venv: `.\.venv\Scripts\Activate.ps1` |
| `running scripts is disabled` (PowerShell) | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |

---

## 📊 Tech Stack

- [LangGraph](https://github.com/langchain-ai/langgraph) — graph orchestration
- [LangChain](https://github.com/langchain-ai/langchain) — LLM abstraction
- [Groq](https://groq.com/) — ultra-fast free LLM inference
- [Pydantic](https://docs.pydantic.dev/) — schema validation

---


## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

##  Acknowledgments

- Inspired by the [Plan-and-Execute](https://blog.langchain.dev/planning-agents/) pattern
- Built with the free [Groq API](https://console.groq.com/)

---

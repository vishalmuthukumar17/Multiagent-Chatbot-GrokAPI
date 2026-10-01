"""Interactive CLI for the two-agent Plan-and-Execute system."""
from graph import app


BANNER = """
============================================================
  Two-Agent Plan-and-Execute System (Groq - Free Tier)
  Thinking Agent  ->  plans the steps
  Executing Agent ->  carries them out
  Commands: 'quit' to exit
============================================================
"""


def run():
    print(BANNER)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        try:
            result = app.invoke({
                "input": user_input,
                "past_steps": [],
            })
            print(f"\n{'='*60}")
            print("FINAL ANSWER:")
            print(f"{'='*60}")
            print(result.get("response", "No response generated."))
        except Exception as e:
            print(f"\n[Error] {type(e).__name__}: {e}")


if __name__ == "__main__":
    run()
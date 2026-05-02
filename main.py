import sys
from db import init_db
from agent import build_agent, extract_reply

BANNER = """
╔══════════════════════════════════════════╗
║            E-Commerce AI Agent           ║
║  Type your question and press Enter.     ║
║  Commands: 'quit' or 'exit' to leave.    ║
╚══════════════════════════════════════════╝
"""


def main():
    print(BANNER)

    init_db()

    print("⏳ Loading agent…")
    agent = build_agent()
    print("✅ Agent ready! Ask me anything about products, users, or orders.\n")

    history = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            print("Agent: Goodbye! Have a great day. 👋")
            break

        history.append({"role": "user", "content": user_input})

        try:
            result = agent.invoke({"messages": history})
            reply = extract_reply(result)

            history.append({"role": "assistant", "content": reply})

            print(f"\nAgent: {reply}\n")
        except Exception as e:
            print(f"\n⚠️  Error: {e}\n")


if __name__ == "__main__":
    main()

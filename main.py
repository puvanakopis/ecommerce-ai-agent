import sys
from db import init_db

BANNER = """
╔══════════════════════════════════════════╗
║         E-Commerce AI Agent              ║
║  Type your question and press Enter.     ║
║  Commands: 'quit' or 'exit' to leave.    ║
╚══════════════════════════════════════════╝
"""

def main():
    print(BANNER)

    init_db()


if __name__ == "__main__":
    main()
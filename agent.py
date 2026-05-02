from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from config import settings
from tools import tools
from prompts import SYSTEM_PROMPT


def build_agent():
    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY missing. Add it to your .env file.")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=settings.GROQ_API_KEY,
        temperature=0.2,
    )
    return create_react_agent(model=llm, tools=tools, prompt=SYSTEM_PROMPT)


def extract_reply(result: dict) -> str:
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if getattr(msg, "type", None) == "ai":
            content = getattr(msg, "content", "")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                parts = [c.get("text", "") for c in content if isinstance(c, dict)]
                return "\n".join(p for p in parts if p).strip()
    return "Sorry, I could not generate a response."
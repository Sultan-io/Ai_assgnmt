import asyncio
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import aiosqlite
from dotenv import load_dotenv
from fastmcp.client import Client
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain.mcp import MCPAdapter
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from agent import SYSTEM_PROMPT
from llm import llm
from memory import list_threads, show_history

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
MCP_URL = os.getenv("MCP_URL", "http://127.0.0.1:8000/mcp")
MCP_KEY = os.getenv("FASTMCP_KEY")


def make_adapter():
    if MCP_KEY:
        return MCPAdapter(Client(MCP_URL, auth=MCP_KEY))
    return MCPAdapter(MCP_URL)


async def repair_unanswered_tool_calls(app, config) -> bool:
    """Turn any saved unanswered tool call into an MCP failure ToolMessage."""
    state = await app.aget_state(config)
    messages = state.values.get("messages", [])
    answered = {
        getattr(message, "tool_call_id", None)
        for message in messages
        if isinstance(message, ToolMessage)
    }
    repair_messages = []
    for message in messages:
        if isinstance(message, AIMessage):
            for call in getattr(message, "tool_calls", []):
                call_id = call.get("id")
                if call_id and call_id not in answered:
                    repair_messages.append(ToolMessage(
                        content="MCP server unavailable. The tool could not be called.",
                        tool_call_id=call_id,
                        name=call.get("name"),
                    ))
    if repair_messages:
        await app.aupdate_state(config, {"messages": repair_messages})
        return True
    return False


async def stream_response(app, inputs, config) -> bool:
    """Stream updates and model tokens, and recover cleanly from MCP failures."""
    try:
        async for chunk in app.astream(
            inputs, config, stream_mode=["updates", "messages"], version="v2"
        ):
            if chunk["type"] == "messages":
                token, metadata = chunk["data"]
                if getattr(token, "text", "") and metadata.get("langgraph_node"):
                    print(token.text, end="", flush=True)
            else:
                for node, update in chunk["data"].items():
                    if node == "tools":
                        continue
        print()
        return True
    except Exception as exc:
        print(f"\nMCP error: {exc}")
        repaired = await repair_unanswered_tool_calls(app, config)
        if repaired:
            print("Added a tool-failure result to chat memory so the conversation can continue.")
        return False


async def main() -> None:
    async with aiosqlite.connect("cgpa_memory.sqlite") as conn:
        memory = AsyncSqliteSaver(conn)
        async with make_adapter() as adapter:
            tools = await adapter.list_tools()
            app = create_agent(
                model=llm,
                tools=tools,
                system_prompt=SYSTEM_PROMPT,
                checkpointer=memory,
            )

            print("PUCIT GPA/CGPA Assistant")
            saved_threads = await list_threads(memory)
            if saved_threads:
                print("Saved chats:", ", ".join(saved_threads))

            name = input("Who is chatting? ").strip() or "default"
            config = {"configurable": {"thread_id": name}}
            print("\nCommands: /switch, /history, /forget, quit/exit")

            while True:
                try:
                    user_input = input("You: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nGoodbye.")
                    break
                if not user_input:
                    continue
                if user_input.lower() in {"quit", "exit"}:
                    print("Goodbye.")
                    break
                if user_input == "/switch":
                    name = input("Who is chatting? ").strip() or "default"
                    config = {"configurable": {"thread_id": name}}
                    continue
                if user_input == "/history":
                    await show_history(app, config)
                    continue
                if user_input == "/forget":
                    await memory.adelete_thread(name)
                    print(f"Forgot chat history for '{name}'.")
                    continue

                print("Agent: ", end="", flush=True)
                ok = await stream_response(app, {"messages": [HumanMessage(user_input)]}, config)
                if not ok:
                    await repair_unanswered_tool_calls(app, config)
                    await stream_response(
                        app,
                        {"messages": [HumanMessage(
                            "The MCP tool server is currently unavailable. "
                            "Do not claim a tool calculation was performed. "
                            "Tell the student the tool service is down and ask them to try again."
                        )]},
                        config,
                    )


if __name__ == "__main__":
    asyncio.run(main())

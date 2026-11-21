from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


async def list_threads(memory: AsyncSqliteSaver) -> list[str]:
    """List unique thread IDs that have saved checkpoints."""
    threads: set[str] = set()
    async for checkpoint in memory.alist(None):
        configurable = checkpoint.config.get("configurable", {})
        thread_id = configurable.get("thread_id")
        if thread_id:
            threads.add(str(thread_id))
    return sorted(threads)


async def show_history(app, config: dict) -> None:
    """Print the conversation messages for the current thread."""
    state = await app.aget_state(config)
    messages = state.values.get("messages", [])
    if not messages:
        print("(No saved history)")
        return
    for message in messages:
        role = getattr(message, "type", "message")
        content = getattr(message, "content", "")
        if role == "human":
            print(f"You: {content}")
        elif role == "ai":
            print(f"Agent: {content}" if content else "Agent: [tool call]")
        elif role == "tool":
            print(f"Tool {getattr(message, 'name', '')}: {content}")

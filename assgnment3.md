# Assignment 3

The last step for the CGPA Guider you built in the previous assignment: you can use the graph version or, for your ease, you can also use the `create_agent` version. You give it the two things from Lab 6—**memory** and **streaming**—and you move its tools out onto your own **MCP server** on the internet (Lab 7). The agent itself doesn't change. Ask your TAs anything, and use AI to learn, but write the code yourself.

---

## The Idea

Your current CGPA Guider has three problems:

1. **It forgets.** Close it and the student has to type their CGPA and all relevant details again.
2. **It's silent.** While `check` widens the window three times, the student stares at a blank screen.
3. **Its tools are locked in.** They sit in `tools.py` next to the agent, so only your agent can use them. A friend's agent, in another language or another framework, can't.

---

## Task 1: Your MCP Server (`server/`)

MCP is one standard plug between an agent (the client) and a set of tools (the server). The server says *"here are my tools"* (`tools/list`) and runs them when asked (`tools/call`). It doesn't care what language or framework the client uses. `FastMCP` builds a server from plain Python functions: the docstring and type hints become the description the model reads, just like `@tool`.

The starter `server.py` already shares one tool:

```python
from fastmcp import FastMCP
from tools import get_credit_hours

mcp = FastMCP("cgpa")
mcp.tool(get_credit_hours)  # turns a function into an MCP tool; similarly, do it for all
```

**Your job:** Share all your tools, then test the server on its own. No agent, no LLM, and no key needed:

```bash
fastmcp list server.py
# Lists all your tools, with descriptions

fastmcp call server.py get_credit_hours semesters='[5,6]'
# 37.0 -> Calling the tool
```

---

## Task 2: Connect Your Agent to the Server (`agent/`)

Start the server in its own terminal and leave it running:

```bash
cd server && python server.py
# serves http://127.0.0.1:8000/mcp
```

In `agent/.env`, next to your `GROQ_API_KEY`, add:

```env
MCP_URL=http://127.0.0.1:8000/mcp
```

Then make two changes:

1. **Get tools from the server and attach them to your agent.**
2. **Everything is async now.** MCP tools talk over the network, so they only come in an async version. Your checkpointer is async too.

```python
tools = await MCPAdapter(server).list_tools()  # connect, list tools, disconnect
```

**OR**

```python
async with MCPAdapter(server) as adapter:
    tools = adapter.list_tools()  # or work within with-construct; new connection whenever needed
```

`MCPAdapter` is the MCP client which turns each server tool into a normal LangChain tool, so `bind_tools` and `ToolNode` work exactly as before.

3. **Run it, and fix what breaks.**

---

## Task 3: Memory

A checkpointer saves the graph's whole state after every step. A `thread_id` says whose conversation it is. You send only the new message. The graph loads everything saved for that thread, and the reducer on messages (`add_messages`) adds your message to the end. We use a SQLite file so chats survive closing the program. `AsyncSqliteSaver` is the async version of Lab 6's `SqliteSaver`.

Use the following config:

```python
config = {"configurable": {"thread_id": name}}
```

In `main()`:
1. Print the saved chats with `await list_threads(memory)`, then ask who is chatting. Their name is the `thread_id`.
2. Support three commands in the loop:
   - `/switch` — change person
   - `/history` — `await show_history(app, config)`
   - `/forget` — `await memory.adelete_thread(name)`

---

## Task 4: Streaming

`ainvoke` waits for the whole run. `astream` hands you pieces as they happen. Ask for two kinds at once:

```python
async for chunk in app.astream(inputs, config, stream_mode=["updates", "messages"], version="v2"):
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]          # one piece of the model's answer
        node = metadata["langgraph_node"]        # which node produced it
    else:                                        # "updates"
        for node, update in chunk["data"].items():
            # update = what that node returned
            pass
```

---

## Task 5: Put the Server on the Internet

Your agent doesn't change at all here—only `MCP_URL` (and a key) in `.env`.

Find some good free hosting online for your MCP server:
- [Prefect Horizon](http://horizon.prefect.io/) is one option; though it only lets you host privately on the free plan, you will need to generate an API key from the dashboard in order to run it with ease, and then it will work fine.
- There are also other free hosting services like **Render** which you can try.

Choose a free service and host your MCP server. Check it, then switch your agent:

```bash
fastmcp list <your URL> --auth <your key>  # your tools
fastmcp list <your URL>                    # if your hosting service allows without auth
```

In case your hosting service doesn't require auth, you can simply do:

```python
MCPAdapter(target_url)
```

In case your hosting service requires auth:

```python
from fastmcp.client import Client

MCPAdapter(Client(target_url, auth=api_key))
```

In case you have multiple MCP servers:

```python
config = {
    "mcpServers": {
        "langchain": {"url": "https://docs.langchain.com/mcp", "transport": "http"},
        "another_mcp": {"url": "https://xyz/mcp", "auth": "api_key", "transport": "http"},
    },
}
```

Put the URL in `MCP_URL` and the key in `FASTMCP_KEY`. The starter already passes the key: `Client(MCP_URL, auth=KEY)`.

---

## Task 6: When the Server is Down

Stop your server (or turn off Wi-Fi) in the middle of a chat and ask another question. The chat crashes. Worse, run it again and type `/history`: a tool call that never got an answer is saved in your memory. Most model APIs, Groq included, refuse a chat like that, so this person is stuck for good. 

**Fix it so the model is told instead.**

---

## Submission and Rules

- Submit your code zipped as `ROLLNO_Assignment3.zip`, with a `README.md` that includes:
  - Your server URL (and `api_key` in case your MCP server requires auth).
  - Your GitHub repository link for the server code.
- **Viva Preparation:** You must come prepared for a viva covering topics including **Streaming**, **Memory**, and **MCP**. You will be asked questions about these concepts as well as your own code.

**Good Luck!**
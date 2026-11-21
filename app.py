import streamlit as st
import asyncio
import os
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from fastmcp.client import Client
from langchain.mcp import MCPAdapter

from agent import SYSTEM_PROMPT
from llm import llm

load_dotenv()


async def load_mcp_tools():
    """Load LangChain tools from the configured MCP server."""
    mcp_url = os.getenv("MCP_URL", "http://127.0.0.1:8000/mcp")
    mcp_key = os.getenv("FASTMCP_KEY")
    adapter = MCPAdapter(Client(mcp_url, auth=mcp_key)) if mcp_key else MCPAdapter(mcp_url)
    async with adapter as connection:
        return await connection.list_tools()


@st.cache_resource
def get_agent():
    """Create and cache the LangChain GPA agent once for the app lifecycle."""
    try:
        tools = asyncio.run(load_mcp_tools())
        return create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)
    except Exception as exc:
        st.error(f"Could not connect to the MCP server: {exc}")
        return None


st.set_page_config(
    page_title="PUCIT GPA Assistant",
    page_icon="🎓",
    layout="centered",
)

st.title("🎓 PUCIT Conversational GPA Agent")
st.caption("Ask questions about your GPA, CGPA target plans, or BS(CS) courses.")

with st.sidebar:
    st.header("Settings & Options")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

user_input = st.chat_input("e.g. I got 78 in Analysis of Algorithms and 85 in AI...")

if user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking & calculating..."):
            agent = get_agent()
            if agent is not None:
                result = asyncio.run(
                    agent.ainvoke({"messages": st.session_state.messages})
                )
                st.session_state.messages = result["messages"]
                final_reply = st.session_state.messages[-1].content
                st.write(final_reply)

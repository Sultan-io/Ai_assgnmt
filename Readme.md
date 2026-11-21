# PUCIT GPA Assistant

## Local setup

1. Install dependencies: `pip install fastmcp langgraph-checkpoint-sqlite streamlit python-dotenv langchain langchain-core`.
2. Copy `.env.example` to `.env` and set `API_KEY` (Groq), `MCP_URL`, and optionally `FASTMCP_KEY`.
3. Start the MCP server:
   ```bash
   cd server
   python server.py
   ```
4. In another terminal, start the assignment 3 terminal agent:
   ```bash
   python agent/main.py
   ```
5. The existing Streamlit app remains available with:
   ```bash
   streamlit run app.py
   ```

## MCP server testing

```bash
fastmcp list server/server.py
fastmcp call server/server.py get_credit_hours semesters='[5,6]'
```

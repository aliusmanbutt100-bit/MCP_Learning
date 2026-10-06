# MCP Learning

Hands-on learning repo for the **Model Context Protocol (MCP)** — built step by step while learning how MCP servers, clients, and LLM integration work in practice.

## What's in here

This repo documents a structured path through MCP, starting from a simple calculator server and ending with a full LLM-integrated client using both manual and automated (LangChain) approaches.

| File | What it covers |
|---|---|
| `01_server.py` | First MCP server — exposes `add`, `sub`, `mul`, `div` tools using `FastMCP` and the `@mcp.tool()` decorator |
| `01_client.py` | Manual MCP client — connects to the server, lists tools, and calls them directly using `ClientSession` |
| `03_resource.py` | Demonstrates MCP **Resources** — read-only data exposed via `@app.resource("uri")` |
| `04_prompt.py` | Demonstrates MCP **Prompts** — reusable prompt templates via `@app.prompt()` |
| `07_mcp_connect_llm.py` | Manually wires an LLM (OpenRouter) to MCP tools — converts MCP tool schemas into OpenAI's function-calling format, parses `tool_calls`, and executes them against the MCP server |
| `08_langchain_adapter.py` | Same LLM + tool-calling flow, but using `langchain-mcp-adapters` to automate the tool conversion (`load_mcp_tools`) and `llm.bind_tools()` |

## Core concepts covered

- **MCP architecture** — server/client model, why it's a framework-agnostic standard (vs. tools tied to one library like LangChain's `bind_tools`)
- **Tools** — actions an LLM can trigger (`@mcp.tool()`)
- **Resources** — read-only data an LLM can access (`@app.resource()`)
- **Prompts** — reusable prompt templates served by the MCP server (`@app.prompt()`)
- **Transports** — using `stdio` for local server-client communication
- **Manual vs. automated integration** — writing the tool-conversion and tool-calling logic by hand first, then seeing how `langchain-mcp-adapters` automates it
- **Testing with MCP Inspector** — using `npx @modelcontextprotocol/inspector` to inspect and test tools without writing a client

## Key takeaway

MCP doesn't replace an orchestration layer like LangGraph — it standardizes how tools are *exposed*, so the same tool can be used by any MCP-compatible client (Claude Desktop, a custom LangGraph agent, etc.) without rewriting it per framework.

## Setup

```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install mcp langchain-mcp-adapters langchain-openai python-dotenv
```

Add a `.env` file with:
```
OPENROUTER_API_KEY=your_key_here
```

## Running

```bash
# Test a server directly with MCP Inspector
npx @modelcontextprotocol/inspector python 01_server.py

# Run a client (starts its paired server automatically)
python 01_client.py
```

## Note on `mcp` package versions

- `mcp` v2.x: `from mcp.server.mcpserver import MCPServer`
- `mcp` v1.x: `from mcp.server.fastmcp import FastMCP`

Installing `langchain-mcp-adapters` currently pins `mcp` back to v1.x — check your installed version with `pip show mcp` if you hit import errors.

---

Built as part of a GenAI / Agentic AI developer learning path, following the [Axis Retail Agent](https://github.com/aliusmanbutt100-bit) multi-agent project.

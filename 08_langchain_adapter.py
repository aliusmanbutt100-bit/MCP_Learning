#Previously we convert the tool_list in LLM readable formatt and connect it with LLM manually but now we do this automatically with the help of a library.In previous we do manual to understand the internal working or flow
#pip install langchain-mcp-adapters this package do this 2 tasks(convert and connect for us)
import asyncio
# asyncio: async code chalane ke liye (pehle jaisa)

from langchain_mcp_adapters.tools import load_mcp_tools
# load_mcp_tools: MCP server se tools leta hai aur seedha
#                 LangChain-compatible bana deta hai (auto-conversion)

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
# ye teeno pehle jaisa hi hai - connection banane ke liye

from langchain_openai import ChatOpenAI
# ChatOpenAI: LangChain ka LLM wrapper (aap already jaante ho
#             Axis Retail Agent se)
import os
from dotenv import load_dotenv
load_dotenv()

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["02_server.py"]   # apna calculator server
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected to server!")

            # yahi hai magic line - MCP tools ko LangChain tools bana deta hai
            # (humne pehle jo convert_tools_for_llm() manually likha tha,
            #  wo sab is EK line mein ho gaya)
            tools = await load_mcp_tools(session)

            print("Loaded tools:", [tool.name for tool in tools])
            # LangChain ka LLM wrapper, OpenRouter ke saath
            llm = ChatOpenAI(
                model="dots-studio/dots-3-note-preview:free",
                openai_api_key=os.getenv("OPENROUTER_API_KEY"),
                openai_api_base="https://openrouter.ai/api/v1"
            )

            # tools ko LLM se bind karo - bilkul Axis Retail Agent jaisa!
            llm_with_tools = llm.bind_tools(tools)

            # user ka sawal bhejo
            response = await llm_with_tools.ainvoke("What is 15 plus 27?")

            print("LLM Response:", response.content)
            print("Tool calls:", response.tool_calls)
            if response.tool_calls:
                tc = response.tool_calls[0]
                result = await session.call_tool(tc['name'], tc['args'])
                print("Final Result:", result.content)

asyncio.run(main())
import asyncio
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

#function to convert llm readable formatt
# MCP se mila hua tool list lo, aur OpenAI format mein convert karo
def convert_tools_for_llm(mcp_tools):
    # mcp_tools.tools -> MCP se mili tools ki list
    openai_tools = []

    for tool in mcp_tools.tools:
        # har tool ko is structure mein daalna hai (OpenAI ka required format)
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,                    # jaise "add"
                "description": tool.description,       # docstring wala text
                "parameters": tool.inputSchema          # a, b jaise parameters ka schema
            }
        })

    return openai_tools

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["02_server.py"]
    )
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read,write) as (session):
            await session.initialize()
            print("Connected to server!")

            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])
            
            # MCP tools ko LLM-readable format mein convert karo
            llm_tools = convert_tools_for_llm(tools)

            # OpenRouter client banao (OpenAI package use karke)
            from openai import OpenAI
            import os
            from dotenv import load_dotenv
            load_dotenv()

            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY")
            )

            # User ka message
            user_message = "What is 15 mul 27?"

            # LLM ko message + tools bhejo
            response = client.chat.completions.create(
                model="dots-studio/dots-3-note-preview:free",   # ya jo model aap use kar rahe the
                messages=[{"role": "user", "content": user_message}],
                tools=llm_tools
            )

            print(response.choices[0].message)

            #Abh llm ka decision ly kar tool chalana hai bs

            # LLM ne kaunsa tool maanga, wo nikalo
            message = response.choices[0].message

            if message.tool_calls:
                # pehla tool call lo (abhi ke liye ek hi maan rahe hain)
                tool_call = message.tool_calls[0]

                tool_name = tool_call.function.name          # "add"
                import json
                tool_args = json.loads(tool_call.function.arguments)  # {"a": 15, "b": 27}

                print(f"LLM wants to call: {tool_name} with {tool_args}")

                # ab MCP server se ye tool actually call karo
                result = await session.call_tool(tool_name, tool_args)

                print("Final Result:", result.content)
asyncio.run(main())
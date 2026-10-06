"""
Asynchronus func is and its syntax is different from normal func
Jo function await use kare, uske upar async def likhna zaroori hai
async def my_function():        #async use hoga 
    result = await something()  #await use hoga
asyncio.run(my_function())      # ye chahiye hota hai to call func
"""
import asyncio
# asyncio: MCP client "async" hota hai (ek kaam ka wait karte hue
# doosra kaam bhi chal sakta hai) - isko run karne ke liye zaroori hai

from mcp import ClientSession, StdioServerParameters
# ClientSession: server ke saath "conversation" banata hai,
#                isi se hum tools call karenge
# StdioServerParameters: batata hai kaunsa server chalana hai aur kaise

from mcp.client.stdio import stdio_client
# stdio_client: asal connection banata hai server ke saath
#               (stdio transport use karke)
async def main():
    # server_params: batata hai konsa server chalana hai
    # command="python" -> python se chalega
    # args=["01_server.py"] -> ye file run hogi (aapka calculator server)
    server_params = StdioServerParameters(
        command="python",
        args=["02_server.py"]
    )

    # stdio_client: server ko start karta hai aur connection khol deta hai
    # "async with" -> connection khulti hai, kaam khatam hone pe khud band ho jati hai
    async with stdio_client(server_params) as (read, write):

        # ClientSession: connection ke upar ek "session" banata hai
        # taake hum tools call kar sakein
        async with ClientSession(read, write) as session:

            # initialize(): session ko server ke saath "handshake" karwata hai
            # (dono ek doosre ko confirm karte hain "haan hum baat kar sakte hain")
            await session.initialize()
            print("Connected to server!")

            # list_tools(): server se poochta hai "tumhare paas konse tools hain?"
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])

            # call_tool(): actual tool ko call karta hai
            # "add" -> tool ka naam
            # {"a": 5, "b": 3} -> parameters (dictionary format mein)
            result = await session.call_tool("add", {"a": 5, "b": 3})
            sub=await session.call_tool("sub",{"a":5,"b":3})
            print("Result:", result.content)
            print("Result:", sub.content)

# Sabse end mein, ye async function ko chalata hai
asyncio.run(main())

#abhi ye ham client manuall use kar rahy hai abhi ham isko llm ky sath connect kar ky use kary gai next ta ky ai khud decide kary osko konsa tool use karna hai

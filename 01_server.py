from mcp.server.fastmcp import FastMCP  #FastMCP is a helper class and it handles complex protocol we only need to define tools
mcp = FastMCP("calculator")  #server object banaya

#now make add tool
@mcp.tool() #decorator
def add(a:int , b:int) ->int:  #normal python func
    """Add two numbers together""" #it is a docstring and very imp in mcp bcz it is the text that AI/LLM will see to decide when to use tool
    return a+b 
#it starts the server
if __name__ == "__main__":
    mcp.run()

"""
after this we use a command of node js in terminal so we can test our tool:
   Kaise kaam karta hai: Inspector ek chhota tool hai jo browser mein khulta hai, aapke server se connect hota hai, aur aap wahan se tools test kar sakte ho
  command: npx @modelcontextprotocol/inspector python 01_server.py (put here the name of file u run like now i want to run 01_server.py)
"""
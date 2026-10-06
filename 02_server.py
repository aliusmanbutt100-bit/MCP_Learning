#in previous we only make one add tool but now we r going to make server with 2 or more tools
from mcp.server.fastmcp import FastMCP
app=FastMCP("calculator") #ye ik server bana hai app name ka isme 4 tool hai add,sub,mul,div 
@app.tool() #add tool
def add(a:int,b:int)->int:
    "add two numbers together"
    return a+b
@app.tool() #sub tool
def sub(a:int,b:int)->int:
    "subtract two numbers together"
    return a-b
@app.tool() #multi tool
def mul(a:int,b:int)->int:
    "multiply two numbers together"
    return a*b
@app.tool() #divide tool
def divide(a:int,b:int)->int:
    "divide two numbers together"
    return a/b
#this helps us to run our server (app) server
if __name__=="__main__":
    app.run()
    # npx @modelcontextprotocol/inspector python 02_server.py
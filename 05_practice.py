from mcp.server.fastmcp import FastMCP
app=FastMCP("calculator")
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
#now we add a resource
@app.resource("store://timings")
def get_store_timings() -> str:
    """Store's operating hours"""
    return "Open Monday to Saturday, 10 AM to 9 PM"
#now add a prompt
@app.prompt()
def order_summary_prompt(items: str) -> str:
    """Generate a prompt to summarize a customer's order"""
    return f"Summarize this order clearly for the customer: {items}"
#now to run server
if __name__=="__main__":
    app.run()
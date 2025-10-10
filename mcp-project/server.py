from fastmcp import FastMCP
import os



# # 设置环境变量禁用代理
# os.environ["HTTP_PROXY"] = ""
# os.environ["HTTPS_PROXY"] = ""

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
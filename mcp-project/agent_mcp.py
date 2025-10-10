# --- 第一步：安装和导入 ---
# 确保所有库都是最新版本
# !pip install -U langchain langchain_google_genai fastmcp langchain_mcp_adapters langgraph

import os
import getpass
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

# --- 第二步：配置环境 ---
if 'GOOGLE_API_KEY' not in os.environ:
    os.environ['GOOGLE_API_KEY'] = getpass.getpass('Enter your Google API Key: ')



# --- 第三步：初始化大脑、工具和 Prompt ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


# 设置环境变量禁用代理
# os.environ["HTTP_PROXY"] = ""
# os.environ["HTTPS_PROXY"] = ""
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

# 创建 MCP 客户端
async def setup_agent():
    # 使用 MultiServerMCPClient 连接到 MCP 服务器
    client = MultiServerMCPClient(
        {
            "greet_service": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )
    
    # 获取 MCP 工具
    tools = await client.get_tools()

    # 使用 create_react_agent 创建 agent
    agent = create_react_agent(
        llm,
        tools
    )
    
    
    
    return agent

# --- 第四步：运行 Agent ---
async def main():
    agent = await setup_agent()
    
    # 初始化对话历史
    chat_history = []
    
    # 第一个问题
    question1 = "调用greet工具向张三问好"
    
    # 调用 agent
    response1 = await agent.ainvoke({
        "messages": [
          {
            "role": "user", 
            "content": question1
          }
        ]
    })
    
    # 打印出 Agent 的回答
    print("\nUser Question 1:", question1)
    
    # 从响应中提取最后一条消息的内容
    if "messages" in response1:
        last_message = response1["messages"][-1]
        agent_answer = last_message.content
        print("Agent Answer 1:", agent_answer)
    else:
        print("Agent Answer 1:", response1)  # 打印整个响应以便调试
    
    # 更新对话历史
    chat_history.extend([
        HumanMessage(content=question1),
        last_message  # 直接添加 AIMessage 对象
    ])

if __name__ == "__main__":
    asyncio.run(main())

from browser_use import Agent, ChatGoogle,Browser
from dotenv import load_dotenv
import asyncio
# from google.colab import userdata # Import userdata

import os
import getpass

# ## NEST ASYNCIO FIX ## 导入并应用nest_asyncio补丁
# import nest_asyncio
# nest_asyncio.apply()


load_dotenv()

# Email_Address = userdata.get('Email_Address')
# Password = userdata.get('Password')


if 'Email_Address' not in os.environ:
    os.environ['Email_Address'] = getpass.getpass('Enter your Email_Address: ')
if 'Password' not in os.environ:
    os.environ['Password'] = getpass.getpass('Enter your Password: ')



async def main():
    # Get the API key from Colab secrets and pass it to ChatGoogle
    
    if 'GOOGLE_API_KEY' not in os.environ:
        os.environ['GOOGLE_API_KEY'] = getpass.getpass('Enter your Google API Key: ')

    llm = ChatGoogle(model="gemini-2.5-flash", api_key='GOOGLE_API_KEY')



    # 使用 f-string 创建带有真实值的任务指令
    #    注意 {Email_Address} 和 {Password} 这两个占位符
    # 优化任务指令，给予AI更大的灵活性和自主权
    task = f"""
        **最终目标：登录Hunter.io，搜索OpenAI公司的员工信息并报告。**

        **详细步骤：**
        1. 导航至 https://hunter.io/ 并点击 "Log in" 按钮进入登录页面。
        2. 使用以下凭据进行登录：
           - 邮箱: "{Email_Address}"
           - 密码: "{Password}"
        3. **关键步骤：** 登录过程中，你可能会遇到Cloudflare的安全验证。**请仔细观察屏幕。** 这个验证可能是自动的，你只需要耐心等待几秒钟。如果出现任何需要交互的元素（例如需要点击的复选框），请执行交互。如果多次尝试后仍然无法登录（例如页面提示密码错误或持续卡在验证页面），请终止任务并报告遇到的具体问题。
        4. 成功登录后，导航至 https://hunter.io/discover 页面。
        5. 在 "Company name" 输入框中输入 "openai.com"，然后从下拉建议中选择 "openai.com"。
        6. 在出现的公司列表中，点击 "OpenAI" 公司的主页链接。
        7. 提取并以列表形式报告页面上所有能看到的员工姓名和职位。
        """

    # Connect to your existing Chrome browser
    browser = Browser(
        headless=False
    )

    agent = Agent(task=task,browser=browser, llm=llm)

    history = await agent.run()
    return history


if __name__ == "__main__":
    history = asyncio.run(main())
    print(history)

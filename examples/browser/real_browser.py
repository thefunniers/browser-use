import asyncio
import os
import sys
import requests
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, Browser, ChatGoogle

# 尝试连接 Chrome 的调试接口
url = "http://127.0.0.1:9222/json/version"
ws_url = None
print(f"Checking connection to: {url} ...")

try:
    response = requests.get(url, timeout=3)
    print(f"✅ 状态码: {response.status_code}")
    print(f"📄 返回内容: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        ws_url = data.get("webSocketDebuggerUrl")
        print(f"🚀 成功！WS地址是: {ws_url}")
    else:
        print("❌ 连上了，但是 Chrome 返回了错误的状态码。")

except requests.exceptions.ConnectionError:
    print("❌ 无法连接。原因可能是：")
    print("1. Chrome 没开，或者已经退出了。")
    print("2. 端口号不对（你启动时用的是 9222 吗？）。")
    print("3. 防火墙拦截了 localhost 通信。")
except json.JSONDecodeError:
    print("❌ 连上了，但返回的不是 JSON。")
    print("这通常是因为你通过浏览器直接访问过这个地址，导致 Chrome 卡住了。")
except Exception as e:
    print(f"❌ 发生未知错误: {e}")

# REAL_CHROME_WS = "ws://127.0.0.1:9222/devtools/browser/ee297f2b-2090-45d0-8583-713104e2d8c7"
os.environ["GOOGLE_API_KEY"] = "AIzaSyBlCsfwmfPaag2Lz1uG9nNVstx2ZaoMWEU"
# Connect to your existing Chrome browser
browser = Browser(
	cdp_url= ws_url
)


# NOTE: You have to close all Chrome browsers before running this example so that we can launch chrome in debug mode.
async def main():
	# save storage state
	agent = Agent(
		llm=ChatGoogle(model='gemini-3-pro-preview',
				 api_key=os.getenv("GOOGLE_API_KEY"),
				 thinking_level= 'high',
				 ),
		# Google blocks this approach, so we use a different search engine
		task='I need to organize a business lunch for 5 people in San Francisco next Tuesday. Use Yelp to find three highly-rated Italian restaurants that accept reservations. You must verify their menus to ensure they offer at least two vegetarian main course options. Analyze the recent reviews to determine which of these three is described as the "quietest" or best for business meetings. Once selected, navigate to its reservation page and proceed as far as possible without clicking the final "Confirm" or "Book" button. Report back with the restaurant name, the vegetarian options found, and a summary of why it was chosen.',
		browser=browser,
	)
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())

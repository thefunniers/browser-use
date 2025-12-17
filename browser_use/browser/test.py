import requests
import json

# 尝试连接 Chrome 的调试接口
url = "http://127.0.0.1:9222/json/version"

print(f"Checking connection to: {url} ...")

try:
    response = requests.get(url, timeout=3)
    print(f"✅ 状态码: {response.status_code}")
    print(f"📄 返回内容: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        ws_url = data.get("webSocketDebuggerUrl")
        print(f"\n🚀 成功！WS地址是: {ws_url}")
        print("请把上面这个 ws:// 开头的地址复制下来！")
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
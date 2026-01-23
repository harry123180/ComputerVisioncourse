import requests
import json

# 根據截圖 image_4f7ce2.png，確認埠號為 8080
url = "http://127.0.0.1:8080/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    # 使用你截圖中的第一個 Key
    "Authorization": "Bearer your-api-key-1"
}

data = {
    "model": "claude-3-5-sonnet",
    "messages": [{"role": "user", "content": "驗證成功，請跟我打個招呼。"}],
    "stream": False
}

try:
    print(f"正在使用 your-api-key-1 請求 API...")
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)

    print(f"狀態碼: {response.status_code}")
    print(f"回應內容: {response.text[:500] if response.text else '(空)'}")

    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        print("\n--- 驗證成功 ---")
        print(f"Claude 回覆：\n{content}")
    else:
        print(f"\n--- 驗證失敗 --- 狀態碼: {response.status_code}")
        print("回傳訊息：", response.text)
        print("提示：請確認你是否已經在 EasyCLI 主畫面點擊了右下角的 Apply 按鈕。")
except Exception as e:
    print("\n--- 發生連線錯誤 ---")
    print("錯誤詳情：", e)

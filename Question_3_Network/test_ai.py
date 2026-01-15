import ollama

print("正在測試連線到 Ollama...")

try:
    # 嘗試送出一個簡單的 "hi"
    response = ollama.chat(model='llama3', messages=[
        {'role': 'user', 'content': 'hi'}
    ])
    print("✅ 成功！Ollama 回覆了：")
    print(response['message']['content'])

except Exception as e:
    print("❌ 失敗！錯誤原因如下：")
    print(e)
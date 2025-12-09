# 第三章：高级特性 (Advanced Features)

本章介绍 FastAPI 的高级功能：后台任务 (Background Tasks) 和 WebSocket。

## 1. 后台任务 (Background Tasks)

文件：`background_tasks.py`

有时候你需要在请求返回后执行一些操作（如发送邮件、处理数据），但不想让用户等待。`BackgroundTasks` 可以轻松实现这一点。

```python
def write_notification(email: str, message=""):
    # 模拟耗时操作
    ...

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```

### 运行
```bash
fastapi dev background_tasks.py
```
访问 `/send-notification/test@example.com`，你会立即收到响应，而 `log.txt` 会在后台被写入。

## 2. WebSockets

文件：`websockets_app.py`

FastAPI 原生支持 WebSockets，适合构建实时聊天、通知推送等应用。

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

### 运行
```bash
fastapi dev websockets_app.py
```
然后打开浏览器访问 `http://127.0.0.1:8000`。你将看到一个简单的聊天界面，发送的消息会通过 WebSocket 回显。

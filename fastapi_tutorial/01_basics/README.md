# 第一章：基础 (Basics)

本章介绍 FastAPI 的最基础功能：如何创建一个应用，处理路径参数、查询参数，以及如何使用 Pydantic 模型处理请求体。

## 1. 核心概念

- **FastAPI 实例**: `app = FastAPI()` 是所有 API 功能的入口。
- **路径操作装饰器**: `@app.get("/")` 告诉 FastAPI 当用户访问 `/` 路径时执行下方的函数。
- **路径参数**: 如 `/items/{item_id}` 中的 `item_id`。
- **查询参数**: 函数参数中未在路径中声明的参数，如 `q`。
- **请求体**: 使用 Pydantic 模型 (`BaseModel`) 定义。

## 2. 代码解析 (`main.py`)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 定义数据模型
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

# 根路径
@app.get("/")
def read_root():
    return {"Hello": "World"}

# 路径参数和查询参数
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# 请求体处理
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

## 3. 运行方法

在终端中执行以下命令（确保已安装 `fastapi[standard]` 或 `uvicorn`）：

```bash
fastapi dev main.py
```

或者使用 uvicorn 直接运行：

```bash
uvicorn main:app --reload
```

## 4. 测试 API

启动服务后，访问自动生成的交互式文档：
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

你可以尝试：
1. 发送 GET 请求到 `/items/5?q=somequery`
2. 发送 PUT 请求到 `/items/5`，并附带 JSON Body:
   ```json
   {
       "name": "Foo",
       "price": 3.5
   }
   ```

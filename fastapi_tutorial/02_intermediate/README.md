# 第二章：中级 (Intermediate)

本章介绍 FastAPI 的核心特性：依赖注入系统，以及如何结合 SQL 数据库使用。

## 1. 依赖注入 (Dependencies)

文件：`dependencies.py`

FastAPI 拥有强大的依赖注入系统。依赖项可以是一个函数，它在路径操作函数执行前运行，可以处理认证、数据库连接、共享逻辑等。

```python
# 定义依赖
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# 使用依赖
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

### 运行
```bash
uv run fastapi dev dependencies.py
```

## 2. 数据库集成 (SQL Databases)

文件：`database_app.py`

此示例展示了如何在一个文件中集成 SQLAlchemy (ORM) 和 SQLite。

### 主要组件：
1.  **Engine & Session**: 数据库连接管理。
2.  **Models (SQLAlchemy)**: 定义数据库表结构。
3.  **Schemas (Pydantic)**: 定义 API 请求和响应的数据格式。
4.  **Dependency (`get_db`)**: 创建数据库会话，并在请求结束后关闭它。

### 运行

确保已安装 SQLAlchemy：
```bash
uv add sqlalchemy
```
*(如果按照根目录 `pyproject.toml` 设置，则无需单独安装)*

运行应用：
```bash
uv run fastapi dev database_app.py
```

这将会在当前目录下创建一个 `test.db` 文件。

### 测试
1. POST `/users/` 创建用户：
   ```json
   { "email": "user@example.com" }
   ```
2. GET `/users/1` 获取用户信息。

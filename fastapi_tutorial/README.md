# FastAPI 完整教程 (从入门到精通)

这份教程旨在帮助你快速掌握 FastAPI，从基础概念到高级特性，并包含可直接运行的代码示例。

## 目录

1. [第一章：基础 (Basics)](./01_basics/README.md)
   - Hello World
   - 路径参数 & 查询参数
   - 请求体与 Pydantic
2. [第二章：中级 (Intermediate)](./02_intermediate/README.md)
   - 依赖注入系统
   - 数据库集成 (SQLAlchemy + SQLite)
3. [第三章：高级特性 (Advanced)](./03_advanced/README.md)
   - 后台任务 (Background Tasks)
   - WebSockets (实时通信)
4. [第四章：部署 (Deployment)](./04_deployment/README.md)
   - Docker 容器化

## 环境准备

本教程基于 Python 3.10+。请确保安装了依赖：

```bash
pip install "fastapi[standard]"
```

## 如何使用本教程

每个章节都有对应的文件夹（如 `01_basics`），其中包含：
- `.py` 源代码文件：可直接运行。
- `README.md`：该章节的详细讲解。

建议按照目录顺序学习，并亲自运行代码体验。

## 官方文档

本教程参考了 [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)，那是获取最新、最详细信息的最佳来源。

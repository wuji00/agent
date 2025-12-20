# 开发笔记

## 任务目标
参考 `anthropics/claude-quickstarts` 仓库，使用 LangChain 和 LangGraph 实现以下四个演示：
1. Customer Support Agent
2. Financial Data Analyst
3. Computer Use Demo
4. Autonomous Coding Agent

## 实现过程

### 1. 环境搭建
- 使用 `uv` 初始化项目。
- 依赖项包括：`langchain`, `langgraph`, `langchain-anthropic`, `langchain-community`, `faiss-cpu`, `langchain-huggingface` 等。

### 2. Customer Support Agent
- **参考**: 原项目是一个 Next.js 应用，使用 Bedrock Knowledge Base。
- **实现**: 使用 `LangGraph` 构建状态图。
- **RAG**: 使用 `FAISS` 和 `HuggingFaceEmbeddings` (all-MiniLM-L6-v2) 实现本地检索。
- **逻辑**: 检索上下文 -> 构建 Prompt (包含分类逻辑) -> 调用 Claude -> 输出 JSON。
- **问题**: 本地运行需要下载 Embedding 模型，初次运行可能较慢。

### 3. Financial Data Analyst
- **参考**: 原项目使用 React 前端展示图表。
- **实现**: 使用 `create_react_agent` 构建 ReAct 代理。
- **工具**: 模拟了 `get_stock_price` 和 `get_company_financials` 工具。
- **交互**: 命令行交互，代理可以查询多个工具并回答问题。

### 4. Computer Use Demo
- **参考**: 原项目是一个复杂的 Docker 环境，通过 API 控制 VNC。
- **实现**: 模拟了 "Computer Use" 的工具调用结构。
- **工具**: 定义了 `computer_tool` (模拟屏幕操作), `bash_tool`, `edit_tool`。
- **注意**: 使用了 `anthropic-beta: computer-use-2024-10-22` header 来启用 Beta 功能。由于没有真实的 GUI 环境，工具返回模拟结果。

### 5. Autonomous Coding Agent
- **参考**: 使用 Claude Agent SDK。
- **实现**: 使用 `LangGraph` 的 `create_react_agent`。
- **工具**: 提供了 `list_files`, `read_file`, `write_file` 工具，限制在 `workspace` 目录下操作以保证安全。

## 总结
成功将四个不同类型的 Claude 应用逻辑移植到了 LangChain/LangGraph 框架下。为了简化演示和依赖，部分外部服务（如 AWS Bedrock, 真实股票 API, GUI 环境）进行了本地化模拟或简化。

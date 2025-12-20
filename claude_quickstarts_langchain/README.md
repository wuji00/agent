# Claude LangChain Quickstarts (中文版)

这个仓库包含使用 LangChain and LangGraph 实现的四个 Claude Quickstart 示例。

## 目录

1. [环境设置](#环境设置)
2. [Customer Support Agent (客户支持代理)](#customer-support-agent)
3. [Financial Data Analyst (金融数据分析师)](#financial-data-analyst)
4. [Autonomous Coding Agent (自主编码代理)](#autonomous-coding-agent)
5. [Computer Use Demo (电脑操作演示)](#computer-use-demo)

## 环境设置

使用 `uv` 管理依赖：

```bash
uv sync
```

确保你设置了 `ANTHROPIC_API_KEY` 环境变量。

## Customer Support Agent

这是一个使用 RAG (检索增强生成) 的客户支持代理。它使用 ChromaDB 作为向量存储，并根据用户的情绪和问题类别生成结构化的 JSON 响应。

**运行方法:**
```bash
python customer_support/main.py
```

## Financial Data Analyst

这是一个金融数据分析师代理，可以使用工具获取股票价格 (yfinance) 并生成图表数据。

**运行方法:**
```bash
python financial_analyst/main.py
```

## Autonomous Coding Agent

这是一个自主编码代理，采用了多阶段流程：
1. **Initializer**: 将用户请求分解为功能列表 (JSON)。
2. **Planner**: 规划下一个要执行的任务。
3. **Coder**: 使用文件系统和 Shell 工具执行任务。

**运行方法:**
```bash
python autonomous_coding/main.py
```
*注意：代码将在 `autonomous_coding/workspace` 目录中执行。*

## Computer Use Demo

这是一个电脑操作代理的模拟实现。它定义了 `computer` (鼠标/键盘), `bash`, `str_replace_editor` 工具的接口，并使用 LangGraph 驱动代理循环。由于没有实际的 GUI 环境，工具执行是模拟的。

**运行方法:**
```bash
python computer_use/main.py
```

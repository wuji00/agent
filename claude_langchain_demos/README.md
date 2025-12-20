# Claude LangChain Demos (中文版)

本项目包含了四个使用 [LangChain](https://www.langchain.com/) 和 [LangGraph](https://langchain-ai.github.io/langgraph/) 实现的 Claude 示例应用。
代码参考自 [anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts)，旨在展示如何使用 LangChain 生态系统复现这些功能。

## 目录

1.  [环境设置](#环境设置)
2.  [Customer Support Agent (客户支持代理)](#customer-support-agent)
3.  [Financial Data Analyst (金融数据分析师)](#financial-data-analyst)
4.  [Computer Use Demo (电脑操作演示)](#computer-use-demo)
5.  [Autonomous Coding Agent (自主编程代理)](#autonomous-coding-agent)

## 环境设置

本项目使用 `uv` 进行依赖管理。请确保已安装 `uv`。

1.  进入项目目录：
    ```bash
    cd claude_langchain_demos
    ```

2.  安装依赖：
    ```bash
    uv sync
    ```

3.  配置 API Key：
    复制 `.env.example` 为 `.env` 并填入你的 Anthropic API Key。
    ```bash
    cp .env.example .env
    ```
    编辑 `.env` 文件：
    ```
    ANTHROPIC_API_KEY=sk-ant-api03-...
    ```

## 演示说明

所有演示均通过命令行运行。

### Customer Support Agent (客户支持代理)

这是一个 RAG (检索增强生成) 应用。它会加载本地的一个文本文件作为知识库（模拟 Anthropic 的文档），检索相关信息来回答用户的客户支持问题，并同时对问题进行分类。

**运行方式：**
```bash
uv run python customer_support/main.py
```

**示例输入：**
- "How do I update my billing info?" (我该如何更新账单信息？)
- "What is Claude?" (Claude 是什么？)

### Financial Data Analyst (金融数据分析师)

这是一个能够调用工具获取股票价格和公司信息的智能代理。为了演示方便，这里使用了模拟的股票数据工具。

**运行方式：**
```bash
uv run python financial_analyst/main.py
```

**示例输入：**
- "What is the stock price of Apple?" (苹果的股价是多少？)
- "Compare the PE ratio of MSFT and AAPL." (比较微软和苹果的市盈率。)

### Computer Use Demo (电脑操作演示)

演示了 Claude 如何通过 Computer Use API (Beta) 来控制电脑。由于在无头环境中运行，本项目模拟了计算机交互工具。

**运行方式：**
```bash
uv run python computer_use/main.py
```

**示例输入：**
- "Take a screenshot of the current screen." (截取当前屏幕。)
- "Move the mouse to the start button and click." (移动鼠标到开始按钮并点击。)

### Autonomous Coding Agent (自主编程代理)

这是一个可以读写文件的编程代理，模拟了自主编码的能力。为了安全起见，文件操作限制在 `autonomous_coding/workspace/` 目录下。

**运行方式：**
```bash
uv run python autonomous_coding/main.py
```

**示例输入：**
- "Create a file named hello.py that prints 'Hello, LangChain!'." (创建一个名为 hello.py 的文件，内容是打印 'Hello, LangChain!'。)
- "List all files in the workspace." (列出工作区的所有文件。)

## 项目结构

```
claude_langchain_demos/
├── customer_support/    # 客户支持代理 (RAG + LangGraph StateGraph)
├── financial_analyst/   # 金融分析师 (ReAct Agent)
├── computer_use/        # 电脑操作 (Computer Use Tools)
├── autonomous_coding/   # 自动编程 (File Tools)
├── pyproject.toml       # 依赖配置
├── notes.md             # 开发笔记
└── README.md            # 说明文档
```

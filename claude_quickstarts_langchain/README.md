# Claude Quickstarts (LangChain Edition)

这个存储库包含了 [anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts) 中四个演示的 LangChain 和 LangGraph 实现。

每个演示都位于自己的目录中，并包含 README.md 说明。

## 目录

1. **[客户支持代理 (Customer Support Agent)](./customer_support_agent)**
   - 使用 RAG 和结构化输出来处理客户查询。
2. **[金融数据分析师 (Financial Data Analyst)](./financial_data_analyst)**
   - 分析数据并生成图表配置。
3. **[自动编码代理 (Autonomous Coding Agent)](./autonomous_coding_agent)**
   - 能够编写代码、运行测试和管理项目的自主代理。
4. **[计算机使用演示 (Computer Use Demo)](./computer_use_demo)**
   - 展示 Claude 3.5 Sonnet 的计算机使用能力（模拟环境）。

## 依赖

安装所有依赖：

```bash
uv pip install -r requirements.txt
```

## 使用方法

进入每个目录并按照其 README 中的说明运行 `main.py`。
您需要设置 `ANTHROPIC_API_KEY` 环境变量。

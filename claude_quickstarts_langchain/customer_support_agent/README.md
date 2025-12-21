# 客户支持代理 (Customer Support Agent)

这是一个使用 LangChain 和 LangGraph 实现的客户支持代理示例。它模拟了参考代码中的功能，包括 RAG（检索增强生成）和结构化 JSON 输出。

## 功能

- **RAG**: 使用本地知识库（`knowledge_base.txt`）回答有关 Anthropic 产品的查询。
- **结构化输出**: 代理返回包含思考过程、用户情绪、建议问题等信息的 JSON。
- **分类**: 自动将查询分类到预定义的类别中。
- **重定向**: 如果查询超出范围，建议重定向到人工代理。

## 安装

确保已安装项目根目录下的 `requirements.txt` 中的依赖项。

```bash
uv pip install -r ../requirements.txt
```

## 运行

设置 `ANTHROPIC_API_KEY` 环境变量，然后运行 `main.py`：

```bash
export ANTHROPIC_API_KEY=your_key_here
python main.py
```

## 文件说明

- `graph.py`: 定义 LangGraph 状态图和节点逻辑。
- `main.py`: CLI 入口点，处理用户输入并调用图。
- `customer_support_categories.json`: 客户支持类别定义。
- `knowledge_base.txt`: 模拟的知识库内容。

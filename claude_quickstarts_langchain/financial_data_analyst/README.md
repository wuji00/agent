# 金融数据分析师 (Financial Data Analyst)

这是一个使用 LangChain 和 LangGraph 实现的金融数据分析师代理示例。它模拟了参考代码中的功能，能够分析上传的文本或图像数据，并生成图表数据。

## 功能

- **多模态输入**: 支持文本和图像文件（通过文件路径输入）。
- **数据分析**: 使用 Claude 3.5 Sonnet 分析金融数据。
- **图表生成**: 通过 `generate_graph_data` 工具生成结构化的 JSON 图表配置。

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

在提示时，您可以输入文本问题，或输入本地文件的路径（如 `data.csv`, `chart.png`）来让代理分析。

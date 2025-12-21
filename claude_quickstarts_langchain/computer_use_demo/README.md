# 计算机使用演示 (Computer Use Demo)

这是一个使用 LangChain 和 LangGraph 实现的计算机使用演示。

**注意**: 由于在沙箱环境中无法运行真实的 GUI 环境，本演示使用模拟工具（Mock Tools）。代理会发出操作指令（如移动鼠标、点击、键入），工具会记录这些操作并返回模拟结果，但不会在真实屏幕上执行。

## 功能

- **Computer Tool**: 模拟鼠标和键盘操作。
- **Bash Tool**: 执行 Bash 命令。
- **Editor Tool**: 编辑文件。

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

您可以尝试要求代理执行操作，例如 "打开 Firefox 并搜索 Anthropic"。代理将生成相应的鼠标和键盘操作指令。

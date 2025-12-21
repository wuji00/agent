# 自动编码代理 (Autonomous Coding Agent)

这是一个使用 LangChain 和 LangGraph 实现的自动编码代理。它包含两个阶段：初始化（Initializer）和编码（Coding）。

## 工作流程

1. **初始化阶段**: 如果 `workspace` 目录下没有 `feature_list.json`，代理将读取 `app_spec.txt` 并生成详细的功能列表（`feature_list.json`）和初始化脚本。
2. **编码阶段**: 如果存在 `feature_list.json`，代理将读取它，选择下一个未完成的功能，编写代码，运行测试（模拟），并更新 `feature_list.json`。

## 功能

- **文件操作**: 代理可以读写文件。
- **命令执行**: 代理可以在 `workspace` 目录中执行 Bash 命令（如 git, ls, npm install 等）。
- **状态持久化**: 进度保存在文件系统中（`feature_list.json`, `claude-progress.txt`）。

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

每次运行 `main.py` 都会执行一个会话。您可以多次运行它来逐步构建项目。

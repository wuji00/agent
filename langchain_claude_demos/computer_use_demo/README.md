# Computer Use Demo

This demo implements the Computer Use capabilities using LangChain and LangGraph.

**Note:** This demo is intended to be run in an environment where Anthropic's Computer Use tools are available or mocked. Since this is a sandbox environment without a GUI, the tools are mocked to log actions instead of executing them.

## Features

-   **Computer Use Tools:** Integrates `computer`, `bash`, and `str_replace_editor` tools.
-   **LangGraph Loop:** Manages the agent loop, handling tool calls and API responses.

## Setup

1.  Dependencies:
    ```bash
    pip install langchain langchain-anthropic langchain-community langgraph
    ```
2.  Set `ANTHROPIC_API_KEY`.

## Usage

Run the demo:

```bash
python computer_use_demo.py
```

# Browser Use Demo

This demo implements the Browser Use capabilities using LangChain and LangGraph.

**Note:** This demo mocks the browser interactions (Playwright) as it runs in a headless sandbox environment.

## Features

-   **Browser Tools:** Mocks `navigate`, `click`, `type`, `scroll`, etc.
-   **Agent Loop:** Handles interactions with the browser.

## Setup

1.  Dependencies:
    ```bash
    pip install langchain langchain-anthropic langchain-community langgraph
    ```
2.  Set `ANTHROPIC_API_KEY`.

## Usage

Run the demo:

```bash
python browser_use_demo.py
```

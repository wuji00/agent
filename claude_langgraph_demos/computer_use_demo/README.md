# Computer Use Demo (Mock)

This directory contains a LangGraph implementation of the Computer Use Demo.

**Note:** This is a mock implementation. The tools log actions but do not execute them on the actual system (to prevent safety issues and because a full desktop environment is not available in this CLI sandbox).

## Running the Agent

You can run the agent interactively:

```bash
python agent.py
```

## Description

The agent uses the `computer-use-2024-10-22` beta capability (simulated by passing the header, though actual tool execution is mocked).
It includes tools for:
*   `computer`: Mouse/Keyboard control.
*   `bash`: Command execution.
*   `str_replace_editor`: File editing.

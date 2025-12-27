# Computer Use Demo

A demo of Claude's computer use capabilities, mocked for a headless environment.
It uses `claude-3-5-sonnet-20241022` with the `computer-use-2024-10-22` beta flag.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the agent:
   ```bash
   python agent.py
   ```

## Tools (Mocked)
- `computer_mouse_move`: Logs mouse movement.
- `computer_left_click`: Logs a click.
- `computer_type`: Logs typing.
- `computer_screenshot`: Logs a screenshot action.

This allows testing the agent's logic and tool invocation without needing a real GUI environment.

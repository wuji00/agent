# Browser Use Demo

A demo of browser automation powered by Claude, using mocked Playwright-like tools.

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
- `navigate_to_url`: Logs navigation.
- `click_element`: Logs clicks.
- `fill_input`: Logs input filling.
- `extract_text`: Logs text extraction.

This allows simulating browser interactions without needing a headless browser installed in the environment.

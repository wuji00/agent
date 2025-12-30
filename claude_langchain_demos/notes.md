# Development Notes

## Goal
Implement the following four demos from `anthropics/claude-quickstarts` using LangChain and LangGraph:
1. Customer Support Agent
2. Financial Data Analyst
3. Computer Use Demo
4. Autonomous Coding Agent

## Implementation Details

### 1. Environment Setup
- Project initialized with `uv`.
- Dependencies: `langchain`, `langgraph`, `langchain-anthropic`, `langchain-community`, `faiss-cpu`, `langchain-huggingface`, `sentence-transformers`, `python-dotenv`.
- Note: `langchain-openai` is intentionally excluded.

### 2. Customer Support Agent
- **Reference**: Originally a Next.js app with Bedrock Knowledge Base.
- **Implementation**: Used `StateGraph` from `langgraph`.
- **RAG**: Implemented local retrieval using `FAISS` and `HuggingFaceEmbeddings` (all-MiniLM-L6-v2).
- **Logic**: Retrieve context -> Build Prompt (with categorization instructions) -> Call Claude -> Output JSON.
- **Verification**: Verified `knowledge.txt` and `categories.json` are present and used. `agent.py` implements the flow correctly.

### 3. Financial Data Analyst
- **Reference**: Originally used React to display charts.
- **Implementation**: Used `create_react_agent` from `langgraph.prebuilt`.
- **Updates**: Added a system message to `agent.py` to instruct the model to output structured JSON for charting (compatible with Recharts) alongside text responses.
- **Tools**: Mocked `get_stock_price`, `get_company_financials`, `get_market_trends`.

### 4. Computer Use Demo
- **Reference**: Originally a complex Docker environment with VNC.
- **Implementation**: Simulated "Computer Use" tool call structure.
- **Configuration**: Enabled `anthropic-beta: computer-use-2024-10-22` header in `ChatAnthropic`.
- **Tools**: Implemented mock `computer_tool`, `bash_tool`, and `edit_tool` that log actions without execution, suitable for headless environments.

### 5. Autonomous Coding Agent
- **Reference**: Uses Claude Agent SDK.
- **Implementation**: Used `create_react_agent`.
- **Tools**: Implemented `list_files`, `read_file`, `write_file`, and `delete_file`.
- **Security**: Added path validation (`_is_safe_path`) to restrict operations to the `workspace` directory.

## Summary
Successfully verified and updated all four demos. Key improvements include adding structured JSON output for the Financial Analyst and ensuring the Autonomous Coding agent has a `delete_file` tool.

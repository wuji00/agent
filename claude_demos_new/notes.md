# Development Notes

## Goal
Implement four Claude Quickstarts demos using LangChain and LangGraph:
1. Customer Support Agent
2. Financial Data Analyst
3. Computer Use Demo
4. Autonomous Coding Agent

## Implementation Details

### Environment
- Python 3.11+
- Dependencies: `langchain`, `langgraph`, `langchain-anthropic`, `langchain-community`, `faiss-cpu`, `langchain-huggingface`.

### 1. Customer Support Agent
- **Location**: `customer_support/`
- **Logic**: Uses a `StateGraph` with a retrieval node (RAG) and a generation node.
- **RAG**: Implemented using `FAISS` and `HuggingFaceEmbeddings`.
- **Data**: Mocked knowledge base in `data/knowledge.txt` and categories in `data/categories.json`.
- **Tools**: None explicitly, but uses RAG as a retrieval mechanism.

### 2. Financial Data Analyst
- **Location**: `financial_analyst/`
- **Logic**: Uses `create_react_agent` (prebuilt ReAct agent).
- **Tools**: `generate_graph_data` (mocked).
- **Behavior**: The agent calls the tool to generate data for visualization. The tool returns the structure expected by a frontend.

### 3. Computer Use Demo
- **Location**: `computer_use/`
- **Logic**: Uses `create_react_agent`.
- **Tools**: `computer_tool`, `bash_tool`, `edit_tool`.
- **Behavior**: Mocks the tools to simulate computer interaction. `computer_tool` handles actions like `screenshot`, `mouse_move`, etc.
- **Configuration**: Uses `anthropic-beta: computer-use-2024-10-22` header.

### 4. Autonomous Coding Agent
- **Location**: `autonomous_coding/`
- **Logic**: Uses `create_react_agent`.
- **Tools**: `list_files`, `read_file`, `write_file`, `delete_file`.
- **Safety**: Tools are restricted to a `workspace` directory to prevent unauthorized file system access.

## Verification
- Each agent has a `__main__` block in `agent.py` for testing.
- Verified that agents attempt to call the API (verified via error logs due to missing/mock API key).
- Verified tool definitions and graph structures.

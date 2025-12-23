# Notes

## Plan
1.  Create directory `langchain_claude_demos` and `notes.md`.
2.  Implement `Customer Support Agent` demo using LangGraph.
3.  Implement `Financial Data Analyst` demo using LangGraph.
4.  Implement `Computer Use Demo` demo using LangGraph.
5.  Implement `Autonomous Coding Agent` demo using LangGraph.
6.  Write `README.md` summarizing the implementations and usage.

## Implementation Details

### Customer Support Agent
- Used `langchain` and `langgraph`.
- Implemented RAG using `FAISS` and `HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`) to avoid dependency on AWS Bedrock for the demo, making it runnable locally.
- Created `ingest.py` to index a dummy data file.
- Created `agent.py` which defines a StateGraph with:
    - `detect_mood`: Analyzes user sentiment.
    - `retrieve`: Fetches context from FAISS.
    - `generate`: Produces the final response using Claude.

### Financial Data Analyst
- Used `pandas` and `matplotlib`.
- Defined tools:
    - `get_financial_data`: Reads a CSV file.
    - `generate_plot`: Executes Python code to generate plots (simulated via `exec` for demo purposes, warned about safety).
- Used `ChatAnthropic` with `bind_tools`.
- Used `ToolNode` and `prebuilt` components from LangGraph.

### Computer Use Demo
- Since running a full Docker/VNC environment is out of scope for a simple script demo, I mocked the tools.
- Created `mock_tools.py` with `computer`, `bash`, and `str_replace_editor` tools that return string descriptions of actions.
- Implemented the agent loop using LangGraph to call these tools based on user input.

### Autonomous Coding Agent
- Modeled the "two-agent" pattern (Initializer + Coding Agent) using a single StateGraph with different nodes.
- `initializer` node: Sets up the project directory and creates a `feature_list.json`.
- `coding_agent` node: Iterates through the feature list and simulates implementation.
- `supervisor` logic: Determines transition between nodes and termination.

## Dependencies
- `langchain`
- `langgraph`
- `langchain-anthropic`
- `langchain-community`
- `faiss-cpu`
- `langchain-huggingface`
- `sentence-transformers`
- `pandas`
- `matplotlib`

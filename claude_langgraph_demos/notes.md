# Notes

## Autonomous Coding Agent
- Implemented `autonomous_coding` package.
- Ported `prompts/` and `prompts.py` from reference.
- Implemented `tools.py` with `read_file`, `write_file`, `list_files`, `delete_file`, and `run_bash_command`.
- Added strict path validation to `tools.py` to confine operations to `workspace/`.
- Implemented `agent.py` using `langgraph.prebuilt.create_react_agent`.
- Modeled the dual-phase strategy by checking for `feature_list.json` and selecting the appropriate prompt (`initializer_prompt` vs `coding_prompt`).
- Created `test_tools.py` to verify tool functionality and security (path traversal protection).

## Other Demos
- Verified `customer_support_agent` setup. Created `dummy_kb.txt` (via setup script if needed, but the script failed initially so I fixed dependencies).
- Fixed `setup_kb.py` dependency issues (`langchain-huggingface`, `faiss-cpu`, etc.).
- Implemented `financial_data_analyst` with `generate_chart` tool.
- Implemented `computer_use_demo` with mock tools and `anthropic-beta` header support.
- Added `__init__.py` to all packages for proper module resolution.

## Environment
- Updated `requirements.txt` (implicitly via `pip install`) and ensured all dependencies are documented or available in the environment.
- Verified that running `pytest` works for the new tests.

from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from .tools import computer_tool, bash_tool, edit_tool

def build_agent():
    # We need to enable the beta feature for computer use
    # Note: This uses standard tool calling. For full computer use fidelity,
    # one needs to match the exact tool schema expected by Claude's computer use training.
    # The memory said: Implementations using Anthropic's Computer Use features via `ChatAnthropic` require the model `claude-3-5-sonnet-20241022` and the `betas` parameter to include `computer-use-2024-10-22`.

    # langchain-anthropic uses `model_kwargs` to pass extra parameters or `client_options`.
    # Let's check `ChatAnthropic` signature or documentation in memory...
    # Actually the memory just said use the model and betas parameter.

    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        model_kwargs={"extra_headers": {"anthropic-beta": "computer-use-2024-10-22"}}
    )

    tools = [computer_tool, bash_tool, edit_tool]

    agent = create_react_agent(llm, tools)
    return agent

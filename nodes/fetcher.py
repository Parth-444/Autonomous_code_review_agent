import yaml
from typing import List

from pydantic import BaseModel, Field
from nodes.llm_client import llm
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

from graph.state import AgentState
from integrations.mcp_config import MCP_CONFIG


class ImportantFiles(BaseModel):
    """Schema for the list of important files selected for documentation."""

    important_files: List[str] = Field(
        description="List of relative file paths that are important for documentation generation."
    )


with open("prompts/important_files.yaml", "r") as f:
    p = yaml.safe_load(f)

llm_with_structured = llm.with_structured_output(ImportantFiles)


async def fetcher(state: AgentState):
    # Create client inside the async function so it shares the same event loop
    client = MultiServerMCPClient(MCP_CONFIG)
    tools = await client.get_tools()

    repo_tree_tool = next(t for t in tools if t.name == "get_repo_tree")
    get_file_content_tool = next(t for t in tools if t.name == "get_file_content")

    repo_tree = await repo_tree_tool.ainvoke({"repo_name": state["repo_name"]})

    messages = [
        SystemMessage(content=p["system"]),
        HumanMessage(content=p["user"].format(repo_tree=repo_tree)),
    ]

    response = await llm_with_structured.ainvoke(messages)
    important_files = response.important_files

    files_fetched = {}
    for filepath in important_files:
        file_content = await get_file_content_tool.ainvoke({"repo_name": state["repo_name"], "path": filepath})
        files_fetched[filepath] = file_content

    return {
        "repo_tree": repo_tree,
        "important_files": important_files,
        "files_fetched": files_fetched,
    }

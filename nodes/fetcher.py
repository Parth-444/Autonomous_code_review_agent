import os
import yaml
from typing import List

from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import AgentState
from integrations.mcp_config import tools


class ImportantFiles(BaseModel):
    """Schema for the list of important files selected for documentation."""

    important_files: List[str] = Field(
        description="List of relative file paths that are important for documentation generation."
    )


def initiate_fetcher():
    key = os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=key)

    with open("prompts/important_files.yaml", "r") as f:
        p = yaml.safe_load(f)

    llm_with_structured = llm.with_structured_output(ImportantFiles)
    repo_tree_tool = next(t for t in tools if t.name == "get_repo_tree")
    get_file_content_tool = next(t for t in tools if t.name == "get_file_content")

    return p, llm_with_structured, repo_tree_tool, get_file_content_tool


p, llm_with_structured, repo_tree_tool, get_file_content_tool = initiate_fetcher()


def fetcher(state: AgentState):
    repo_tree = repo_tree_tool(repo_name=state["repo_name"])

    messages = [
        SystemMessage(content=p["system"]),
        HumanMessage(content=p["user"].format(repo_tree=repo_tree)),
    ]

    response = llm_with_structured.invoke(messages)
    important_files = response.important_files

    files_fetched = {}
    for filepath in important_files:
        file_content = get_file_content_tool(repo_name=state["repo_name"], filepath=filepath)
        files_fetched[filepath] = file_content

    return {
        "repo_tree": repo_tree,
        "important_files": important_files,
        "files_fetched": files_fetched,
    }

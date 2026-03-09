import asyncio
import yaml
from typing import List

from pydantic import BaseModel, Field
from nodes.llm_client import llm
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import AgentState




with open("prompts/design.yaml", "r") as f:
    p = yaml.safe_load(f)


class DesignIssue(BaseModel):
    location: str = Field(description="File and function/class name where the issue exists")
    problem: str = Field(description="Description of the design issue")
    suggestion: str = Field(description="Concrete fix suggestion")


class DesignAnalysis(BaseModel):
    issues: List[DesignIssue] = Field(description="List of design issues found")


llm_with_structure = llm.with_structured_output(DesignAnalysis)


async def design_analyzer(state: AgentState):
    await asyncio.sleep(6)  # Stagger request
    messages = [
        SystemMessage(content=p["system"]),
        HumanMessage(content=p["user"].format(files_content=state["files_fetched"], repo_structure=state["repo_tree"])),
    ]

    response = await llm_with_structure.ainvoke(messages)

    return {"analysis_results": {"design": response.issues}}

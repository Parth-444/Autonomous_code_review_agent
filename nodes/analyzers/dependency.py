import asyncio
import yaml
from typing import List

from pydantic import BaseModel, Field
from nodes.llm_client import llm
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import AgentState




with open("prompts/dependency.yaml", "r") as f:
    p = yaml.safe_load(f)


class DependencyIssue(BaseModel):
    location: str = Field(description="File and function/class name where the issue exists")
    problem: str = Field(description="Description of the dependency issue")
    suggestion: str = Field(description="Concrete fix suggestion")


class DependencyAnalysis(BaseModel):
    issues: List[DependencyIssue] = Field(description="List of dependency issues found")


llm_with_structure = llm.with_structured_output(DependencyAnalysis)


async def dependency_analyzer(state: AgentState):
    await asyncio.sleep(8)  # Stagger request
    messages = [
        SystemMessage(content=p["system"]),
        HumanMessage(content=p["user"].format(files_content=state["files_fetched"])),
    ]

    response = await llm_with_structure.ainvoke(messages)

    return {"analysis_results": {"dependency": response.issues}}

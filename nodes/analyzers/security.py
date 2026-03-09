import asyncio
import yaml
from typing import List

from pydantic import BaseModel, Field
from nodes.llm_client import llm
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import AgentState




with open("prompts/security.yaml", "r") as f:
    p = yaml.safe_load(f)


class SecurityIssue(BaseModel):
    location: str = Field(description="File and function/class name where the issue exists")
    problem: str = Field(description="Description of the security issue")
    suggestion: str = Field(description="Concrete fix suggestion")


class SecurityAnalysis(BaseModel):
    issues: List[SecurityIssue] = Field(description="List of security issues found")


llm_with_structure = llm.with_structured_output(SecurityAnalysis)


async def security_analyzer(state: AgentState):
    await asyncio.sleep(4)  # Stagger request
    messages = [
        SystemMessage(content=p["system"]),
        HumanMessage(content=p["user"].format(files_content=state["files_fetched"])),
    ]

    response = await llm_with_structure.ainvoke(messages)

    return {"analysis_results": {"security": response.issues}}

import os
import yaml
from typing import Dict, List

from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import AgentState


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))

with open("prompts/complexity.yaml", "r") as f:
    p = yaml.safe_load(f)


class ComplexityIssue(BaseModel):
    location: str = Field(description="File and function/class name where the issue exists")
    problem: str = Field(description="Description of the complexity issue")
    suggestion: str = Field(description="Concrete fix suggestion")


class ComplexityAnalysis(BaseModel):
    issues: List[ComplexityIssue] = Field(description="List of complexity issues found")


llm_with_structure = llm.with_structured_output(ComplexityAnalysis)


def complexity_analyzer(state: AgentState):
    messages = [
        SystemMessage(content=p["system"]),
        HumanMessage(content=p["user"].format(files_content=state["files_fetched"])),
    ]

    response = llm_with_structure.invoke(messages)

    return {"analysis_results": {"complexity": response.issues}}

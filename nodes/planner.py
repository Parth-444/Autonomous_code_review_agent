
import yaml
from typing import Dict

from pydantic import BaseModel, Field
from nodes.llm_client import llm
from langchain_core.messages import HumanMessage, SystemMessage

from graph.state import AgentState


class AnalyzerPlan(BaseModel):
    analyzers: Dict[str, str] = Field(description="Dictionary of selected analyzers and reason they were chosen")


with open("prompts/planner_decision.yaml", "r") as f:
    p = yaml.safe_load(f)


llm_with_structure = llm.with_structured_output(AnalyzerPlan)


def planner(state: AgentState):
    repo_tree = state["repo_tree"]
    file_content = state["files_fetched"]

    messages = [
        SystemMessage(content=p["system"]),
        HumanMessage(content=p["user"].format(repo_tree=repo_tree, files_content=file_content)),
    ]

    response = llm_with_structure.invoke(messages)

    return {"analyzers": response.analyzers}
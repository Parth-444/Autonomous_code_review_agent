from graph.state import AgentState
import yaml
from nodes.llm_client import llm
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from typing import List


class CriticIssue(BaseModel):
    file_and_function: str = Field(description="File and function name where issue was found")
    flagged_by: List[str] = Field(description="Which analyzers flagged this issue")
    combined_severity_reason: str = Field(description="Why combined severity is higher than individual findings")
    priority: str = Field(description="Critical / High / Medium / Low")
    fix_order: str = Field(description="Recommended fix order and approach")

class CriticOutput(BaseModel):
    issues: List[CriticIssue] = Field(description="List of cross-referenced prioritized issues")



with open("prompts/critic.yaml", "r") as f:
    p = yaml.safe_load(f)

llm_with_structure = llm.with_structured_output(CriticOutput)

def critic(state: AgentState):
    messages = [
        SystemMessage(content=p["system"]),
        HumanMessage(content=p["user"].format(issues=state["analysis_results"], code_context=state["files_fetched"]))
    ]
    response = llm_with_structure.invoke(messages)
    return {"critic_results": response.issues}
    

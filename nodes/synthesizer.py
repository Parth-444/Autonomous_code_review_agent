from langchain_core.messages import SystemMessage, HumanMessage
import yaml
from nodes.llm_client import llm
from graph.state import AgentState
from pydantic import BaseModel

class Synthesizer(BaseModel):
    report: str

with open("prompts/synthesizer.yaml", "r") as f:
    p = yaml.safe_load(f)

llm_with_structure = llm.with_structured_output(Synthesizer)

def synthesizer(state: AgentState):
    messages = [
        SystemMessage(content=p["system"]),
        HumanMessage(content=p["user"].format(analyzer_results = state["analysis_results"], critic_results=state["critic_results"]))
    ]
    response = llm_with_structure.invoke(messages)

    return {"report": response.report}
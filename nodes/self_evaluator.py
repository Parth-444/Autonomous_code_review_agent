import yaml
from nodes.llm_client import llm
from pydantic import BaseModel, Field
from graph.state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage


with open("prompts/self_evaluator.yaml", "r") as f:
    p = yaml.safe_load(f)


class DimensionScore(BaseModel):
    score: int = Field(description="Score from 0-10")
    justification: str = Field(description="One sentence justification for the score")
    improvement: str = Field(description="What would improve this score")

class EvaluationOutput(BaseModel):
    actionability: DimensionScore
    accuracy: DimensionScore
    coverage: DimensionScore

llm_with_structure = llm.with_structured_output(EvaluationOutput)

def self_evaluator(state: AgentState):
    messages = [
        SystemMessage(content=p["system"]),
        HumanMessage(content=p["user"].format(files_fetched=state["files_fetched"], report=state["report"]))
    ]
    response = llm_with_structure.invoke(messages)

    return {"self_evaluation": response.model_dump()}





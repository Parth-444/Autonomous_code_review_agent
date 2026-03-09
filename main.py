import asyncio
import os
import json
from langgraph.graph import StateGraph, END
from graph.state import AgentState
from nodes.fetcher import fetcher
from nodes.planner import planner
from nodes.analyzers.complexity import complexity_analyzer
from nodes.analyzers.security import security_analyzer
from nodes.analyzers.design import design_analyzer
from nodes.analyzers.dependency import dependency_analyzer
from nodes.critic import critic
from nodes.synthesizer import synthesizer
from nodes.self_evaluator import self_evaluator
from typing import List


def route_to_analyzers(state: AgentState) -> List[str]:
    """Returns the list of analyzer node names the planner selected."""
    return list(state["analyzers"].keys())


builder = StateGraph(AgentState)

# Add all nodes
builder.add_node("fetcher", fetcher)
builder.add_node("planner", planner)
builder.add_node("complexity", complexity_analyzer)
builder.add_node("security", security_analyzer)
builder.add_node("design", design_analyzer)
builder.add_node("dependency", dependency_analyzer)
builder.add_node("critic", critic)
builder.add_node("synthesizer", synthesizer)
builder.add_node("self_evaluator", self_evaluator)

# Entry point
builder.set_entry_point("fetcher")

# Linear edges
builder.add_edge("fetcher", "planner")

# Conditional fan-out from planner to selected analyzers
builder.add_conditional_edges(
    "planner",
    route_to_analyzers,
    {
        "complexity": "complexity",
        "security": "security",
        "design": "design",
        "dependency": "dependency",
    }
)

# All analyzers converge into critic
builder.add_edge("complexity", "critic")
builder.add_edge("security", "critic")
builder.add_edge("design", "critic")
builder.add_edge("dependency", "critic")

# Rest of the pipeline
builder.add_edge("critic", "synthesizer")
builder.add_edge("synthesizer", "self_evaluator")
builder.add_edge("self_evaluator", END)

graph = builder.compile()


async def main():
    result = await graph.ainvoke({
        "repo_name": "Real-Estate-Price-Prediction-and-Analytics-Platform",
        "repo_tree": "",
        "files_fetched": {},
        "analyzers": {},
        "analysis_results": {},
        "critic_results": [],
        "final_report": "",
        "self_eval_scores": {}
    })
    print(result["report"])
    print(result["self_evaluation"])

    os.makedirs("output", exist_ok=True)
    
    with open("output/report.txt", "w", encoding="utf-8") as f:
        f.write(result["report"])
        
    with open("output/self_evaluation.txt", "w", encoding="utf-8") as f:
        if isinstance(result["self_evaluation"], dict):
            f.write(json.dumps(result["self_evaluation"], indent=4))
        else:
            f.write(str(result["self_evaluation"]))
            
    print("Report and self-evaluation written to 'output' directory.")

if __name__ == "__main__":
    asyncio.run(main())
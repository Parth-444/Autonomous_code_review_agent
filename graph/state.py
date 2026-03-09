from typing import TypedDict, List, Dict, Annotated

def merge_dicts(a: dict, b: dict) -> dict:
    return {**a, **b}
    
class AgentState(TypedDict):
    repo_name: str
    repo_tree: List
    important_files: List
    files_fetched: Dict[str, str]
    analyzers: Dict[str, str]
    analysis_results: Annotated[Dict[str, List], merge_dicts]
    critic_results: List[Dict]
    report: str
    self_evaluation: Dict
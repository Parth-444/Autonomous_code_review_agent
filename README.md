# Autonomous_code_review_agent

## Overview
The Autonomous Code Review Agent is a specialized system designed to perform automated, multi-dimensional analysis on code repositories. Utilizing a LangGraph-based state machine, the agent performs an end-to-end review by fetching repository data, planning the necessary analysis steps, executing specialized code inspections, and synthesizing the findings into a comprehensive report.

The system exists to provide developers with proactive insights into code complexity, security vulnerabilities, design flaws, and dependency issues. It works conceptually by passing a shared `AgentState` through a series of specialized nodes (Fetchers, Analyzers, Critics, and Synthesizers) that refine raw code data into actionable developer feedback.

## Architecture / Folder Structure

```text
Autonomous_code_review_agent
├── .python-version
├── README.md
├── graph
│   ├── __init__.py
│   └── state.py
├── integrations
│   ├── __init__.py
│   └── mcp_config.py
├── main.py
├── nodes
│   ├── __init__.py
│   ├── analyzers
│   │   ├── __init__.py
│   │   ├── complexity.py
│   │   ├── dependency.py
│   │   ├── design.py
│   │   └── security.py
│   ├── critic.py
│   ├── fetcher.py
│   ├── llm_client.py
│   ├── planner.py
│   ├── self_evaluator.py
│   └── synthesizer.py
├── prompts
│   ├── complexity.yaml
│   ├── critic.yaml
│   ├── dependency.yaml
│   ├── design.yaml
│   ├── important_files.yaml
│   ├── planner_decision.yaml
│   ├── security.yaml
│   ├── self_evaluator.yaml
│   └── synthesizer.yaml
├── pyproject.toml
└── uv.lock
```

The system is built on a directed acyclic graph (DAG) architecture managed by **LangGraph**. The workflow follows a strict pipeline: 
1. **Fetcher**: Retrieves the repository structure and content via MCP.
2. **Planner**: Determines which analysis nodes are required based on the repository content.
3. **Analyzers**: Concurrent execution of specialized modules (Complexity, Security, Design, Dependency).
4. **Critic**: Cross-references findings to prioritize issues.
5. **Synthesizer**: Generates the final readable report.
6. **Self-Evaluator**: Provides a metric-based assessment of the generated output.

## Key Modules
- **`graph/state.py`**: Defines the `AgentState` TypedDict, which maintains the repository context, analysis results, and system state throughout the pipeline.
- **`nodes/fetcher.py`**: Interacts with MCP servers to traverse the repository and load critical files into the agent state.
- **`nodes/planner.py`**: Uses LLM-driven decision-making to select the appropriate analysis nodes, enabling dynamic routing of the review pipeline.
- **`nodes/analyzers/`**: Contains specialized logic to analyze specific facets of code quality using structured Pydantic outputs.
- **`nodes/critic.py`**: Consolidates results from different analyzers to remove noise and prioritize fixes.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Parth-444/Autonomous_code_review_agent
   ```
2. Ensure you have `uv` installed.
3. Install dependencies:
   ```bash
   uv sync
   ```
4. Set your `GEMINI_API_KEY` in a `.env` file.

## Usage
Execute the main entry point to initiate an automated review:
```bash
uv run python main.py
```
The system will generate a `report.txt` and `self_evaluation.txt` within an `output/` directory in the root folder.

## External Dependencies
- **LangGraph**: Used for orchestrating the multi-node autonomous agent pipeline.
- **MCP (Model Context Protocol)**: Utilized via `langchain-mcp-adapters` to interface with remote repository tools for fetching code.
- **Google Generative AI**: The system uses `gemini-3.1-flash-lite-preview` for intelligent analysis and structured output generation.

## Configuration
- **Prompts**: All system instructions are externalized in the `prompts/` directory as YAML files. Modifying these files will directly alter the behavior and focus of the respective nodes.
- **MCP**: Integration settings are managed in `integrations/mcp_config.py`.

## Contributing
Contributions are welcome. Please ensure that any new analyzer nodes follow the existing Pydantic structure and are registered in `main.py`.

## Reporting Issues
Please report issues via the GitHub repository's issue tracker. Ensure you include the logs and the repository name that triggered the failure.

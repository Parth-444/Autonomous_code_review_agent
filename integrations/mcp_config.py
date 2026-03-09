from langchain_mcp_adapters.client import MultiServerMCPClient

MCP_CONFIG = {
    "github-server": {
        "command": "uv",
        "args": ["run", "python", "main.py"],
        "transport": "stdio",
        "cwd": "C:\\Users\\Parth\\Desktop\\github_mcp_server"
    }
}

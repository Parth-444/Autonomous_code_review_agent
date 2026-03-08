from langchain_mcp_adapters.client import MultiServerMCPClient

def get_mcp_tools():
    client = MultiServerMCPClient(
        "github-server":{
            "command": "uv",
            "args": ["run", "python", "C:\\Users\\Parth\\Desktop\\github_mcp_server\\main.py"],
            "transport": "stdio"
        }
    )
    tools = client.get_tools()
    return tools

tools = get_mcp_tools()

# get_username_tool = next(t for t in tools if t.name == "get_username")
# repo_tree_tool = next(t for t in tools if t.name == "get_repo_tree")
# list_repos_tool = next(t for t in tools if t.name == "list_repos")
# get_file_content_tool = next(t for t in tools if t.name == "get_file_content")


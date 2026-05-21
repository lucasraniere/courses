from dotenv import load_dotenv

load_dotenv()

from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from typing import Any, Dict
from requests import get

mcp = FastMCP("mcp_server")

tavily_client = TavilyClient()

@mcp.tool()
def search_web(query: str) -> Dict[str, Any]:
    """Search the web for the given query and return the results."""
    results = tavily_client.search(query)
    return results

# Resources - provide access to langchain-ai repo files
@mcp.resource("github://langchain-ai/langchain-mcp-adapters/blob/main/README.md")
def github_file():
    """
    Resource for accessing langchain-ai/langchain-mcp-adapters README.md file from GitHub.
    """
    url = "https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/main/README.md"
    response = get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch the file from GitHub. Status code: {response.status_code}")


@mcp.prompt()
def prompt():
    """Analyze data from a langchain-ai repo file wiht comprehensive insights"""
    return """
    You are a helpful assistant that answers user questions about LangChain, LangGraph and LangSmith.

    You can use the following tools/resources to answer user questions:
    - search_web: Search the web for information
    - github_file: Access the langchain-ai repo files

    If the user asks a question that is not related to LangChain, LangGraph or LangSmith, you should say "I'm sorry, I can only answer questions related to LangChain, LangGraph and LangSmith."

    You may try multiple tool and resource calls to answer the user's question.

    You may also ask clarifying questions to the user to better understand their question.
    """


if __name__ == "__main__":
    mcp.run()

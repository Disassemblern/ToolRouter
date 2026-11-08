from mcp.server.mcpserver import MCPServer

server = MCPServer("class6-hello")


@server.tool()
def hello(name: str) -> str:
    """Say hello to a person."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    server.run(transport="stdio")

import asyncio
import os
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters
from mcp.server.mcpserver import MCPServer
from mcp.types import TextContent
from server import server

HERE = Path(__file__).resolve().parent


async def check_hello(label: str, target: MCPServer | StdioServerParameters) -> None:
    async with Client(target) as client:
        tools = (await client.list_tools()).tools
        assert [tool.name for tool in tools] == ["hello"]
        result = await client.call_tool("hello", {"name": "ToolRouter"})
        assert not result.is_error
        content = result.content[0]
        assert isinstance(content, TextContent)
        assert content.text == "Hello, ToolRouter!"
        print(f"{label}: hello -> {content.text}")


async def check_filesystem(npx_script: str) -> None:
    sandbox = str(HERE / "sandbox")
    npm_cache = os.environ.get("npm_config_cache", str(HERE / ".npm-cache"))
    target = StdioServerParameters(
        command="node",
        args=[
            str(Path(npx_script).resolve()),
            "--yes",
            "--prefer-offline",
            "--cache",
            npm_cache,
            "@modelcontextprotocol/server-filesystem@2.2.0",
            sandbox,
        ],
    )
    async with Client(target) as client:
        names = [tool.name for tool in (await client.list_tools()).tools]
        assert "list_directory" in names
        print(f"Filesystem ({len(names)} tools): {', '.join(names)}")
        result = await client.call_tool("list_directory", {"path": sandbox})
        assert not result.is_error
        content = result.content[0]
        assert isinstance(content, TextContent)
        assert content.text.strip() == "[FILE] example.txt"
        print(f"Filesystem list_directory: {content.text}")


async def main(npx_script: str | None = None) -> None:
    async with asyncio.timeout(120):
        await check_hello("In memory", server)
        target = StdioServerParameters(
            command=sys.executable,
            args=[str(HERE / "server.py")],
        )
        await check_hello("Stdio", target)
        if npx_script:
            await check_filesystem(npx_script)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise SystemExit("Usage: python check.py [path-to-npx-cli.js]")
    asyncio.run(main(*sys.argv[1:]))

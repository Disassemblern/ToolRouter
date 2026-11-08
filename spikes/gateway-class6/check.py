import argparse
import asyncio
import sys
from importlib.metadata import version
from pathlib import Path

from mcp import Client, StdioServerParameters
from mcp.server.mcpserver import MCPServer
from mcp.types import TextContent
from server import server

HERE = Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox"
FILESYSTEM_PACKAGE = "@modelcontextprotocol/server-filesystem@2.2.0"


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


async def check_filesystem(node: str, npx_script: Path, npm_cache: Path) -> None:
    target = StdioServerParameters(
        command=node,
        args=[
            str(npx_script.resolve()),
            "--yes",
            "--cache",
            str(npm_cache.resolve()),
            FILESYSTEM_PACKAGE,
            str(SANDBOX),
        ],
    )
    async with Client(target) as client:
        names = [tool.name for tool in (await client.list_tools()).tools]
        assert "list_directory" in names
        print(f"Filesystem ({len(names)} tools): {', '.join(names)}")
        result = await client.call_tool("list_directory", {"path": str(SANDBOX)})
        assert not result.is_error
        content = result.content[0]
        assert isinstance(content, TextContent)
        assert content.text.strip() == "[FILE] example.txt"
        print(f"Filesystem list_directory: {content.text}")


async def main(args: argparse.Namespace) -> None:
    print(f"Python {sys.version.split()[0]}, mcp {version('mcp')}")
    async with asyncio.timeout(120):
        if args.mode in ("hello", "all"):
            await check_hello("In memory", server)
            target = StdioServerParameters(
                command=sys.executable,
                args=[str(HERE / "server.py")],
            )
            await check_hello("Stdio", target)
        if args.mode in ("filesystem", "all"):
            await check_filesystem(args.node, args.npx_script, args.npm_cache)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("hello", "filesystem", "all"))
    parser.add_argument("--node", default="node")
    parser.add_argument("--npx-script", type=Path)
    parser.add_argument("--npm-cache", type=Path, default=HERE / ".npm-cache")
    args = parser.parse_args()
    if args.mode != "hello" and args.npx_script is None:
        parser.error("--npx-script is required for the filesystem check")
    asyncio.run(main(args))

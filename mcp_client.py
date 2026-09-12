# The client is responsible for launching the MCP server as a subprocess
# and talking to it over stdio using the MCP protocol.

import sys
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Optional

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from pydantic import AnyUrl


class MCPClient:
    def __init__(self):
        # Holds the live session once connect() has been called
        self._session: Optional[ClientSession] = None
        # Keeps the stdio transport and session open for the client's lifetime
        self._exit_stack = AsyncExitStack()

    def session(self) -> ClientSession:
        if self._session is None:
            raise ConnectionError(
                "Client session not initialized. Call connect() first."
            )
        return self._session

    # Launches mcp_server.py as a subprocess and opens an MCP session over its stdio
    async def connect(self, server_script_path: str = "mcp_server.py"):
        server_path = Path(__file__).parent / server_script_path
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(server_path)],
        )

        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        stdio, write = stdio_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(stdio, write)
        )
        await self._session.initialize()

    # Function gets all available tools from the MCP server

    # We access our session (the connection to the server),
    # call the built-in list_tools() method,
    # and return the tools from the result.

    async def list_tools(self) -> list[types.Tool]:
        result = await self.session().list_tools()
        return result.tools

    async def call_tool(self, tool_name: str, tool_input: dict) -> types.CallToolResult:
        return await self.session().call_tool(tool_name, tool_input)

    # Lists direct resources (static URIs) the server exposes.
    async def list_resources(self) -> list[types.Resource]:
        result = await self.session().list_resources()
        return result.resources

    # Lists templated resources (URIs with {params}) the server exposes.
    async def list_resource_templates(self) -> list[types.ResourceTemplate]:
        result = await self.session().list_resource_templates()
        return result.resourceTemplates

    # Reads one resource by URI, e.g. "docs://documents" or "docs://documents/plan.md".
    async def read_resource(self, uri: str) -> types.ReadResourceResult:
        return await self.session().read_resource(AnyUrl(uri))

    async def cleanup(self):
        await self._exit_stack.aclose()

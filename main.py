import asyncio

from mcp_client import MCPClient


async def main():
    client = MCPClient()
    await client.connect()

    try:
        tools = await client.list_tools()
        print(f"Connected. Server exposes {len(tools)} tool(s):\n")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())

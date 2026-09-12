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

        # Direct resource: static URI, no params
        resources = await client.list_resources()
        print(f"\n{len(resources)} direct resource(s):")
        for resource in resources:
            print(f"- {resource.uri}")

        # Templated resource: URI has a {doc_id} placeholder
        templates = await client.list_resource_templates()
        print(f"\n{len(templates)} templated resource(s):")
        for template in templates:
            print(f"- {template.uriTemplate}")

        # Read the direct resource (docs://documents -> list of doc ids, parsed from JSON)
        doc_list = await client.read_resource("docs://documents")
        print(f"\ndocs://documents ->\n{doc_list}")

        # Read a templated resource, filling in {doc_id}
        doc_text = await client.read_resource("docs://documents/plan.md")
        print(f"\ndocs://documents/plan.md ->\n{doc_text}")

        # Prompts: reusable message templates the server exposes
        prompts = await client.list_prompts()
        print(f"\n{len(prompts)} prompt(s):")
        for prompt in prompts:
            print(f"- {prompt.name}: {prompt.description}")

        messages = await client.get_prompt("format", {"doc_id": "plan.md"})
        print(f"\nformat prompt rendered {len(messages)} message(s):")
        for message in messages:
            print(f"[{message.role}] {message.content.text}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())

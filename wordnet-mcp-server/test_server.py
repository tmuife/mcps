import asyncio
from fastmcp import FastMCP, Client, Context
from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.auth.providers.bearer import RSAKeyPair
import inspect

# 1. Generate a new key pair for signing and verifying tokens
key_pair = RSAKeyPair.generate()

# 2. Configure the server-side authentication provider
# IMPORTANT: Make sure issuer and audience match between server and token
auth_provider = BearerAuthProvider(
    public_key=inspect.cleandoc(key_pair.public_key),
    issuer="https://dev.example.com",  # Must match token issuer
    audience="my-mcp-server",  # Must match token audience
)

# 3. Create the FastMCP server instance with the auth provider
mcp_server = FastMCP(
    name="AuthProtectedServer",
    auth=auth_provider,
)


@mcp_server.tool()
async def get_secret_message(ctx: Context) -> str:
    """A protected tool that requires authentication."""
    return "This is a secret message for authenticated users."


async def main():
    """
    Starts the server, creates an authenticated client, and makes a call.
    """
    host = "127.0.0.1"
    port = 4588
    server_url = f"http://{host}:{port}/mcp/"

    # Start the server
    server_task = asyncio.create_task(
        mcp_server.run_async(transport="streamable-http", host=host, port=port, path="/mcp/")
    )

    # Wait a moment for the server to start up
    await asyncio.sleep(2)
    print(f"✅ MCP Server started at {server_url}")

    # 4. Generate a token for the client
    # This token is signed with the private key and MUST match server config
    client_token = key_pair.create_token(
        subject="test-client",
        issuer="https://dev.example.com",  # Must match server's expected issuer
        audience="my-mcp-server",  # Must match server's expected audience
        scopes=["read", "write"],
    )
    print(f"\n🔑 Generated client token: {client_token[:50]}...")

    # 5. Create a client and authenticate using the token
    try:
        print("\n🚀 Client connecting and authenticating...")
        async with Client(server_url, auth=client_token) as client:
            print("✅ Client connected successfully!")

            print("\n📋 Listing available tools...")
            tools = await client.list_tools()
            print(f"Available tools: {[tool.name for tool in tools]}")

            # Call the protected tool
            print("\n🔧 Calling protected tool...")
            response = await client.call_tool("get_secret_message")
            print(f"✅ Successfully called protected tool.")
            print(f"🤫 Server response: '{response}'")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up and stop the server
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            print("\n🛑 MCP Server stopped.")


if __name__ == "__main__":
    asyncio.run(main())
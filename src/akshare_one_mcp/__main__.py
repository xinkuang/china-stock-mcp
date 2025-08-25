import logging
import os
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from akshare_one_mcp.server import mcp


logger = logging.getLogger(__name__)


def main():
    # HTTP mode for Smithery deployment
    print("MCP Server starting in HTTP mode...")

    # Setup Starlette app with CORS for cross-origin requests
    app = mcp.http_app()

    # IMPORTANT: add CORS middleware for browser based clients
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["mcp-session-id", "mcp-protocol-version"],
        max_age=86400,
    )

    # Use Smithery-required PORT environment variable
    port = int(os.environ.get("PORT", 8081))
    print(f"Listening on port {port}")

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="debug")


if __name__ == "__main__":
    main()

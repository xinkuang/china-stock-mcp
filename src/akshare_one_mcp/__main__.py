import logging

from akshare_one_mcp.server import mcp


logger = logging.getLogger(__name__)

def main():
    logger.info("Starting AKShare One MCP Server...")
    mcp.run(transport="stdio")
    logger.info("AKShare One MCP Server stopped.")

if __name__ == "__main__":
    main()

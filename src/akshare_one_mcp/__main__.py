import logging

from akshare_one_mcp.server import mcp


logger = logging.getLogger(__name__)


def main():
    # mcp.run(transport="streamable-http", port=8081)
    mcp.run()


if __name__ == "__main__":
    main()

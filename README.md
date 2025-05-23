# AKShare One MCP Server

<div align="center">
  <a href="README.md">English</a> | 
  <a href="README_zh.md">中文</a>
</div>

[![smithery badge](https://smithery.ai/badge/@zwldarren/akshare-one-mcp)](https://smithery.ai/server/@zwldarren/akshare-one-mcp)

An MCP server based on [akshare-one](https://github.com/zwldarren/akshare-one), providing interfaces for China stock market data. It offers a set of tools for retrieving financial information including historical stock data, real-time data, news data, financial statements, etc.

<a href="https://glama.ai/mcp/servers/@zwldarren/akshare-one-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@zwldarren/akshare-one-mcp/badge" alt="akshare-one-mcp MCP server" />
</a>

## Tools

### `get_hist_data`

Get historical stock data
Input parameters:

- symbol (string): Stock code
- interval (string): Time interval ('minute','hour','day','week','month','year')
- interval_multiplier (number, optional): Interval multiplier (default: 1)
- start_date (string, optional): Start date in YYYY-MM-DD format (default: '1970-01-01')
- end_date (string, optional): End date in YYYY-MM-DD format (default: '2030-12-31')
- adjust (string, optional): Adjustment type ('none', 'qfq', 'hfq') (default: 'none')
- source (string, optional): Data source ('eastmoney', 'sina') (default: 'eastmoney')

### `get_realtime_data`

Get real-time stock data
Input parameters:

- symbol (string, optional): Stock code
- source (string, optional): Data source (default: 'xueqiu')

### `get_news_data`

Get stock-related news data
Input parameters:

- symbol (string): Stock code
- recent_n (number, optional): Number of most recent records to return (optional)

### `get_balance_sheet`

Get company balance sheet data
Input parameters:

- symbol (string): Stock code
- recent_n (number, optional): Number of most recent records to return (optional)

### `get_income_statement`

Get company income statement data
Input parameters:

- symbol (string): Stock code
- recent_n (number, optional): Number of most recent records to return (optional)

### `get_cash_flow`

Get company cash flow statement data
Input parameters:

- symbol (string): Stock code
- source (string, optional): Data source (default: 'sina')

### `get_inner_trade_data`

Get company insider trading data
Input parameters:

- symbol (string, optional): Stock code

## Usage Instructions

### Installing via Smithery

To install akshare-one-mcp for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@zwldarren/akshare-one-mcp):

```bash
npx -y @smithery/cli install @zwldarren/akshare-one-mcp --client claude
```

### Installing via `uv`

Install directly from PyPI using uv:

```bash
uv pip install akshare-one-mcp
```

Add the following configuration:

```json
"mcpServers": {
    "akshare-one-mcp": {
        "command": "uvx",
        "args": ["akshare-one-mcp"]
    }
}
```

### Installing via local source code

1. Clone this repository:

    ```bash
    git clone https://github.com/zwldarren/akshare-one-mcp.git
    cd akshare-one-mcp
    ```

2. Install [uv](<https://docs.astral.sh/uv/getting-started/installation/>) if you haven't already.

3. Install dependencies:

    ```bash
    uv sync
    ```

4. Add the following configuration:

    ```json
    "mcpServers": {
        "akshare-one-mcp": {
            "command": "uv",
            "args": [
                "--directory",
                "/path/to/akshare-one-mcp",
                "run",
                "akshare-one-mcp"
            ]
        }
    }
    ```

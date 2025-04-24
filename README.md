# AKShare One MCP Server

An MCP server based on [akshare-one](https://github.com/zwldarren/akshare-one), providing interfaces for China stock market data. It offers a set of tools for retrieving financial information including historical stock data, real-time data, news data, financial statements, etc.

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
- source (string, optional): Data source (default: 'eastmoney')

### `get_news_data`

Get stock-related news data
Input parameters:

- symbol (string): Stock code
- source (string, optional): Data source (default: 'eastmoney')

### `get_balance_sheet`

Get company balance sheet data
Input parameters:

- symbol (string): Stock code
- source (string, optional): Data source (default: 'sina')

### `get_income_statement`

Get company income statement data
Input parameters:

- symbol (string): Stock code
- source (string, optional): Data source (default: 'sina')

### `get_cash_flow`

Get company cash flow statement data
Input parameters:

- symbol (string): Stock code
- source (string, optional): Data source (default: 'sina')

### `get_inner_trade_data`

Get company insider trading data
Input parameters:

- symbol (string, optional): Stock code
- source (string, optional): Data source (default: 'xueqiu')

## Usage Instructions

### Running the server

1. Clone this repository:

    ```bash
    git clone https://github.com/zwldarren/akshare-one-mcp.git
    cd akshare-one-mcp
    ```

2. Install uv (<https://docs.astral.sh/uv/getting-started/installation/>)

3. Install dependencies:

    ```bash
    uv sync
    ```

4. Run the server:

    ```bash
    uv run main.py
    ```

### Connect to Claude Desktop

Add the following configuration to the MCP server configuration file:

```json
"mcpServers": {
    "akshare-one-mcp": {
        "command": "uv",
        "args": [
            "--directory",
            "/path/to/akshare-one-mcp",
            "run",
            "server.py"
        ]
    }
}
```

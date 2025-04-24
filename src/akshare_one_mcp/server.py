import akshare_one as ak
from mcp.server.fastmcp import FastMCP
from typing import Optional


mcp = FastMCP("akshare-one-mcp", dependencies=["akshare-one"])


@mcp.tool()
def get_hist_data(
    symbol: str,
    interval: str,
    interval_multiplier: int = 1,
    start_date: str = "1970-01-01",
    end_date: str = "2030-12-31",
    adjust: str = "none",
    source: str = "eastmoney",
) -> str:
    """Get historical stock market data

    Args:
        symbol: Stock symbol/ticker
        interval: Time interval ('minute','hour','day','week','month','year')
        interval_multiplier: Interval multiplier (default: 1)
        start_date: Start date in YYYY-MM-DD format (default: '1970-01-01')
        end_date: End date in YYYY-MM-DD format (default: '2030-12-31')
        adjust: Adjustment type ('none', 'qfq', 'hfq') (default: 'none')
        source: Data source ('eastmoney', 'sina') (default: 'eastmoney')
    """
    df = ak.get_hist_data(
        symbol=symbol,
        interval=interval,
        interval_multiplier=interval_multiplier,
        start_date=start_date,
        end_date=end_date,
        adjust=adjust,
        source=source,
    )
    return df.to_json(orient="records")


@mcp.tool()
def get_realtime_data(symbol: Optional[str] = None, source: str = "eastmoney") -> str:
    """Get real-time stock market data

    Args:
        symbol: Stock symbol/ticker (optional)
        source: Data source (default: 'eastmoney')
    """
    df = ak.get_realtime_data(symbol=symbol, source=source)
    return df.to_json(orient="records")


@mcp.tool()
def get_news_data(symbol: str, source: str = "eastmoney") -> str:
    """Get stock-related news data

    Args:
        symbol: Stock symbol/ticker
        source: Data source (default: 'eastmoney')
    """
    df = ak.get_news_data(symbol=symbol, source=source)
    return df.to_json(orient="records")


@mcp.tool()
def get_balance_sheet(symbol: str, source: str = "sina") -> str:
    """Get company balance sheet data

    Args:
        symbol: Stock symbol/ticker
        source: Data source (default: 'sina')
    """
    df = ak.get_balance_sheet(symbol=symbol, source=source)
    return df.to_json(orient="records")


@mcp.tool()
def get_income_statement(symbol: str, source: str = "sina") -> str:
    """Get company income statement data

    Args:
        symbol: Stock symbol/ticker
        source: Data source (default: 'sina')
    """
    df = ak.get_income_statement(symbol=symbol, source=source)
    return df.to_json(orient="records")


@mcp.tool()
def get_cash_flow(symbol: str, source: str = "sina") -> str:
    """Get company cash flow statement data

    Args:
        symbol: Stock symbol/ticker
        source: Data source (default: 'sina')
    """
    df = ak.get_cash_flow(symbol=symbol, source=source)
    return df.to_json(orient="records")


@mcp.tool()
def get_inner_trade_data(symbol: Optional[str] = None, source: str = "xueqiu") -> str:
    """Get company insider trading data

    Args:
        symbol: Stock symbol/ticker (optional)
        source: Data source (default: 'xueqiu')
    """
    df = ak.get_inner_trade_data(symbol=symbol, source=source)
    return df.to_json(orient="records")

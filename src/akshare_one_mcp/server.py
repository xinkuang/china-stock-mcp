from datetime import datetime
import akshare as ak
import akshare_one as ako
from fastmcp import FastMCP
from typing import Optional


mcp = FastMCP(name="akshare-one-mcp")


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
        symbol: Stock symbol/ticker (e.g. '000001')
        interval: Time interval ('minute','hour','day','week','month','year')
        interval_multiplier: Interval multiplier (default: 1)
        start_date: Start date in YYYY-MM-DD format (default: '1970-01-01')
        end_date: End date in YYYY-MM-DD format (default: '2030-12-31')
        adjust: Adjustment type ('none', 'qfq', 'hfq') (default: 'none')
        source: Data source ('eastmoney', 'sina') (default: 'eastmoney')
    """
    df = ako.get_hist_data(
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
def get_realtime_data(symbol: Optional[str] = None, source: str = "xueqiu") -> str:
    """Get real-time stock market data

    Args:
        symbol: Stock symbol/ticker (optional, e.g. '000001')
        source: Data source ('xueqiu', 'eastmoney') (default: 'xueqiu')
    """
    df = ako.get_realtime_data(symbol=symbol, source=source)
    return df.to_json(orient="records")


@mcp.tool()
def get_news_data(symbol: str, recent_n: Optional[int] = 10) -> str:
    """Get stock-related news data

    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
        recent_n: Number of most recent records to return (optional)
    """
    df = ako.get_news_data(symbol=symbol, source="eastmoney")
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool()
def get_balance_sheet(symbol: str, recent_n: Optional[int] = 10) -> str:
    """Get company balance sheet data

    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
        recent_n: Number of most recent records to return (optional)
    """
    df = ako.get_balance_sheet(symbol=symbol, source="sina")
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool()
def get_income_statement(symbol: str, recent_n: Optional[int] = 10) -> str:
    """Get company income statement data

    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
        recent_n: Number of most recent records to return (optional)
    """
    df = ako.get_income_statement(symbol=symbol, source="sina")
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool()
def get_cash_flow(
    symbol: str, source: str = "sina", recent_n: Optional[int] = 10
) -> str:
    """Get company cash flow statement data

    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
        source: Data source (default: 'sina')
        recent_n: Number of most recent records to return (optional)
    """
    df = ako.get_cash_flow(symbol=symbol, source=source)
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool()
def get_inner_trade_data(symbol: str) -> str:
    """Get company insider trading data

    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
    """
    df = ako.get_inner_trade_data(symbol, source="xueqiu")
    return df.to_json(orient="records")


@mcp.tool()
def get_time_info() -> dict:
    """Get current time with ISO format, timestamp, and the last trading day

    Returns:
        A dictionary containing:
        - iso_format: ISO formatted local time string
        - timestamp: Unix timestamp
        - last_trading_day: The most recent trading day in YYYY-MM-DD format
    """
    local_time = datetime.now().astimezone()
    current_date = local_time.date()

    # Get trading calendar
    trade_date_df = ak.tool_trade_date_hist_sina()
    trade_dates = [d for d in trade_date_df["trade_date"]]

    # Filter dates <= current date and sort descending
    past_dates = sorted([d for d in trade_dates if d <= current_date], reverse=True)

    # Find the most recent trading day
    last_trading_day = past_dates[0].strftime("%Y-%m-%d") if past_dates else None

    return {
        "iso_format": local_time.isoformat(),
        "timestamp": local_time.timestamp(),
        "last_trading_day": last_trading_day,
    }

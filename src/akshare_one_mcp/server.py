from datetime import datetime
from typing import Annotated, Literal

import akshare as ak
import akshare_one as ako
from fastmcp import FastMCP
from pydantic import Field


mcp = FastMCP(name="akshare-one-mcp")


@mcp.tool()
def get_hist_data(
    symbol: Annotated[str, Field(description="Stock symbol/ticker (e.g. '000001')")],
    interval: Annotated[
        Literal["minute", "hour", "day", "week", "month", "year"],
        Field(description="Time interval"),
    ],
    interval_multiplier: Annotated[
        int, Field(description="Interval multiplier", ge=1)
    ] = 1,
    start_date: Annotated[
        str, Field(description="Start date in YYYY-MM-DD format")
    ] = "1970-01-01",
    end_date: Annotated[
        str, Field(description="End date in YYYY-MM-DD format")
    ] = "2030-12-31",
    adjust: Annotated[
        Literal["none", "qfq", "hfq"], Field(description="Adjustment type")
    ] = "none",
    source: Annotated[
        Literal["eastmoney", "eastmoney_direct", "sina"],
        Field(description="Data source"),
    ] = "eastmoney",
) -> str:
    """Get historical stock market data. Use 'eastmoney_direct' to get HK stock data (e.g. '00700')."""
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
def get_realtime_data(
    symbol: Annotated[
        str | None, Field(description="Stock symbol/ticker (e.g. '000001')")
    ] = None,
    source: Annotated[
        Literal["xueqiu", "eastmoney", "eastmoney_direct"],
        Field(description="Data source"),
    ] = "xueqiu",
) -> str:
    """Get real-time stock market data. Use 'eastmoney_direct' to get HK stock data (e.g. '00700')."""
    df = ako.get_realtime_data(symbol=symbol, source=source)
    return df.to_json(orient="records")


@mcp.tool()
def get_news_data(
    symbol: Annotated[str, Field(description="Stock symbol/ticker (e.g. '000001')")],
    recent_n: Annotated[
        int | None, Field(description="Number of most recent records to return", ge=1)
    ] = 10,
) -> str:
    """Get stock-related news data."""
    df = ako.get_news_data(symbol=symbol, source="eastmoney")
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool()
def get_balance_sheet(
    symbol: Annotated[str, Field(description="Stock symbol/ticker (e.g. '000001')")],
    recent_n: Annotated[
        int | None, Field(description="Number of most recent records to return", ge=1)
    ] = 10,
) -> str:
    """Get company balance sheet data."""
    df = ako.get_balance_sheet(symbol=symbol, source="sina")
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool()
def get_income_statement(
    symbol: Annotated[str, Field(description="Stock symbol/ticker (e.g. '000001')")],
    recent_n: Annotated[
        int | None, Field(description="Number of most recent records to return", ge=1)
    ] = 10,
) -> str:
    """Get company income statement data."""
    df = ako.get_income_statement(symbol=symbol, source="sina")
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool()
def get_cash_flow(
    symbol: Annotated[str, Field(description="Stock symbol/ticker (e.g. '000001')")],
    source: Annotated[str, Field(description="Data source")] = "sina",
    recent_n: Annotated[
        int | None, Field(description="Number of most recent records to return", ge=1)
    ] = 10,
) -> str:
    """Get company cash flow statement data."""
    df = ako.get_cash_flow(symbol=symbol, source=source)
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool()
def get_inner_trade_data(
    symbol: Annotated[str, Field(description="Stock symbol/ticker (e.g. '000001')")],
) -> str:
    """Get company insider trading data."""
    df = ako.get_inner_trade_data(symbol, source="xueqiu")
    return df.to_json(orient="records")


@mcp.tool()
def get_time_info() -> dict:
    """Get current time with ISO format, timestamp, and the last trading day."""
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

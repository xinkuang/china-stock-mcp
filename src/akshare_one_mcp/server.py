from datetime import datetime
from typing import Annotated, Literal

import akshare as ak
import akshare_one as ako
from akshare_one import indicators
from fastmcp import FastMCP
from pydantic import Field


mcp = FastMCP(name="china-stock-mcp") # 初始化 FastMCP 服务器实例

@mcp.tool(name="获取历史行情数据", description="获取股票的历史行情数据，支持多种数据源和技术指标")
def get_hist_data(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    interval: Annotated[
        Literal["minute", "hour", "day", "week", "month", "year"],
        Field(description="时间周期: minute, hour, day, week, month, year。默认:day"),
    ] = "day",
    interval_multiplier: Annotated[
        int, Field(description="时间周期乘数", ge=1)
    ] = 1,
    start_date: Annotated[
        str, Field(description="开始日期，格式为 YYYY-MM-DD")
    ] = "1970-01-01",
    end_date: Annotated[
        str, Field(description="结束日期，格式为 YYYY-MM-DD")
    ] = "2030-12-31",
    adjust: Annotated[
        Literal["none", "qfq", "hfq"], Field(description="复权类型: none, qfq(前复权), hfq(后复权)。默认：none")
    ] = "none",
    source: Annotated[
        Literal["eastmoney", "eastmoney_direct", "sina"],
        Field(description="数据来源: xueqiu, eastmoney, eastmoney_direct。默认：eastmoney"),
    ] = "eastmoney",
    indicators_list: Annotated[
        list[
            Literal[
                "SMA",
                "EMA",
                "RSI",
                "MACD",
                "BOLL",
                "STOCH",
                "ATR",
                "CCI",
                "ADX",
                "WILLR",
                "AD",
                "ADOSC",
                "OBV",
                "MOM",
                "SAR",
                "TSF",
                "APO",
                "AROON",
                "AROONOSC",
                "BOP",
                "CMO",
                "DX",
                "MFI",
                "MINUS_DI",
                "MINUS_DM",
                "PLUS_DI",
                "PLUS_DM",
                "PPO",
                "ROC",
                "ROCP",
                "ROCR",
                "ROCR100",
                "TRIX",
                "ULTOSC",
            ]
        ]
        | None,
        Field(description="要添加的技术指标: SMA, EMA, RSI, MACD, BOLL, STOCH, ATR, CCI, ADX, WILLR, AD, ADOSC, OBV, MOM, SAR, TSF, APO, AROON, AROONOSC, BOP, CMO, DX, MFI, MINUS_DI, MINUS_DM, PLUS_DI, PLUS_DM, PPO, ROC, ROCP, ROCR, ROCR100, TRIX, ULTOSC"),
    ] = None,
    recent_n: Annotated[
        int | None, Field(description="返回最近N条记录的数量", ge=1)
    ] = 100,
) -> str:
    """获取股票历史行情数据. 'eastmoney_direct' 支持所有 A, B, H 股"""
    df = ako.get_hist_data(
        symbol=symbol,
        interval=interval,
        interval_multiplier=interval_multiplier,
        start_date=start_date,
        end_date=end_date,
        adjust=adjust,
        source=source,
    )
    if indicators_list:
        indicator_map = {
            "SMA": (indicators.get_sma, {"window": 20}),
            "EMA": (indicators.get_ema, {"window": 20}),
            "RSI": (indicators.get_rsi, {"window": 14}),
            "MACD": (indicators.get_macd, {"fast": 12, "slow": 26, "signal": 9}),
            "BOLL": (indicators.get_bollinger_bands, {"window": 20, "std": 2}),
            "STOCH": (
                indicators.get_stoch,
                {"window": 14, "smooth_d": 3, "smooth_k": 3},
            ),
            "ATR": (indicators.get_atr, {"window": 14}),
            "CCI": (indicators.get_cci, {"window": 14}),
            "ADX": (indicators.get_adx, {"window": 14}),
            "WILLR": (indicators.get_willr, {"window": 14}),
            "AD": (indicators.get_ad, {}),
            "ADOSC": (indicators.get_adosc, {"fast_period": 3, "slow_period": 10}),
            "OBV": (indicators.get_obv, {}),
            "MOM": (indicators.get_mom, {"window": 10}),
            "SAR": (indicators.get_sar, {"acceleration": 0.02, "maximum": 0.2}),
            "TSF": (indicators.get_tsf, {"window": 14}),
            "APO": (
                indicators.get_apo,
                {"fast_period": 12, "slow_period": 26, "ma_type": 0},
            ),
            "AROON": (indicators.get_aroon, {"window": 14}),
            "AROONOSC": (indicators.get_aroonosc, {"window": 14}),
            "BOP": (indicators.get_bop, {}),
            "CMO": (indicators.get_cmo, {"window": 14}),
            "DX": (indicators.get_dx, {"window": 14}),
            "MFI": (indicators.get_mfi, {"window": 14}),
            "MINUS_DI": (indicators.get_minus_di, {"window": 14}),
            "MINUS_DM": (indicators.get_minus_dm, {"window": 14}),
            "PLUS_DI": (indicators.get_plus_di, {"window": 14}),
            "PLUS_DM": (indicators.get_plus_dm, {"window": 14}),
            "PPO": (
                indicators.get_ppo,
                {"fast_period": 12, "slow_period": 26, "ma_type": 0},
            ),
            "ROC": (indicators.get_roc, {"window": 10}),
            "ROCP": (indicators.get_rocp, {"window": 10}),
            "ROCR": (indicators.get_rocr, {"window": 10}),
            "ROCR100": (indicators.get_rocr100, {"window": 10}),
            "TRIX": (indicators.get_trix, {"window": 30}),
            "ULTOSC": (
                indicators.get_ultosc,
                {"window1": 7, "window2": 14, "window3": 28},
            ),
        }
        temp = []
        for indicator in indicators_list:
            if indicator in indicator_map:
                func, params = indicator_map[indicator]
                indicator_df = func(df, **params)
                temp.append(indicator_df)
        if temp:
            df = df.join(temp)
    if recent_n is not None:
        df = df.tail(recent_n)
    return df.to_json(orient="records")


@mcp.tool(name="获取实时行情数据", description="获取股票的实时行情数据，支持多种数据源")
def get_realtime_data(
    symbol: Annotated[
        str | None, Field(description="股票代码 (例如: '000001')")
    ] = None,
    source: Annotated[
        Literal["xueqiu", "eastmoney", "eastmoney_direct"],
        Field(description="数据来源: xueqiu, eastmoney, eastmoney_direct。默认为：eastmoney_direct"),
    ] = "eastmoney_direct",
) -> str:
    """获取实时股票行情数据. 'eastmoney_direct' 支持所有 A, B, H 股"""
    df = ako.get_realtime_data(symbol=symbol, source=source)
    return df.to_json(orient="records")


@mcp.tool(name="获取新闻数据", description="获取股票相关的新闻数据")
def get_news_data(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    recent_n: Annotated[
        int | None, Field(description="返回最近N条记录的数量", ge=1)
    ] = 10,
) -> str:
    """获取股票相关新闻数据."""
    df = ako.get_news_data(symbol=symbol, source="eastmoney")
    if recent_n is not None:
        df = df.tail(recent_n)
    return df.to_json(orient="records")


@mcp.tool(name="获取资产负债表", description="获取公司的资产负债表数据")
def get_balance_sheet(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    recent_n: Annotated[
        int | None, Field(description="返回最近N条记录的数量", ge=1)
    ] = 10,
) -> str:
    """获取公司资产负债表数据."""
    df = ako.get_balance_sheet(symbol=symbol, source="sina")
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool(name="获取利润表", description="获取公司的利润表数据")
def get_income_statement(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    recent_n: Annotated[
        int | None, Field(description="返回最近N条记录的数量", ge=1)
    ] = 10,
) -> str:
    """获取公司利润表数据."""
    df = ako.get_income_statement(symbol=symbol, source="sina")
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool(name="获取现金流量表", description="获取公司的现金流量表数据")
def get_cash_flow(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    source: Annotated[Literal["sina"], Field(description="数据来源")] = "sina",
    recent_n: Annotated[
        int | None, Field(description="返回最近N条记录的数量", ge=1)
    ] = 10,
) -> str:
    """获取公司现金流量表数据."""
    df = ako.get_cash_flow(symbol=symbol, source=source)
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool(name="获取内部交易数据", description="获取公司的内部交易数据")
def get_inner_trade_data(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
) -> str:
    """获取公司内部交易数据."""
    df = ako.get_inner_trade_data(symbol, source="xueqiu")
    return df.to_json(orient="records")


@mcp.tool(name="获取财务指标", description="获取三大财务报表的关键财务指标")
def get_financial_metrics(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    recent_n: Annotated[
        int | None, Field(description="返回最近N条记录的数量", ge=1)
    ] = 10,
) -> str:
    """
    获取三大财务报表的关键财务指标.
    """
    df = ako.get_financial_metrics(symbol)
    if recent_n is not None:
        df = df.head(recent_n)
    return df.to_json(orient="records")


@mcp.tool(name="获取时间信息", description="获取当前时间（ISO格式、时间戳）和最近一个交易日")
def get_time_info() -> dict:
    """获取当前时间（ISO格式、时间戳）和最近一个交易日."""
    local_time = datetime.now().astimezone()
    current_date = local_time.date()

    # 获取交易日历数据
    trade_date_df = ak.tool_trade_date_hist_sina()
    trade_dates = [d for d in trade_date_df["trade_date"]] # 提取所有交易日期

    # 筛选出小于等于当前日期的交易日，并按降序排列
    past_dates = sorted([d for d in trade_dates if d <= current_date], reverse=True)

    # 找到最近的一个交易日
    last_trading_day = past_dates[0].strftime("%Y-%m-%d") if past_dates else None

    return {
        "iso_format": local_time.isoformat(),
        "timestamp": local_time.timestamp(),
        "last_trading_day": last_trading_day,
    }
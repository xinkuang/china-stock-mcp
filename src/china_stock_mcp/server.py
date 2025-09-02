from datetime import datetime
from typing import Annotated, Literal

import akshare as ak
import akshare_one as ako
from akshare_one import indicators
from fastmcp import FastMCP
from pydantic import Field


mcp = FastMCP(name="china-stock-mcp") # 初始化 FastMCP 服务器实例

@mcp.tool(name="get_hist_data", description="获取股票的历史行情数据，支持多种数据源和技术指标")
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


@mcp.tool(name="get_realtime_data", description="获取股票的实时行情数据，支持多种数据源")
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


@mcp.tool(name="get_news_data", description="获取股票相关的新闻数据")
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


@mcp.tool(name="get_balance_sheet", description="获取公司的资产负债表数据")
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


@mcp.tool(name="get_income_statement", description="获取公司的利润表数据")
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


@mcp.tool(name="get_cash_flow", description="获取公司的现金流量表数据")
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


@mcp.tool(name="get_inner_trade_data", description="获取公司的内部交易数据")
def get_inner_trade_data(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
) -> str:
    """获取公司内部交易数据."""
    df = ako.get_inner_trade_data(symbol, source="xueqiu")
    return df.to_json(orient="records")


@mcp.tool(name="get_financial_metrics", description="获取三大财务报表的关键财务指标")
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


@mcp.tool(name="get_time_info", description="获取当前时间（ISO格式、时间戳）和最近一个交易日")
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
@mcp.tool(name="get_stock_basic_info", description="获取指定股票的基本概要信息")
def get_stock_basic_info(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001' 代表A股, '00700' 代表港股)")],
    market_type: Annotated[
        Literal["A股", "港股"], Field(description="市场类型: A股, 港股。默认: A股")
    ] = "A股",
    data_source: Annotated[
        Literal["eastmoney", "xueqiu", "cninfo", "xq"],
        Field(description="数据来源: eastmoney(东方财富), xueqiu(雪球), cninfo(巨潮资讯), xq(雪球)。默认: cninfo"),
    ] = "cninfo",
    recent_n: Annotated[
        int | None, Field(description="返回最近N条记录的数量，仅适用于部分接口", ge=1)
    ] = None,
) -> str:
    """获取股票基本概要信息，支持 A 股和港股"""
    try:
        if market_type == "A股":
            if data_source == "eastmoney":
                df = ak.stock_individual_info_em(symbol)
            elif data_source == "xueqiu":
                df = ak.stock_individual_basic_info_xq(symbol="SH" + symbol)
            elif data_source == "cninfo":
                df = ak.stock_profile_cninfo(symbol)
            elif data_source == "xq":
                df = ak.stock_individual_basic_info_hk_xq(symbol)
            else:
                raise ValueError(f"Unsupported data_source for A股: {data_source}")
        elif market_type == "港股":
            if data_source == "eastmoney":
                df = ak.stock_hk_company_profile_em(symbol)
            elif data_source == "xq":
                df = ak.stock_individual_basic_info_hk_xq(symbol)
            else:
                raise ValueError(f"Unsupported data_source for 港股: {data_source}")
        else:
            raise ValueError(f"Unsupported market_type: {market_type}")

        if recent_n is not None:
            df = df.tail(recent_n)

        return df.to_json(orient="records")

    except Exception as e:
        return f"Error fetching stock basic info: {str(e)}"


@mcp.tool(name="get_macro_data", description="获取宏观经济数据")
def get_macro_data(
    indicator: Annotated[
        Literal["money_supply", "gdp", "cpi", "pmi", "stock_summary"],
        Field(
            description="宏观经济指标，可选值包括: money_supply(货币供应量), gdp(GDP数据), cpi(CPI数据), pmi(PMI数据), stock_summary(股市概览)等",
            examples=["money_supply", "gdp", "cpi", "pmi", "stock_summary"]
        )
    ],
    data_source: Annotated[
        Literal["sina", "eastmoney"],
        Field(description="数据来源: sina, eastmoney。默认: sina"),
    ] = "sina",
    recent_n: Annotated[
        int | None, Field(description="返回最近N条记录的数量", ge=1)
    ] = 100,
) -> str:
    """获取宏观经济数据"""
    try:
        if indicator == "money_supply":
            if data_source == "sina":
                df = ak.macro_china_money_supply()
            else:
                raise ValueError(f"Unsupported data_source for money_supply: {data_source}")
        elif indicator == "gdp":
            if data_source == "sina":
                df = ak.macro_china_gdp()
            elif data_source == "eastmoney":
                df = ak.macro_china_gdp_yearly()
            else:
                raise ValueError(f"Unsupported data_source for gdp: {data_source}")
        elif indicator == "cpi":
            df = ak.macro_china_cpi_monthly()
        elif indicator == "pmi":
            df = ak.macro_china_pmi_yearly()
        elif indicator == "stock_summary":
            if data_source == "sina":
                df = ak.stock_sse_summary()
            elif data_source == "eastmoney":
                df = ak.stock_szse_summary()
            else:
                raise ValueError(f"Unsupported data_source for stock_summary: {data_source}")
        else:
            raise ValueError(f"Unsupported indicator: {indicator}")

        if recent_n is not None:
            df = df.tail(recent_n)

        return df.to_json(orient="records")

    except Exception as e:
        return f"Error fetching macro data: {str(e)}"


@mcp.tool(name="get_investor_sentiment", description="分析散户和机构投资者的投资情绪")
def get_investor_sentiment(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    indicator: Annotated[
        Literal["retail_attention", "retail_bullish", "northbound_flow", "institution_research", "institution_participate"],
        Field(description="情绪指标: retail_attention(散户关注), retail_bullish(散户看涨), northbound_flow(北向资金), institution_research(机构调研),institution_participate(机构关注)。默认: institution_participate"),
    ] = "institution_participate",
    data_source: Annotated[
        Literal["eastmoney"],
        Field(description="数据来源: eastmoney。默认: eastmoney"),
    ] = "eastmoney",
    recent_n: Annotated[
        int | None, Field(description="返回最近N条记录的数量", ge=1)
    ] = 10,
) -> str:
    """分析散户和机构投资者的投资情绪"""
    try:
        if indicator == "retail_attention":
            if data_source == "eastmoney":
                df = ak.stock_comment_detail_scrd_focus_em(symbol)
            else:
                raise ValueError(f"Unsupported data_source for retail_attention: {data_source}")
        elif indicator == "retail_bullish":
            if data_source == "eastmoney":      
                df = ak.stock_comment_detail_scrd_desire_daily_em(symbol)
            else:
                raise ValueError(f"Unsupported data_source for retail_bullish: {data_source}")
        elif indicator == "northbound_flow":
            if data_source == "eastmoney":
                df = ak.stock_hsgt_fund_flow_summary_em()
            else:
                raise ValueError(f"Unsupported data_source for northbound_flow: {data_source}")
        elif indicator == "institution_research":
            if data_source == "eastmoney":
                df = ak.stock_institute_recommend_detail(symbol)
            else:
                raise ValueError(f"Unsupported data_source for institution_research: {data_source}")
        elif indicator == "institution_participate":
            if data_source == "eastmoney":
                df = ak.stock_comment_detail_zlkp_jgcyd_em(symbol)
            else:
                raise ValueError(f"Unsupported data_source for institution_participate: {data_source}")
        else:
            raise ValueError(f"Unsupported indicator: {indicator}")

        if recent_n is not None:
            df = df.tail(recent_n)

        return df.to_json(orient="records")

    except Exception as e:
        return f"Error fetching investor sentiment data: {str(e)}"


@mcp.tool(name="get_shareholder_info", description="获取指定股票的股东情况")
def get_shareholder_info(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    shareholder_type: Annotated[
        Literal["shareholder_count"],
        Field(description="股东类型: shareholder_count(股东户数)。默认: shareholder_count"),
    ] = "shareholder_count",
    data_source: Annotated[
        Literal["eastmoney"],
        Field(description="数据来源: eastmoney。默认: eastmoney"),
    ] = "eastmoney",
    recent_n: Annotated[
        int | None, Field(description="返回最近N条记录的数量", ge=1)
    ] = 10,
) -> str:
    """获取股东情况"""
    try:
        if shareholder_type == "shareholder_count":
            if data_source == "eastmoney":
                df = ak.stock_zh_a_gdhs_detail_em(symbol)  
                print(df)         
            else:
                raise ValueError(f"Unsupported data_source for top_circulating: {data_source}")       
        else:
            raise ValueError(f"Unsupported shareholder_type: {shareholder_type}")

        if recent_n is not None:
            df = df.tail(recent_n)

        return df.to_json(orient="records")

    except Exception as e:
        return f"Error fetching shareholder info: {str(e)}"


@mcp.tool(name="get_product_info", description="获取指定股票公司的主要产品或业务构成")
def get_product_info(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    info_type: Annotated[
        Literal["business_composition"],
        Field(description="信息类型: business_composition(主营构成)。默认: business_composition"),
    ] = "business_composition",
    data_source: Annotated[
        Literal["ths", "eastmoney"],
        Field(description="数据来源: ths(同花顺), eastmoney(东风财富网)。默认: ths"),
    ] = "ths",
    recent_n: Annotated[
        int | None, Field(description="返回最近N条记录的数量", ge=1)
    ] = 10,
) -> str:
    """获取产品情况"""
    try:
        if info_type == "business_composition":
            if data_source == "ths":
                df = ak.stock_zyjs_ths(symbol)
            elif data_source == "eastmoney":
                df = ak.stock_zygc_em(symbol)
            else:
                raise ValueError(f"Unsupported data_source for business_composition: {data_source}")       

        if recent_n is not None:
            df = df.tail(recent_n)

        return df.to_json(orient="records")

    except Exception as e:
        return f"Error fetching product info: {str(e)}"
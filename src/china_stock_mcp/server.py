from datetime import datetime
from typing import Annotated, Literal, Callable, Any, List

import akshare as ak
import akshare_one as ako
import pandas as pd
from akshare_one import indicators
from fastmcp import FastMCP
from pydantic import Field


def _fetch_data_with_fallback(
    fetch_func: Callable[..., pd.DataFrame],
    primary_source: str,
    fallback_sources: List[str],
    **kwargs: Any,
) -> pd.DataFrame:
    """
    通用的数据源故障切换辅助函数。
    按优先级尝试数据源，直到获取到有效数据或所有数据源都失败。

    Args:
        fetch_func: 实际调用 akshare 或 akshare_one 获取数据的函数。
                    这个函数应该接受 'source' 参数，或者在内部处理 source 的映射。
        primary_source: 用户指定的首选数据源。
        fallback_sources: 备用数据源列表，按优先级排序。
        **kwargs: 传递给 fetch_func 的其他参数。

    Returns:
        pd.DataFrame: 获取到的数据。

    Raises:
        RuntimeError: 如果所有数据源都未能获取到有效数据。
    """
    data_source_priority = [primary_source] + fallback_sources
    # 移除重复项并保持顺序
    seen = set()
    unique_data_source_priority = []
    for x in data_source_priority:
        if x not in seen:
            unique_data_source_priority.append(x)
            seen.add(x)

    df = None
    errors = []

    for current_source in unique_data_source_priority:
        try:
            # 假设 fetch_func 能够接受 source 参数
            # 或者 fetch_func 内部根据 kwargs 中的 source 参数进行逻辑判断
            temp_df = fetch_func(source=current_source, **kwargs)
            if temp_df is not None and not temp_df.empty:
                print(f"成功从数据源 '{current_source}' 获取数据。")
                df = temp_df
                break
            else:
                errors.append(f"数据源 '{current_source}' 返回空数据。")
        except Exception as e:
            errors.append(f"从数据源 '{current_source}' 获取数据失败: {str(e)}")

    if df is None or df.empty:
        raise RuntimeError(
            f"所有数据源都未能获取到有效数据。详细错误: {'; '.join(errors)}"
        )

    return df


mcp = FastMCP(name="china-stock-mcp")  # 初始化 FastMCP 服务器实例


@mcp.tool(
    name="get_hist_data", description="获取股票的历史行情数据，支持多种数据源和技术指标"
)
def get_hist_data(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    interval: Annotated[
        Literal["minute", "hour", "day", "week", "month", "year"],
        Field(description="时间周期: minute, hour, day, week, month, year。默认:day"),
    ] = "day",
    interval_multiplier: Annotated[int, Field(description="时间周期乘数", ge=1)] = 1,
    start_date: Annotated[
        str, Field(description="开始日期，格式为 YYYY-MM-DD")
    ] = "1970-01-01",
    end_date: Annotated[
        str, Field(description="结束日期，格式为 YYYY-MM-DD")
    ] = "2030-12-31",
    adjust: Annotated[
        Literal["none", "qfq", "hfq"],
        Field(description="复权类型: none, qfq(前复权), hfq(后复权)。默认：none"),
    ] = "none",
    indicators_list: Annotated[
        str | list[
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
        Field(
            description="要添加的技术指标，可以是逗号分隔的字符串（例如: 'SMA,EMA'）或字符串列表（例如: ['SMA', 'EMA']）。支持的指标包括: SMA, EMA, RSI, MACD, BOLL, STOCH, ATR, CCI, ADX, WILLR, AD, ADOSC, OBV, MOM, SAR, TSF, APO, AROON, AROONOSC, BOP, CMO, DX, MFI, MINUS_DI, MINUS_DM, PLUS_DI, PLUS_DM, PPO, ROC, ROCP, ROCR, ROCR100, TRIX, ULTOSC"
        ),
    ] = [
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
    ],
) -> str:
    """获取股票历史行情数据. 'eastmoney_direct' 支持所有 A, B, H 股"""

    # 定义内部 fetch_func
    def hist_data_fetcher(source: str, **kwargs: Any) -> pd.DataFrame:
        return ako.get_hist_data(source=source, **kwargs)

    df = _fetch_data_with_fallback(
        fetch_func=hist_data_fetcher,
        primary_source="eastmoney",
        fallback_sources=["eastmoney_direct", "sina"],
        symbol=symbol,
        interval=interval,
        interval_multiplier=interval_multiplier,
        start_date=start_date,
        end_date=end_date,
        adjust=adjust,
    )
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


    if isinstance(indicators_list, str):
        indicators_list = [
            indicator.strip()
            for indicator in indicators_list.split(",")
            if indicator.strip()
        ]
    
    # 过滤掉无效的指标
    if indicators_list:
        valid_indicators = []
        for indicator in indicators_list:
            if indicator in indicator_map:
                valid_indicators.append(indicator)
            else:
                print(f"警告: 指标 '{indicator}' 不存在，将被忽略。")
        indicators_list = valid_indicators
        temp = []
        for indicator in indicators_list:
            if indicator in indicator_map:
                func, params = indicator_map[indicator]
                indicator_df = func(df, **params)
                temp.append(indicator_df)
        if temp:
            df = df.join(temp)
    return df.to_json(orient="records")


@mcp.tool(
    name="get_realtime_data", description="获取股票的实时行情数据，支持多种数据源"
)
def get_realtime_data(
    symbol: Annotated[
        str | None, Field(description="股票代码 (例如: '000001')")
    ] = None,
) -> str:
    """获取实时股票行情数据. 'eastmoney_direct' """

    # 定义内部 fetch_func
    def realtime_data_fetcher(source: str, **kwargs: Any) -> pd.DataFrame:
        return ako.get_realtime_data(source=source, **kwargs)

    df = _fetch_data_with_fallback(
        fetch_func=realtime_data_fetcher,
        primary_source="eastmoney_direct",
        fallback_sources=["eastmoney", "xueqiu"],
        symbol=symbol,
    )
    return df.to_json(orient="records")


@mcp.tool(name="get_news_data", description="获取股票相关的新闻数据")
def get_news_data(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
) -> str:
    """获取股票相关新闻数据."""
    df = ako.get_news_data(symbol=symbol, source="eastmoney")
    return df.to_json(orient="records")


@mcp.tool(name="get_balance_sheet", description="获取公司的资产负债表数据")
def get_balance_sheet(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
) -> str:
    """获取公司资产负债表数据."""
    df = ako.get_balance_sheet(symbol=symbol, source="sina")
    return df.to_json(orient="records")


@mcp.tool(name="get_income_statement", description="获取公司的利润表数据")
def get_income_statement(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
) -> str:
    """获取公司利润表数据."""
    df = ako.get_income_statement(symbol=symbol, source="sina")
    return df.to_json(orient="records")


@mcp.tool(name="get_cash_flow", description="获取公司的现金流量表数据")
def get_cash_flow(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
) -> str:
    """获取公司现金流量表数据."""
    df = ako.get_cash_flow(symbol=symbol, source="sina")
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
) -> str:
    """
    获取三大财务报表的关键财务指标.
    """
    df = ako.get_financial_metrics(symbol)
    return df.to_json(orient="records")


@mcp.tool(
    name="get_time_info", description="获取当前时间（ISO格式、时间戳）和最近一个交易日"
)
def get_time_info() -> dict:
    """获取当前时间（ISO格式、时间戳）和最近一个交易日."""
    local_time = datetime.now().astimezone()
    current_date = local_time.date()

    # 获取交易日历数据
    trade_date_df = ak.tool_trade_date_hist_sina()
    trade_dates = [d for d in trade_date_df["trade_date"]]  # 提取所有交易日期

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
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
) -> str:
    """获取股票基本概要信息，支持 A 股和港股"""

    # 定义内部 fetch_func
    def get_stock_basic_info_fetcher(source: str, **kwargs: Any) -> pd.DataFrame:
        if source == "eastmoney":
            df = ak.stock_individual_info_em(symbol)
        elif source == "xueqiu":
            df = ak.stock_individual_basic_info_xq(symbol)
        elif source == "cninfo":
            df = ak.stock_profile_cninfo(symbol)
        elif source == "xq":
            df = ak.stock_individual_basic_info_hk_xq(symbol)
        return df

    df = _fetch_data_with_fallback(
        fetch_func=get_stock_basic_info_fetcher,
        primary_source="cninfo",
        fallback_sources=[
            "eastmoney",
            "xq",
            "xueqiu",
        ],
        symbol=symbol,
    )
    return df.to_json(orient="records")


@mcp.tool(name="get_macro_data", description="获取宏观经济数据")
def get_macro_data() -> str:
    """获取宏观经济数据"""

    def get_macro_data_fetcher(
        indicator: str, source: str, **kwargs: Any
    ) -> pd.DataFrame:
        if indicator == "money_supply":
            # if data_source == "sina":
            df = ak.macro_china_money_supply()
        elif indicator == "gdp":
            if source == "sina":
                df = ak.macro_china_gdp()
            # elif data_source == "eastmoney":
            else:
                df = ak.macro_china_gdp_yearly()
        elif indicator == "cpi":
            df = ak.macro_china_cpi_monthly()
        elif indicator == "pmi":
            df = ak.macro_china_pmi_yearly()
        elif indicator == "stock_summary":
            if source == "sina":
                df = ak.stock_sse_summary()
            # elif data_source == "eastmoney":
            else:
                df = ak.stock_szse_summary()
        return df

    def get_all_macro_data_fetcher(source: str, **kwargs: Any) -> pd.DataFrame:
        """
        获取所有宏观经济数据.
        
        Args:
            data_source: 数据源
            **kwargs: 其他参数
            
        Returns:
            pd.DataFrame: 包含所有宏观经济数据的DataFrame
        """
        df_list = []
        indicators = ["money_supply", "gdp", "cpi", "pmi", "stock_summary"]
        
        for indicator in indicators:
            indicator_df = get_macro_data_fetcher(indicator, source)
            if indicator_df is not None and not indicator_df.empty:
                # 为DataFrame添加指标名称列，以便区分不同指标的数据
                indicator_df['indicator'] = indicator
                df_list.append(indicator_df)
        
        if df_list:
            # 使用 pd.concat 一次性合并所有DataFrame
            df = pd.concat(df_list, ignore_index=True)
        else:
            # 如果没有获取到任何数据，返回空的DataFrame
            df = pd.DataFrame()
            
        return df

    df = _fetch_data_with_fallback(
        fetch_func=get_all_macro_data_fetcher,
        primary_source="sina",
        fallback_sources=["eastmoney"],
    )
    return df.to_json(orient="records")


@mcp.tool(name="get_investor_sentiment", description="分析散户和机构投资者的投资情绪")
def get_investor_sentiment(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],   
) -> str:
    """分析散户和机构投资者的投资情绪"""
    
    def get_investor_sentiment_fetcher(
        symbol: str, indicator: str, **kwargs: Any
    ) -> pd.DataFrame:
        """获取投资情绪数据"""       
        if indicator == "retail_attention":
            df = ak.stock_comment_detail_scrd_focus_em(symbol)
        elif indicator == "retail_bullish":
            df = ak.stock_comment_detail_scrd_desire_daily_em(symbol)           
        # elif indicator == "northbound_flow":
        #     df = ak.stock_hsgt_fund_flow_summary_em()          
        elif indicator == "institution_research":
            df = ak.stock_institute_recommend_detail(symbol)
        elif indicator == "institution_participate":       
            df = ak.stock_comment_detail_zlkp_jgcyd_em(symbol)
        return df

    def get_all_investor_sentiment_fetcher(
        symbol: str,  **kwargs: Any
    ) -> pd.DataFrame:
        df_list = []
        indicators = [
            "retail_attention",
            "retail_bullish",
            "institution_research",
            "institution_participate",
        ]
        for indicator in indicators:
            indicator_df = get_investor_sentiment_fetcher(symbol, indicator, **kwargs)
            if indicator_df is not None and not indicator_df.empty:
                # 为DataFrame添加指标名称列，以便区分不同指标的数据
                indicator_df['indicator'] = indicator
                df_list.append(indicator_df)
        if df_list:
            # 使用 pd.concat 一次性合并所有DataFrame
            df = pd.concat(df_list, ignore_index=True)
        else:
            # 如果没有获取到任何数据，返回空的DataFrame
            df = pd.DataFrame()
        return df

    df = get_all_investor_sentiment_fetcher(symbol) 
    return df.to_json(orient="records")


@mcp.tool(name="get_shareholder_info", description="获取指定股票的股东情况")
def get_shareholder_info(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")]   
) -> str:
    """获取股东情况"""
    def get_shareholder_info_fetcher(
        symbol: str, **kwargs: Any
    ) -> pd.DataFrame:
        """获取股东数据"""
        return ak.stock_zh_a_gdhs_detail_em(symbol)
    
    df = get_shareholder_info_fetcher(symbol)    
    return df.to_json(orient="records")

  


@mcp.tool(name="get_product_info", description="获取指定股票公司的主要产品或业务构成")
def get_product_info(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],   
) -> str:
    """获取产品情况"""
    def get_product_info_fetcher(
        source:str,**kwargs: Any
    ) -> pd.DataFrame:
        if source == "ths":
            df = ak.stock_zyjs_ths(symbol)
        # elif data_source == "eastmoney":
        else:
            df = ak.stock_zygc_em(symbol)
        return df
  
    df = _fetch_data_with_fallback(
        fetch_func=get_product_info_fetcher,
        primary_source="ths",
        fallback_sources=["eastmoney"],
        symbol=symbol,
    )     
    return df.to_json(orient="records")




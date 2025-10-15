from datetime import datetime
from typing import Annotated, Literal, Callable, Any, List
import io
import json

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
    if primary_source is None:
        return fetch_func(**kwargs)
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

def _get_market_from_symbol(symbol: str) -> str:
    """
    根据股票代码判断所属市场。
    上海证券交易所: sh (600, 601, 603, 605, 688 开头)
    深圳证券交易所: sz (000, 001, 002, 300 开头)
    北京证券交易所: bj (830, 870, 880 开头)
    默认返回 "sh"
    """
    if symbol.startswith(("600", "601", "603", "605", "688")):
        return "sh"
    elif symbol.startswith(("000", "001", "002", "300")):
        return "sz"
    elif symbol.startswith(("830", "870", "880")):
        return "bj"
    return "sh" # 默认上海市场

def _format_dataframe_output(
    df: pd.DataFrame,
    output_format: Literal["json", "csv", "xml", "excel", "markdown", "html"],
) -> str:
    """
    根据指定的格式格式化 DataFrame 输出。
    """
    if df.empty:
        return json.dumps([])

    if output_format == "json":
        return df.to_json(orient="records", force_ascii=False)
    elif output_format == "csv":
        return df.to_csv(index=False)
    elif output_format == "xml":
        return df.to_xml(index=False)
    elif output_format == "excel":
        # 使用 BytesIO 将 Excel 写入内存
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        # 返回 base64 编码的二进制数据，或者直接返回字节流
        # 为了兼容性，这里尝试返回 utf-8 编码的字符串，但对于二进制文件，通常直接传输字节流更合适
        return output.getvalue().decode("utf-8", errors="ignore")
    elif output_format == "markdown":
        return df.to_markdown(index=False)
    elif output_format == "html":
        return df.to_html(index=False)
    else:
        return df.to_json(orient="records", force_ascii=False)


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
        ]|None,
        Field(
            description="要添加的技术指标，可以是逗号分隔的字符串（例如: 'SMA,EMA'）或字符串列表（例如: ['SMA', 'EMA']）。支持的指标包括: SMA, EMA, RSI, MACD, BOLL, STOCH, ATR, CCI, ADX, WILLR, AD, ADOSC, OBV, MOM, SAR, TSF, APO, AROON, AROONOSC, BOP, CMO, DX, MFI, MINUS_DI, MINUS_DM, PLUS_DI, PLUS_DM, PPO, ROC, ROCP, ROCR, ROCR100, TRIX, ULTOSC。常用指标：SMA, EMA, RSI, MACD, BOLL, STOCH, OBV, MFI,建议不超过10个。"
        ),
    ] = "SMA, EMA, RSI, MACD, BOLL, STOCH, OBV, MFI",
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",
) -> str:
    """获取股票历史行情数据."""

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

    print("indicators_list: ", indicators_list)
    if indicators_list is None:
        indicators_list = []
    elif isinstance(indicators_list, str):
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
    return _format_dataframe_output(df, output_format)

@mcp.tool(
    name="get_realtime_data", description="获取股票的实时行情数据，支持多种数据源"
)
def get_realtime_data(
   symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",
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
    return _format_dataframe_output(df, output_format)

   

@mcp.tool(name="get_news_data", description="获取股票相关的新闻数据")
def get_news_data(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",
) -> str:
    """获取股票相关新闻数据."""
    df = ako.get_news_data(symbol=symbol, source="eastmoney")
    return _format_dataframe_output(df, output_format)


@mcp.tool(name="get_balance_sheet", description="获取公司的资产负债表数据")
def get_balance_sheet(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",
) -> str:
    """获取公司资产负债表数据."""
    df = ako.get_balance_sheet(symbol=symbol, source="sina")
    if df.empty:
        df = pd.DataFrame()
    return _format_dataframe_output(df, output_format)


@mcp.tool(name="get_income_statement", description="获取指定股票代码的公司的利润表数据")
def get_income_statement(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json"
) -> str:
    """获取公司利润表数据."""
    df = ako.get_income_statement(symbol=symbol, source="sina")
    if df.empty:
        df = pd.DataFrame()
    return _format_dataframe_output(df, output_format)


@mcp.tool(name="get_cash_flow", description="获取指定股票代码的公司的现金流量表数据")
def get_cash_flow(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",
) -> str:
    """获取公司现金流量表数据."""
    df = ako.get_cash_flow(symbol=symbol, source="sina")
    if df.empty:
        df = pd.DataFrame()
    return _format_dataframe_output(df, output_format)


@mcp.tool(name="get_fund_flow", description="获取股票的近 100 个交易日的资金流向数据")
def get_fund_flow(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",
) -> str:   
    market = _get_market_from_symbol(symbol)
    df = ak.stock_individual_fund_flow(stock=symbol, market=market)
    if df.empty:
        df = pd.DataFrame()
    return _format_dataframe_output(df, output_format)

@mcp.tool(name="get_inner_trade_data", description="获取公司的内部股东交易数据")
def get_inner_trade_data(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",
) -> str:
    """获取公司内部股东交易数据."""
    df = ako.get_inner_trade_data(symbol, source="xueqiu")
    if df.empty:
        df = pd.DataFrame()
    return _format_dataframe_output(df, output_format)


@mcp.tool(name="get_financial_metrics", description="获取三大财务报表的关键财务指标")
def get_financial_metrics(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",
) -> str:
    """
    获取三大财务报表的关键财务指标.
    """
    df = ako.get_financial_metrics(symbol)
    if df.empty:
        df = pd.DataFrame()
    return _format_dataframe_output(df, output_format)


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
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",
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
    if df.empty:
        df = pd.DataFrame()
    return _format_dataframe_output(df, output_format)

@mcp.tool(name="get_macro_data", description="获取单个宏观经济指标数据")
def get_macro_data(    
    indicator: Annotated[
        Literal["money_supply", "gdp", "cpi", "pmi", "stock_summary"],
        Field(description="要获取的宏观经济指标。支持的指标包括: money_supply, gdp, cpi, pmi, stock_summary。默认: 'gdp'"),
    ] = "gdp",
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json"
    ) -> str:
        """获取宏观经济数据"""

        def _clean_macro_data(df: pd.DataFrame) -> pd.DataFrame:
            """
            通用数据清洗函数，删除全 null 列和全 null 行。
            """
            if df.empty:
                return df
            # 删除所有列值都为 null 的列
            df = df.dropna(axis=1, how='all')
            # 删除所有行值都为 null 的行
            df = df.dropna(axis=0, how='all')
            return df

        def get_macro_data_fetcher(
            indicator_name: str, **kwargs: Any
        ) -> pd.DataFrame:
            if indicator_name == "money_supply":           
                df = ak.macro_china_money_supply()
            elif indicator_name == "gdp":
                df = ak.macro_china_gdp_yearly()
            elif indicator_name == "cpi":
                df = ak.macro_china_cpi_yearly()
            elif indicator_name == "pmi":
                df = ak.macro_china_pmi_yearly()
            elif indicator_name == "stock_summary":           
                df = ak.macro_china_stock_market_cap()    
            return df

        df = get_macro_data_fetcher(indicator)
        if df is not None and not df.empty:
            df = _clean_macro_data(df)
            df['indicator'] = indicator # 添加指标名称列
        else:
            df = pd.DataFrame() # 如果没有获取到数据，返回空的DataFrame
            
        return _format_dataframe_output(df, output_format)
   

@mcp.tool(name="get_investor_sentiment", description="分析散户和机构投资者的投资情绪")
def get_investor_sentiment(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")],  
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json", 
) -> str:
    """分析散户和机构投资者的投资情绪"""
    
    def get_investor_sentiment_fetcher(
        symbol: str, indicator: str, **kwargs: Any
    ) -> pd.DataFrame:
        """获取投资情绪数据"""       
        if indicator == "用户关注指数":
            df = ak.stock_comment_detail_scrd_focus_em(symbol)
        elif indicator == "日度市场参与意愿":
            df = ak.stock_comment_detail_scrd_desire_daily_em(symbol)           
        # elif indicator == "northbound_flow":
        #     df = ak.stock_hsgt_fund_flow_summary_em()          
        elif indicator == "股票评级记录":
            df = ak.stock_institute_recommend_detail(symbol)
        elif indicator == "机构参与度":       
            df = ak.stock_comment_detail_zlkp_jgcyd_em(symbol)
        return df

    def get_all_investor_sentiment_fetcher(
        symbol: str,  **kwargs: Any
    ) -> pd.DataFrame:
        df_list = []
        indicators = [
            "用户关注指数",
            "日度市场参与意愿",
            "股票评级记录",
            "机构参与度",
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
    if df.empty:
        df = pd.DataFrame()
    return _format_dataframe_output(df, output_format)



@mcp.tool(name="get_shareholder_info", description="获取指定股票的股东情况")
def get_shareholder_info(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")]  ,
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",
) -> str:
    """获取股东情况"""
    def get_shareholder_info_fetcher(
        symbol: str, **kwargs: Any
    ) -> pd.DataFrame:
        """获取股东数据"""
        return ak.stock_zh_a_gdhs_detail_em(symbol)
    
    df = get_shareholder_info_fetcher(symbol)    
    if df.empty:
        df = pd.DataFrame()
    return _format_dataframe_output(df, output_format)


@mcp.tool(name="get_product_info", description="获取指定股票公司的主要产品或业务构成")
def get_product_info(
    symbol: Annotated[str, Field(description="股票代码 (例如: '000001')")], 
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",  
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
    if df.empty:
        df = pd.DataFrame()
    return _format_dataframe_output(df, output_format)



@mcp.tool(name="get_profit_forecast", description="获取股票的业绩预测数据，包括预测年报净利润和每股收益")
def get_profit_forecast(
    symbol: Annotated[str, Field(description="股票代码 (例如: '600519')")],   
    output_format: Annotated[
        Literal["json", "csv", "xml", "excel", "markdown", "html"],
        Field(description="输出数据格式: json, csv, xml, excel, markdown, html。默认: json"),
    ] = "json",
) -> str:
    """
    获取股票的业绩预测数据。
    """
    supported_indicators = ["预测年报净利润", "预测年报每股收益"]
    df_list = []
    for ind in supported_indicators:
            temp_df = ak.stock_profit_forecast_ths(symbol=symbol, indicator=ind)
            if not temp_df.empty:
                temp_df["indicator"] = ind  # 添加指标列以便区分
                df_list.append(temp_df)
        
    if df_list:
            df = pd.concat(df_list, ignore_index=True)
    else:
        df = pd.DataFrame()
    return _format_dataframe_output(df, output_format)

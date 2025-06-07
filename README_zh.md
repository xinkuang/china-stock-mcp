# AKShare One MCP 服务器

<div align="center">
  <a href="README.md">English</a> |
  <a href="README_zh.md">中文</a>
</div>

[![smithery badge](https://smithery.ai/badge/@zwldarren/akshare-one-mcp)](https://smithery.ai/server/@zwldarren/akshare-one-mcp)

基于 [akshare-one](https://github.com/zwldarren/akshare-one) 的 MCP 服务器，提供中国股票市场数据接口，包括历史股票数据、实时数据、新闻数据、财务报表等。

<a href="https://glama.ai/mcp/servers/@zwldarren/akshare-one-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@zwldarren/akshare-one-mcp/badge" alt="akshare-one-mcp MCP 服务器" />
</a>

## 工具

### `get_hist_data`

获取历史股票数据
输入参数：

- symbol (字符串): 股票代码
- interval (字符串): 时间间隔 ('minute','hour','day','week','month','year')
- interval_multiplier (数字, 可选): 间隔倍数 (默认: 1)
- start_date (字符串, 可选): 开始日期 YYYY-MM-DD 格式 (默认: '1970-01-01')
- end_date (字符串, 可选): 结束日期 YYYY-MM-DD 格式 (默认: '2030-12-31')
- adjust (字符串, 可选): 调整类型 ('none', 'qfq', 'hfq') (默认: 'none')
- source (字符串, 可选): 数据源 ('eastmoney', 'eastmoney_direct' 'sina') (默认: 'eastmoney')

### `get_realtime_data`

获取实时股票数据
输入参数：

- symbol (字符串, 可选): 股票代码
- source (字符串, 可选): 数据源 ('xueqiu', 'eastmoney_direct') (默认: 'xueqiu')

### `get_news_data`

获取股票相关新闻数据
输入参数：

- symbol (字符串): 股票代码
- recent_n (数字, 可选): 返回最近记录的数量 (可选)

### `get_balance_sheet`

获取公司资产负债表数据
输入参数：

- symbol (字符串): 股票代码
- recent_n (数字, 可选): 返回最近记录的数量 (可选)

### `get_income_statement`

获取公司利润表数据
输入参数：

- symbol (字符串): 股票代码
- recent_n (数字, 可选): 返回最近记录的数量 (可选)

### `get_cash_flow`

获取公司现金流量表数据
输入参数：

- symbol (字符串): 股票代码
- source (字符串, 可选): 数据源 (默认: 'sina')

### `get_inner_trade_data`

获取公司内部交易数据
输入参数：

- symbol (字符串, 可选): 股票代码

### `get_time_info`

获取当前时间和最近一个交易日

## 使用说明

### 通过 Smithery 安装

要通过 [Smithery](https://smithery.ai/server/@zwldarren/akshare-one-mcp) 自动安装 akshare-one-mcp 以供 Claude Desktop 使用：

```bash
npx -y @smithery/cli install @zwldarren/akshare-one-mcp --client claude
```

### 通过 `uv` 安装

直接从 PyPI 使用 uv 安装：

```bash
uv pip install akshare-one-mcp
```

添加以下配置：

```json
"mcpServers": {
    "akshare-one-mcp": {
        "command": "uvx",
        "args": ["akshare-one-mcp"]
    }
}
```

### 通过本地源码安装

1. 克隆此仓库：

    ```bash
    git clone https://github.com/zwldarren/akshare-one-mcp.git
    cd akshare-one-mcp
    ```

2. 如果尚未安装，请先安装 [uv](<https://docs.astral.sh/uv/getting-started/installation/>)。

3. 安装依赖项：

    ```bash
    uv sync
    ```

4. 添加以下配置：

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

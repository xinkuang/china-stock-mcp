# china-stock-mcp
[![smithery badge](https://smithery.ai/badge/@xinkuang/china-stock-mcp)](https://smithery.ai/server/@xinkuang/china-stock-mcp)
一款基于 [akshare-one](https://github.com/zwldarren/akshare-one) 构建的 MCP (Model Context Protocol) 服务器，为中国股市数据提供接口。提供了一系列工具，用于获取财务信息，包括历史股票数据、实时数据、新闻数据、财务报表等。



## 🚀 核心特性

- **双模式运行**: 支持 stdio 本地模式和 HTTP 网络模式
- **丰富的财务数据**: 涵盖 A/B/H 股数据的全方位获取
- **实时数据**: 支持实时股价、交易信息等
- **财务报表**: 资产负债表、利润表、现金流量表等
- **技术指标**: 30+ 种技术指标自动计算和添加
- **新闻数据**: 股票相关新闻和公告信息
- **易用性**: 简单配置即可集成到 AI 助手 (Claude、Cursor 等)
- **数据缓存**: 内置内存和磁盘缓存机制，提高数据获取效率和响应速度
- **容器化**: 支持 Docker 部署

## 🛠️ 架构概览

### 主要组件

- `server.py`: MCP 服务器核心，定义所有工具和数据接口
- `__main__.py`: 命令行入口，支持多种运行模式
- FastMCP 框架: 处理 MCP 协议通信
- akshare-one 库: 提供底层的中国股市数据获取能力
- `cache_utils.py`: 缓存工具，提供内存和磁盘缓存功能

### 支持的数据源

- \*\*数据源故障切换\*\*: 内置 \`\_fetch\_data\_with\_fallback\` 机制，支持按优先级自动切换数据源。当首选数据源失败或返回空数据时，系统将自动尝试备用数据源，从而提高数据获取的稳定性和可靠性。

- 东方财富 (eastmoney, eastmoney_direct)
- 新浪财经 (sina)
- 雪球 (xueqiu)
## 📋 可用工具

### 1. `获取股票的历史行情数据，支持多种数据源和技术指标` (get_hist_data)

获取股票历史行情数据。

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `interval` (Literal): 时间周期: minute, hour, day, week, month, year。默认:day
- `interval_multiplier` (int): 时间周期乘数
- `start_date` (string): 开始日期，格式为 YYYY-MM-DD
- `end_date` (string): 结束日期，格式为 YYYY-MM-DD
- `adjust` (Literal): 复权类型: none, qfq(前复权), hfq(后复权)。默认：none
- \`indicators\_list\` \(string\|list\): 要添加的技术指标，可以是逗号分隔的字符串（例如: 'SMA,EMA'）或字符串列表（例如: \['SMA', 'EMA'\]）。支持的指标包括: SMA, EMA, RSI, MACD, BOLL, STOCH, ATR, CCI, ADX, WILLR, AD, ADOSC, OBV, MOM, SAR, TSF, APO, AROON, AROONOSC, BOP, CMO, DX, MFI, MINUS\_DI, MINUS\_DM, PLUS\_DI, PLUS\_DM, PPO, ROC, ROCP, ROCR, ROCR100, TRIX, ULTOSC。常用指标：SMA, EMA, RSI, MACD, BOLL, STOCH, OBV, MFI,建议不超过10个。
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 2. `获取股票的实时行情数据，支持多种数据源` (get_realtime_data)

获取实时股票行情数据，支持的数据源包括：eastmoney, eastmoney\_direct, xueqiu。

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 3. `获取股票相关的新闻数据` (get_news_data)

获取股票相关新闻数据.

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 4. `获取公司的资产负债表数据` (get_balance_sheet)

获取公司资产负债表数据.

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 5. `获取指定股票代码的公司的利润表数据` (get_income_statement)

获取公司利润表数据.

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 6. `获取指定股票代码的公司的现金流量表数据` (get_cash_flow)

获取公司现金流量表数据.

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 7. `获取股票的近 100 个交易日的资金流向数据` (get_fund_flow)

获取股票的近 100 个交易日的资金流向数据。

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 8. `获取公司的内部股东交易数据` (get_inner_trade_data)

获取公司内部股东交易数据.

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 9. `获取三大财务报表的关键财务指标` (get_financial_metrics)

获取三大财务报表的关键财务指标.

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 10. `获取当前时间（ISO格式、时间戳）和最近一个交易日` (get_time_info)

获取当前时间（ISO格式、时间戳）和最近一个交易日.

**参数:** 无

### 11. `获取指定股票的基本概要信息` (get_stock_basic_info)

获取股票基本概要信息，支持 A 股和港股

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 12. `获取单个宏观经济指标数据` (get_macro_data)

获取单个宏观经济指标数据

**参数:**
- `indicator` (Literal): 要获取的宏观经济指标。支持的指标包括: money_supply, gdp, cpi, pmi, stock_summary。默认: 'gdp'
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 13. `分析散户和机构投资者的投资情绪` (get_investor_sentiment)

分析散户和机构投资者的投资情绪

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 14. `获取指定股票的股东情况` (get_shareholder_info)

获取股东情况

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 15. `获取指定股票公司的主要产品或业务构成` (get_product_info)

获取产品情况

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 16. `获取股票的业绩预测数据，包括预测年报净利润和每股收益` (get_profit_forecast)

获取股票的业绩预测数据。

**参数:**
- `symbol` (string): 股票代码 (例如: '600519')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 17. `获取分红送股详情` (get_stock_fhps_detail)

获取指定股票的分红送股详情数据。

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown
### 18. `获取筹码分布数据` (get_stock_cyq)

获取指定股票的筹码分布数据。

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `date` (string): 查询日期，格式为 YYYY-MM-DD
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown
### 19. `获取股票研究报告` (get_stock_research_report)

获取指定股票的研究报告数据。

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 20. `获取流通股东数据` (get_stock_circulate_stock_holder)

获取指定股票的流通股东数据。

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 21. `获取高管变动数据` (get_stock_management_change)

获取指定股票的高管变动数据。

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown


### 22. `获取限售解禁数据` (get_stock_restricted_release_queue)

获取指定股票的限售解禁数据。


**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown



### 23. `获取 A 股代码和名称` (get_stock_a_code_name)

获取所有 A 股股票的代码和名称。

**参数:**
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown


### 24. `获取股票估值数据` (get_stock_value)

获取指定股票的估值数据。

**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 25. `计算指定个股的波动率指标` (get_stock_volatility)

通过分钟级历史行情计算指定个股的波动率指标。
**参数:**
- `symbol` (string): 股票代码 (例如: '000001')
- `start_date`(string): 开始日期
- `end_date`(string): 结束日期
- `period` (int): 时间周期，分钟级别 (例如: '1', '5', '15', '30', '60')")
- `adjust`(string): 复权类型: none, qfq(前复权), hfq(后复权)。默认：none
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 26. `获取所有指数的代码和基本信息` (get_all_cni_indices)

获取所有指数的代码和基本信息，去除实时变动数据并支持缓存。

**参数:**
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 27. `获取指定指数的日频率历史行情数据` (get_cni_index_hist)

获取指定指数的日频率历史行情数据。

**参数:**
- `symbol` (string): 指数代码 (例如: '399005')
- `start_date` (string): 开始日期，格式为 YYYYMMDD (例如: '20230114')
- `end_date` (string): 结束日期，格式为 YYYYMMDD (例如: '20240114')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 28. `获取指定指数的成分股样本详情` (get_cni_index_detail)

获取指定指数的成分股样本详情。

**参数:**
- `symbol` (string): 指数代码 (例如: '399001')
- `date` (string): 日期，格式为 YYYYMM (例如: '202404')
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 29. `获取技术选股指标数据，包括创新高、创新低、连续上涨、连续下跌、持续放量、持续缩量、向上突破、向下突破、量价齐升、量价齐跌、险资举牌。`(get_stock_technical_rank)

**参数:**
- `indicator_name` (string): 要获取的技术指标名称 (例如: 创新高-创月新高,  创新高-半年新高,  创新高-一年新高,  创新高-历史新高,  创新低-创月新低,  创新低-半年新低,  创新低-一年新低,  创新低-历史新低,  连续上涨,  连续下跌,  持续放量,  持续缩量,  向上突破-5日均线,  向上突破-10日均线,  向上突破-20日均线,  向上突破-30日均线,  向上突破-60日均线,  向上突破-90日均线,  向上突破-250日均线,  向上突破-500日均线,  向下突破-5日均线,  向下突破-10日均线,  向下突破-20日均线,  向下突破-30日均线,  向下突破-60日均线,  向下突破-90日均线,  向下突破-250日均线,  向下突破-500日均线,  量价齐升,  量价齐跌,  险资举牌)
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

### 30. `获取所有行业板块实时行情数据` (get_stock_board_industry_summary)
**参数:**
- `output_format` (Literal): 输出数据格式: json, csv, xml, excel, markdown, html。默认:markdown

## 🚀 安装和运行
### 方法一: 使用 Smithery

通过 [Smithery](https://smithery.ai/server/@xinkuang/china-stock-mcp) 自动安装到 Claude Desktop：

```bash
npx -y @smithery/cli install @xinkuang/china-stock-mcp
```

### 方法二: 使用 Docker

#### 1. 拉取镜像
```bash
docker pull ghcr.io/xinkuang/china-stock-mcp:latest
```

#### 2. 运行容器
```bash
docker run -p 8081:8081 ghcr.io/xinkuang/china-stock-mcp:latest
```

### 方法三: 本地源代码安装

#### 1. 环境要求
- Python 3.12+
- Git
- uv (推荐的 Python 包管理器)

#### 2. 克隆仓库
```bash
git clone https://github.com/xinkuang/china-stock-mcp
cd china-stock-mcp
```

#### 3. 安装依赖
```bash
# 推荐使用 uv 包管理器
uv sync

# 或者使用 pip
pip install -r requirements.txt
```

#### 4. 运行服务器

**stdio 模式 (默认，适用于本地 MCP 客户端):**
```bash
uv run -m china_stock_mcp
```

**HTTP 模式 (适用于远程访问):**
```bash
uv run -m china_stock_mcp --streamable-http --host 0.0.0.0 --port 8081
```

服务器将在 `http://localhost:8081/mcp` 提供服务。

## ⚙️ MCP 配置示例

### Claude Desktop 配置

编辑 `claude_desktop_config.json`：

**方式一: 本地源代码**
```json
{
  "mcpServers": {
    "china-stock-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/china_stock_mcp",
        "run",
        "china-stock-mcp"
      ]
    }
  }
}
```

**方式二: 通过 uvx**
```json
{
    "mcpServers": {
        "china-stock-mcp": {
            "command": "uvx",
            "args": [
              "china-stock-mcp"
            ]
        }
    }
}
```

**方式三: HTTP 模式**
```json
{
  "mcpServers": {
    "china-stock-mcp": {
      "command": "uvx",
      "args": ["china-stock-mcp", "--streamable-http", "--host", "0.0.0.0", "--port", "8081"],
      "env": {
        "MCP_BASE_URL": "http://localhost:8081/mcp"
      }
    }
  }
}
```

### 其他 AI 客户端配置

**Cursor:**
```json
{
  "mcpServers": {
    "china-stock-mcp": {
      "command": "uvx",
      "args": [ "china-stock-mcp"]
    }
  }
}
```

**Clion with MCP:**
```json
{
  "mcpServers": {
    "china-stock-mcp": {
      "command": "uvx",
    "args": [ "china-stock-mcp"]
    }
  }
}
```

## 🏃‍♂️ 命令行参数

- `--streamable-http`: 启用 HTTP 可流式模式 (默认: stdio 模式)
- `--host`: HTTP 模式下的绑定主机 (默认: 0.0.0.0)
- `--port`: HTTP 模式下的监听端口 (默认: 8081)

## 📊 数据支持范围

### 股票市场
- A股 (上证、深证)
- B股
- H股 (港股)
- 中小板、创业板、新三板

### 数据类型
- 历史行情数据 (分钟级、小时级、日级、周级、月级、年级)
- 实时行情数据
- 技术指标计算
- 新闻资讯
- 财务报表 (资产负债表、利润表、现金流量表)
- 财务指标
- 内部交易数据

## 🔧 开发和贡献

### 开发环境设置

1. 克隆仓库
```bash
git clone https://github.com/xinkuang/china-stock-mcp
cd china-stock-mcp
```

2. 安装开发依赖
```bash
uv sync --dev
```

3. 进入开发模式
```bash
uv run -m china_stock_mcp
```

### 代码结构

```
src/china_stock_mcp/
├── __init__.py
├── __main__.py    # 命令行入口，处理启动参数
├── server.py      # MCP 服务器核心，定义所有工具
├── mcp.json       # MCP 配置规范 (可选)
└── py.typed       # 类型标注文件
```

### 添加新工具

在 `server.py` 中使用 `@mcp.tool` 装饰器添加新工具：

```python
@mcp.tool(name="工具中文名称", description="工具的中文描述")
def your_tool_name(param1: Annotated[str, Field(description="参数描述")]) -> str:
    """工具详情描述"""
    # 实现逻辑
    pass
```

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 🙋‍♂️ 常见问题

**Q: 为什么无法获取数据？**
A: 请检查网络连接和数据源可用性。某些数据源可能有访问限制。

**Q: HTTP 模式下无法连接？**
A: 确认端口 8081 未被其他服务占用，且防火墙允许相应端口的访问。

**Q: 如何更新到最新版本？**
A: 使用 Smithery 安装的可以自动更新，手动安装的请重新拉取仓库代码。
## 🐞 调试

有关如何使用 @modelcontextprotocol/inspector 调试此服务器的详细信息，请参阅 [DEBUG.md](DEBUG.md)。


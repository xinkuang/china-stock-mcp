# china-stock-mcp
一款基于 [akshare-one](https://github.com/zwldarren/akshare-one) 构建的 MCP (Model Context Protocol) 服务器，为中国股市数据提供接口。提供了一系列工具，用于获取财务信息，包括历史股票数据、实时数据、新闻数据、财务报表等。



## 🚀 核心特性

- **双模式运行**: 支持 stdio 本地模式和 HTTP 网络模式
- **丰富的财务数据**: 涵盖 A/B/H 股数据的全方位获取
- **实时数据**: 支持实时股价、交易信息等
- **财务报表**: 资产负债表、利润表、现金流量表等
- **技术指标**: 30+ 种技术指标自动计算和添加
- **新闻数据**: 股票相关新闻和公告信息
- **易用性**: 简单配置即可集成到 AI 助手 (Claude、Cursor 等)
- **容器化**: 支持 Docker 部署

## 🛠️ 架构概览

### 主要组件

- `server.py`: MCP 服务器核心，定义所有工具和数据接口
- `__main__.py`: 命令行入口，支持多种运行模式
- FastMCP 框架: 处理 MCP 协议通信
- akshare-one 库: 提供底层的中国股市数据获取能力

### 支持的数据源

- **数据源故障切换**: 内置 `_fetch_data_with_fallback` 机制，支持按优先级自动切换数据源，提高数据获取的稳定性和可靠性。

- 东方财富 (eastmoney, eastmoney_direct)
- 新浪财经 (sina)
- 雪球 (xueqiu)
## 📋 可用工具

### 1. `获取历史行情数据` (get_hist_data)

获取股票的历史行情数据，支持多种数据源和技术指标。

**参数:**
- `symbol` (string): 股票代码，如 '000001'
- `interval` (string): 时间周期 ('minute','hour','day','week','month','year')，默认为 'day'
- `interval_multiplier` (number): 时间周期乘数，默认为 1
- `start_date` (string): 开始日期，格式为 'YYYY-MM-DD'，默认为 '1970-01-01'
- `end_date` (string): 结束日期，格式为 'YYYY-MM-DD'，默认为 '2030-12-31'
- `adjust` (string): 复权类型 ('none', 'qfq', 'hfq')，默认为 'none'
- `indicators_list` (string|list): 要添加的技术指标，可以是逗号分隔的字符串（例如: 'SMA,EMA'）或字符串列表（例如: ['SMA', 'EMA']）。支持的指标包括: SMA, EMA, RSI, MACD, BOLL, STOCH, ATR, CCI, ADX, WILLR, AD, ADOSC, OBV, MOM, SAR, TSF, APO, AROON, AROONOSC, BOP, CMO, DX, MFI, MINUS_DI, MINUS_DM, PLUS_DI, PLUS_DM, PPO, ROC, ROCP, ROCR, ROCR100, TRIX, ULTOSC


**支持的技术指标** (共 30+ 种):
SMA, EMA, RSI, MACD, BOLL, STOCH, ATR, CCI, ADX, WILLR, AD, ADOSC, OBV, MOM, SAR, TSF, APO, AROON, AROONOSC, BOP, CMO, DX, MFI, MINUS_DI, MINUS_DM, PLUS_DI, PLUS_DM, PPO, ROC, ROCP, ROCR, ROCR100, TRIX, ULTOSC

### 2. `获取实时行情数据` (get_realtime_data)

获取股票的实时行情数据，支持多种数据源。

**参数:**
- `symbol` (string, 可选): 股票代码

### 3. `获取新闻数据` (get_news_data)

获取股票相关的新闻数据。

**参数:**
- `symbol` (string): 股票代码

### 4. `获取资产负债表` (get_balance_sheet)

获取公司的资产负债表数据。

**参数:**
- `symbol` (string): 股票代码

### 5. `获取利润表` (get_income_statement)

获取公司的利润表数据。

**参数:**
- `symbol` (string): 股票代码

### 6. `获取现金流量表` (get_cash_flow)

获取公司的现金流量表数据。

**参数:**
- `symbol` (string): 股票代码

### 7. `获取内部交易数据` (get_inner_trade_data)

获取公司的内部交易数据。

**参数:**
- `symbol` (string): 股票代码

### 8. `获取财务指标` (get_financial_metrics)

获取三大财务报表的关键财务指标。

**参数:**
- `symbol` (string): 股票代码

### 9. `获取时间信息` (get_time_info)

获取当前时间的ISO格式、时间戳和最近的交易日。
### 10. `获取股票基本概要信息` (get_stock_basic_info)

获取指定股票的基本概要信息。

**参数:**
- `symbol` (string): 股票代码，如 '000001' 代表A股, '00700' 代表港股

### 11. `获取宏观经济数据` (get_macro_data)

获取宏观经济数据，包括货币供应量、GDP、CPI、PMI等指标。

### 12. `分析散户和机构投资者投资情绪` (get_investor_sentiment)

分析散户和机构投资者的投资情绪，包括散户关注度、看涨情绪、北向资金流动、机构调研等。

**参数:**
- `symbol` (string): 股票代码，如 '000001'


### 13. `获取股东情况` (get_shareholder_info)

获取指定股票的股东情况，包括十大流通股东、十大股东、股东户数、股权质押等。

**参数:**
- `symbol` (string): 股票代码，如 '000001'


### 14. `获取产品情况` (get_product_info)

获取指定股票公司的主要产品或业务构成，包括主营构成、产品类型、行业分类等。

**参数:**
- `symbol` (string): 股票代码，如 '000001'



## 🚀 安装和运行

### 方法一: 使用 Smithery

通过 [Smithery](https://smithery.ai/server/@xinkuang/china-stock-mcp) 自动安装到 Claude Desktop：

```bash
npx -y @smithery/cli install @xinkuang/china-stock-mcp --client claude
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

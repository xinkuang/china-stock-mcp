#!/bin/bash

# china-stock-mcp 调试脚本
# 使用 @modelcontextprotocol/inspector 启动调试

# 默认参数
MODE="stdio"
HOST="0.0.0.0"
PORT="8081"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --http)
      MODE="http"
      shift
      ;;
    --host)
      HOST="$2"
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    --stdio)
      MODE="stdio"
      shift
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

echo "使用 @modelcontextprotocol/inspector 启动 china-stock-mcp 服务器调试..."
echo "模式: $MODE"

if [ "$MODE" = "http" ]; then
  echo "主机: $HOST"
  echo "端口: $PORT"
  # 使用 PYTHONPATH 确保运行本地源代码
  PYTHONPATH="$PWD/src" npx @modelcontextprotocol/inspector uv run -m china_stock_mcp --streamable-http --host $HOST --port $PORT
else
  # 使用 PYTHONPATH 确保运行本地源代码
  PYTHONPATH="$PWD/src" npx @modelcontextprotocol/inspector uv run -m china_stock_mcp

fi
@echo off
REM china-stock-mcp 调试脚本
REM 使用 @modelcontextprotocol/inspector 启动调试

REM 默认参数
set MODE=stdio
set HOST=0.0.0.0
set PORT=8081

REM 解析命令行参数
:parse
if "%1"=="" goto done
if "%1"=="--http" (
  set MODE=http
  shift
  goto parse
)
if "%1"=="--host" (
  set HOST=%2
  shift
  shift
  goto parse
)
if "%1"=="--port" (
  set PORT=%2
  shift
  shift
  goto parse
)
if "%1"=="--stdio" (
  set MODE=stdio
  shift
  goto parse
)
echo 未知参数: %1
exit /b 1

:done

echo 使用 @modelcontextprotocol/inspector 启动 china-stock-mcp 服务器调试...
echo 模式: %MODE%

if "%MODE%"=="http" (
  echo 主机: %HOST%
  echo 端口: %PORT%
  npx @modelcontextprotocol/inspector uvx china-stock-mcp --streamable-http --host %HOST% --port %PORT%
) else (
  npx @modelcontextprotocol/inspector uvx china-stock-mcp
)
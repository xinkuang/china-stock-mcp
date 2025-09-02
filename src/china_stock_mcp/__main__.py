# 导入所需的库
import argparse # 用于解析命令行参数
import logging # 用于日志记录
import uvicorn # 用于 ASGI 服务器
from starlette.middleware.cors import CORSMiddleware # 用于处理跨域资源共享 (CORS)


from .server import mcp


# 初始化日志记录器
logger = logging.getLogger(__name__)


def create_streamable_http_app():
    """
    创建并配置可流式 HTTP 模式下的 FastAPI 应用。
    此应用将通过 HTTP 接口提供 MCP 服务。
    """
    app = mcp.http_app() # 获取 FastMCP 提供的 FastAPI 应用实例
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # 允许所有来源的跨域请求
        allow_credentials=True, # 允许发送凭据 (如 cookies)
        allow_methods=["GET", "POST", "OPTIONS"], # 允许的 HTTP 方法
        allow_headers=["*"], # 允许所有请求头
        expose_headers=["mcp-session-id", "mcp-protocol-version"], # 暴露给浏览器的响应头
        max_age=86400, # CORS 预检请求的缓存时间 (秒)
    )
    return app


def main():
    """
    主函数，解析命令行参数并启动MCP 服务器。
    支持 HTTP 模式和标准输入/输出 (stdio) 模式。
    """
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="china stock MCP Server - china-stock-mcp 模型上下文协议服务器")
    parser.add_argument(
        "--streamable-http",
        action="store_true",
        help="使用可流式 HTTP 模式启动服务器，而不是默认的 stdio 模式。",
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="服务器绑定的主机地址 (默认: 0.0.0.0，表示监听所有可用网络接口)"
    )
    parser.add_argument(
        "--port", type=int, default=8081, help="服务器监听的端口号 (默认: 8081)"
    )

    # 解析命令行参数
    args = parser.parse_args()

    if args.streamable_http:
        # HTTP 模式启动逻辑
        print("MCP 服务器正在以 HTTP 模式启动...")
        app = create_streamable_http_app() # 创建 HTTP 应用
        print(f"服务器监听地址: {args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port, log_level="debug") # 启动 Uvicorn ASGI 服务器
    else:
        # 标准输入/输出 (stdio) 模式启动逻辑 (默认)
        print("MCP 服务器正在以 stdio 模式启动...")
        mcp.run() # 以 stdio 模式运行 FastMCP 服务器


if __name__ == "__main__":
    # 当脚本直接执行时，调用主函数
    main()
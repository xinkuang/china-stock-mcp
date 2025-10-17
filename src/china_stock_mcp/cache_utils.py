import functools
import hashlib
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Any, Dict

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq




# 默认缓存目录
DEFAULT_CACHE_DIR = Path("./cache_data")

def _generate_cache_key(func: Callable, *args: Any, **kwargs: Any) -> str:
    """
    生成唯一的缓存键，基于函数名、位置参数和关键字参数。
    """
    # 确保 kwargs 的顺序一致性
    sorted_kwargs = sorted(kwargs.items(), key=lambda x: str(x[0]))
    # 将所有参数序列化为 JSON 字符串
    params_str = json.dumps(
        {"args": args, "kwargs": sorted_kwargs}, ensure_ascii=False, default=str
    )
    # 使用 SHA256 哈希函数生成缓存键
    hash_object = hashlib.sha256(
        (func.__qualname__ + params_str).encode("utf-8")
    )
    return hash_object.hexdigest()

def cached_data_fetch(
    mem_ttl: int = 3600,  # 默认内存缓存 1 小时 (秒)
    disk_ttl: int = 86400,     # 默认磁盘缓存 1 天 (秒)
    use_memory_cache: bool = True,
    use_disk_cache: bool = True,
    cache_dir: Path = DEFAULT_CACHE_DIR,
):
    """
    一个用于数据获取函数的缓存装饰器，支持内存缓存和本地磁盘缓存。

    Args:
        ttl (int): 缓存失效时间（秒）。
        use_memory_cache (bool): 是否使用内存缓存。
        use_disk_cache (bool): 是否使用本地磁盘缓存。
        cache_dir (Path): 本地磁盘缓存的目录。
    """

    def decorator(func: Callable) -> Callable:
        # 如果启用内存缓存，则使用 functools.lru_cache
        if use_memory_cache:
            # lru_cache 默认没有 TTL，需要手动管理
            # 这里我们只用它来存储最近访问的数据，TTL 逻辑在内部处理
            _memory_cache: Dict[str, Dict[str, Any]] = {}
        else:
            _memory_cache = {}

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_key = _generate_cache_key(func, *args, **kwargs)
            
           
            # 1. 尝试从内存缓存获取
            if use_memory_cache:
                cached_item = _memory_cache.get(cache_key)
                if cached_item and (time.time() - cached_item["timestamp"] < mem_ttl):
                    print(f"从内存缓存获取数据: {func.__name__} - {cache_key}")
                    return cached_item["data"]
                elif cached_item:
                    # 内存缓存过期
                    del _memory_cache[cache_key]

            # 2. 尝试从本地磁盘缓存获取
            if use_disk_cache:
                cache_dir.mkdir(parents=True, exist_ok=True)
                cache_file = cache_dir / f"{cache_key}.parquet"

                if cache_file.exists():
                    file_mod_time = cache_file.stat().st_mtime
                    if (time.time() - file_mod_time) < disk_ttl:
                        try:
                            print(f"从本地磁盘缓存获取数据: {func.__name__} - {cache_file}")
                            table = pq.read_table(cache_file)
                            df = table.to_pandas()
                            # 更新内存缓存
                            if use_memory_cache:
                                _memory_cache[cache_key] = {"data": df, "timestamp": time.time()}
                            return df
                        except Exception as e:
                            print(f"读取本地磁盘缓存失败 ({cache_file}): {e}，将重新获取数据。")
                            os.remove(cache_file) # 删除损坏的缓存文件
                    else:
                        print(f"本地磁盘缓存过期，删除文件: {cache_file}")
                        os.remove(cache_file) # 删除过期缓存文件

            # 3. 调用原始函数获取数据
            print(f"缓存未命中或过期，调用原始函数获取数据: {func.__name__}")
            data = func(*args, **kwargs)

            # 4. 更新缓存
            if data is not None and not data.empty:
                if use_memory_cache:
                    _memory_cache[cache_key] = {"data": data, "timestamp": time.time()}
                    print(f"数据已存入内存缓存: {func.__name__} - {cache_key}")

                if use_disk_cache:
                    cache_dir.mkdir(parents=True, exist_ok=True)
                    cache_file = cache_dir / f"{cache_key}.parquet"
                    try:
                        table = pa.Table.from_pandas(data)
                        pq.write_table(table, cache_file)
                        print(f"数据已存入本地磁盘缓存: {func.__name__} - {cache_file}")
                    except Exception as e:
                        print(f"写入本地磁盘缓存失败 ({cache_file}): {e}")
            else:
                print(f"原始函数返回空数据，不进行缓存: {func.__name__}")

            return data

        return wrapper

    return decorator
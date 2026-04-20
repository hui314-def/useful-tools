import os
import psutil

def memory_usage():
    """返回当前进程内存使用量(MB)"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

# 使用示例
start_memory = memory_usage()
# 你的代码


end_memory = memory_usage()
print(f"内存使用量: {end_memory - start_memory:.2f} MB")
import GPUtil

def get_gpu_temperature_gputil():
    """使用GPUtil获取GPU温度"""
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            return gpus[0].temperature
    except Exception as e:
        print(f"使用GPUtil获取GPU温度失败: {e}")
    return None

if __name__=='__main__':
    # 获取GPU温度
    gpu_temp = get_gpu_temperature_gputil()
    if gpu_temp:
        print(f"GPU温度: {gpu_temp}°C")


import cv2, os

def extract_frames(video_path, num_frames, output_dir="output_frames"):
    """从视频中抽取指定数量的帧并保存为图片"""
    if not os.path.exists(video_path): # 检查视频文件是否存在
        raise FileNotFoundError(f"视频文件不存在: {video_path}")
    os.makedirs(output_dir, exist_ok=True) # 创建输出目录
    cap = cv2.VideoCapture(video_path) # 打开视频文件
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # 获取视频总帧数
    if num_frames > total_frames: # 如果请求的帧数大于视频总帧数，则调整帧数为总共帧
        print(f"警告: 视频只有 {total_frames} 帧，但请求抽取 {num_frames} 帧。将抽取所有可用帧。")
        num_frames = total_frames

    frame_interval = max(1, total_frames // num_frames) # 计算帧间隔
    print(f"视频总帧数: {total_frames}")
    print(f"抽取帧数: {num_frames}")
    print(f"帧间隔: {frame_interval}")
    
    extracted_count = 0
    frame_index = 0
    while extracted_count < num_frames and frame_index < total_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index) # 设置当前帧位置
        ret, frame = cap.read() # 读取帧
        if ret:
            # 生成输出文件名
            output_filename = f"{extracted_count+1}.jpg"
            output_path = os.path.join(output_dir, output_filename)
            cv2.imwrite(output_path, frame)
            print(f"已保存: {output_path}")
            extracted_count += 1
            frame_index += frame_interval
        else:
            print(f"读取帧 {frame_index} 失败")
            break
    cap.release() # 释放视频资源
    print(f"抽帧完成! 共抽取 {extracted_count} 帧，保存在目录: {output_dir}")

if __name__ == "__main__":
    path = input('文件地址：')
    num = int(input('抽帧数量：'))
    extract_frames(path, num)
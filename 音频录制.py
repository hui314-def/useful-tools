import pyaudio
import wave

def record_audio(filename, duration=5, sample_rate=44100, chunk=1024, channels=1):
    p = pyaudio.PyAudio()
    # 打开音频流
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)
    print("开始录音...")
    frames = []
    # 录制音频数据
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    print("录音结束")
    # 停止并关闭流
    stream.stop_stream()
    stream.close()
    p.terminate()
    # 保存为 WAV 文件
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"音频已保存为: {filename}")

def play_audio(filename, chunk=1024):
    # 打开 WAV 文件
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    # 打开音频流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    print("开始播放...")
    # 读取并播放数据
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    print("播放结束")
    # 清理资源
    stream.stop_stream()
    stream.close()
    p.terminate()

def list_audio_devices():
    p = pyaudio.PyAudio()
    print("可用的音频设备:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(f"设备 {i}: {device_info['name']}")
        print(f"最大输入通道数: {device_info['maxInputChannels']}")
        print(f"最大输出通道数: {device_info['maxOutputChannels']}")
        print(f"默认采样率: {device_info['defaultSampleRate']}")
        print()
    p.terminate()

if __name__=='__main__':
    record_audio("recorded_audio.wav", duration=5)
    # play_audio("recorded_audio.wav")
    list_audio_devices()
import cv2

def start(num): # 传入摄像头索引
    # 初始化摄像头
    cap = cv2.VideoCapture(num)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,2560)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1600)
    cap.set(cv2.CAP_PROP_FPS,60)
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 创建一个可调整大小的窗口
    cv2.namedWindow('Look in my eyes!', cv2.WINDOW_NORMAL)
    print(f'分辨率：{width}X{height}')
    print(f'帧率：{fps}')

    fourcc = cv2.VideoWriter_fourcc(*'H264') # 设置编码格式
    v = cv2.VideoWriter('./out.mp4', fourcc, fps, (int(width), int(height)),isColor=True) # 设置视频文件存储对象
    while True: # 循环读取摄像头画面
        ret, frame = cap.read() # 逐帧捕获，返回是否获取到画面ret以及画面内容frame
        if not ret: # 如果正确读取帧，ret为True
            print("无法读取画面")
            break
        # 如果窗口未被销毁，则继续显示
        if cv2.getWindowProperty('Look in my eyes!', cv2.WND_PROP_VISIBLE) < 1:
            break
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 逐帧更改画面属性，转化为灰度图

        cv2.imshow('Look in my eyes!', frame) # 显示画面
        v.write(frame) # 写入帧到文件

        # 按'q'键退出循环
        if cv2.waitKey(1) == ord('q'):
            break
    # 释放摄像头资源并关闭所有OpenCV窗口
    cap.release()
    cv2.destroyAllWindows()

max_test = 5 # 测试最多5个摄像头是否可用
available = []
for i in range(max_test):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        available.append(i)
        cap.release()

if len(available)==1:
    print('使用默认摄像头')
    start(0)

elif len(available)>1:
    n = input(f'可用多个摄像头有{available}\n你要观察哪个摄像头：')
    start(n)
else:
    print('没有摄像头可用，程序退出')
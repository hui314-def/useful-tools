import pyautogui as pa
import cv2
import numpy as np
import time
'''在划定区域内实现当目标图片出现时的点击操作，需要提供模板图片click.png'''

def show(left, top, right, bottom):
    # 绘制矩形区域以便可视化
    debug_screenshot = pa.screenshot()
    debug_image = np.array(debug_screenshot)
    debug_image_bgr = cv2.cvtColor(debug_image, cv2.COLOR_RGB2BGR)
    cv2.rectangle(debug_image_bgr, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.imshow("Message Region", debug_image_bgr)
    # 等待按键，防止窗口立即关闭
    cv2.waitKey(0)  # 显示窗口，按任意键继续
    cv2.destroyAllWindows()

def click(left, top, right, bottom, name=0):
    # 定义识别区域（根据实际情况调整）
    region = (left, top, right - left, bottom - top)  # (left, top, width, height)
    a = None  # 初始化a为None
    while True:
        try:
            # 用OpenCV实现类似locateCenterOnScreen的功能
            # 截取屏幕指定区域
            screenshot = pa.screenshot(region=region)
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            # 读取模板图片
            template = cv2.imread('click.png', cv2.IMREAD_GRAYSCALE)
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            # 模板匹配
            res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            # 只有当匹配度足够高时才执行点击
            if max_val >= 0.9:
                # 计算中心点
                h, w = template.shape
                center_x = max_loc[0] + w // 2 + region[0]
                center_y = max_loc[1] + h // 2 + region[1]
                a = (center_x, center_y)
                pa.click(a[0], a[1])  # 点击
                print(f"Clicked at {a}")  # 添加日志
                time.sleep(0.5)  # 添加延迟防止连续点击
            else:
                a = None  # 重置a的值
                print("waiting...", name)
                
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)  # 出错时等待1秒再继续

if __name__ == "__main__":
    left = 1000
    top = 485
    right = 1540
    bottom = 1120
    show(left, top, right, bottom) # 可视化识别区域
    click(left, top, right, bottom)
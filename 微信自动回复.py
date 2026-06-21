from pywinauto import Application
import pyautogui as pa
import os, json, requests, pyperclip, sys, cv2
import datetime as dt
import numpy as np
import time, random
'''在微信中实现当有新消息时自动回复的功能，使用图像识别检测消息区域变化（需要手动划定区域），并使用ollama的gemma2模型生成回复'''
random.seed()

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

class Weixin:
    def __init__(self):
        try:
            app = Application().connect(title='微信',found_index=0)
        except:
            print('未找到微信应用，请检查微信是否开启')
            sys.exit()
        self.window = app.window()
        self.window.set_focus()
        self.window.maximize()
        self.rect = self.window.rectangle() # 获取窗口矩形（left, top, right, bottom）
        self.api = MyApi()
        self.message = pyperclip.paste()

    def send(self, messages:list):
        for message in messages:
            pa.click(int(self.rect.left + self.rect.width()/2), int(self.rect.top + self.rect.height()*9/10), duration=random.uniform(0.2, 0.5)) # 点击到输入框
            time.sleep(random.uniform(0.3, 0.8))
            pyperclip.copy(message) # 先复制中文到剪贴板
            pa.hotkey('ctrl', 'v')
            time.sleep(random.uniform(0.5, 1.2))
            pa.press('enter')
            time.sleep(random.uniform(2, 5))
    
    def check(self):
        """
        检查是否有新消息，如果有则点击选中并复制
        使用图像识别检测消息区域变化
        """
        # 定义消息显示区域（通常为微信窗口的中间部分）
        # 根据微信布局调整这些值
        left = int(self.rect.left + self.rect.width() * 0.2)
        top = int(self.rect.top + self.rect.height() * 0.75)
        right = int(self.rect.right - self.rect.width() * 0.5)
        bottom = int(self.rect.bottom - self.rect.height() * 0.16)
        
        show(left, top, right, bottom) # 可视化消息区域（调试用）
        
        # 创建消息区域的矩形
        msg_region = (left, top, right - left, bottom - top)
        
        # 第一次截图作为基准
        if not hasattr(self, 'prev_screenshot'):
            self.prev_screenshot = pa.screenshot(region=msg_region)
            return
        
        # 获取当前截图
        current_screenshot = pa.screenshot(region=msg_region)
        
        # 转换为numpy数组进行比较
        prev_array = np.array(self.prev_screenshot)
        curr_array = np.array(current_screenshot)
        
        # 计算图像差异
        diff = np.sum(np.abs(prev_array - curr_array))
        
        if diff > 10000:
            print(f"检测到新消息，差异值: {diff}")
            # 寻找最有可能包含新消息的区域
            try:
                # 将图像转换为灰度
                prev_gray = cv2.cvtColor(prev_array, cv2.COLOR_RGB2GRAY)
                curr_gray = cv2.cvtColor(curr_array, cv2.COLOR_RGB2GRAY)
                
                # 计算绝对差异
                diff_image = cv2.absdiff(prev_gray, curr_gray)
                
                # 阈值处理
                _, thresh = cv2.threshold(diff_image, 30, 255, cv2.THRESH_BINARY)
                
                # 寻找轮廓
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if contours:
                    # 找到最大的轮廓（假设是新消息）
                    largest_contour = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    
                    # 计算在屏幕上的实际位置
                    click_x = left + x + w // 2
                    click_y = top + y + h // 2
                    
                    # 点击消息区域
                    pa.click(click_x, click_y, duration=random.uniform(0.3, 0.6))
                    
                    # 复制消息
                    pa.hotkey('ctrl', 'a', interval=random.uniform(0.2, 0.5))
                    pa.hotkey('ctrl', 'c', interval=random.uniform(0.2, 0.5))
                    
                    # 获取剪贴板内容
                    message = pyperclip.paste()   
                    
                    if message and message.strip() and message != self.message:
                        print(f"收到消息: {message}")
                        self.message = message
                        # 获取AI回复
                        reply = self.api.run(message)
                        
                        if reply:
                            # 发送回复
                            self.send(reply)
                            self.message = pyperclip.paste()

                    # 更新基准截图
                    self.prev_screenshot = pa.screenshot(region=msg_region)
                    
            except Exception as e:
                print(f"处理新消息时出错: {e}")
                # 更新基准截图，避免重复检测
                self.prev_screenshot = pa.screenshot(region=msg_region)


class MyApi:
    def __init__(self):
        self.url='http://127.0.0.1:11434/api/chat'
        self.time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 打开程序的时间
        self.history = {}
        self.history['time'] = self.time
        self.data = {
            "model":"gemma2:latest", # 可以替换为其他模型
            "messages":[{
                "role":"system",
                "content":'角色设定：你是一个智商很高的人工智能助手。输出格式：1、可以带有表情包或颜文字，2、要求每一句话代表一个气泡消息框，不同消息框用换行符分割开，每句话不超过30词，消息框不超过5个，3、必须输出中文'
            }], # 系统提示词
            "stream":False, # 非流式回答
            "temperature": 0.8,
            "top_p": 0.7,
            "options": {"keep_alive": "10m"} # 控制模型在请求后保留在内存中的时间
        } # 发送请求的数据体

    def run(self, q)->list:
        self.data['messages'].append({"role":"user","content":q})
        try:
            resp = requests.post(self.url, json=self.data)
            resp.raise_for_status() # 向ollama发起POST请求,检查请求是否成功
            result = json.loads(resp.text)
            ans = result['message']['content']
            ans = ans.split('\n')
            ans_list = []
            for i in ans:
                if i:
                    ans_list.append(i)
                    self.data['messages'].append({"role":"assistant","content":i})
            return ans_list

        #报错响应
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP错误发生:{http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"连接错误发生:{conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"请求超时:{timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"请求错误发生:{req_err}")
        except KeyError as key_err:
            print(f"解析响应时发生键错误:{key_err}")
        except Exception as err:
            print(f"其他错误发生:{err}")

    def save(self):
        os.makedirs('微信历史对话',exist_ok=True)
        self.data['messages'].pop(0) # 不保存系统提示词
        self.history['model'] = self.data['model']
        self.history['message'] = self.data['messages']
        time_2 = dt.datetime.now().strftime("%Y年%m月%d日%H时%M分") # 保存程序的时间
        with open('微信历史对话/'+time_2+'.json','w',encoding='utf-8') as f: # 保存文件为json
            json.dump(self.history, f, indent=4, ensure_ascii=False)
        print(f'已保存到微信历史对话的文件夹，文件名为{time_2}.json')

if __name__=='__main__':
    app = Weixin()
    try:
        while True:
            if app.window.is_active() and app.window.is_maximized():
                app.check()
            time.sleep(random.uniform(2, 5))
    except KeyboardInterrupt:
        # app.api.save()
        print('退出程序')
    
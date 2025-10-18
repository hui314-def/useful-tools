import ctypes,sys
import pyautogui as pa
import tkinter as tk
pa.PAUSE=1.3

def run_as_admin():#获取管理员权限以便自动化操控游戏
    if ctypes.windll.shell32.IsUserAnAdmin():
        print("已是管理员权限。")
    else:
        print("正在尝试以管理员身份重新运行...")
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit()

def click(file,c=0.8):#点击目标图片，可能会报错
    a=pa.locateCenterOnScreen(file,confidence=c)#c为匹配相似度
    pa.click(a[0],a[1])

def searching(file,c=0.8):#避免因为找不到图片而报错
    try:
        a=pa.locateCenterOnScreen(file,confidence=c)
        pa.click(a[0],a[1])
        return True
    except:
        return False
    
def enter():#进入游戏界面的初始化
    root.iconify()#最小化
    searching('auto/0.png')
    pa.click(1280,800)
    pa.sleep(1)

def wai_quan(times=1):#刷仪器外圈
    enter()
    pa.press('f4')
    searching('auto/daohang.jpg')
    click('auto/3.jpg')
    click('auto/8.jpg')
    click('auto/9.jpg')
    pa.sleep(5)
    searching('auto/10.jpg')
    pa.sleep(50)
    if times-1!=0:
        for _ in range(times-1):
            while not searching('auto/12.jpg'):
                pa.sleep(1)
            pa.moveTo(1280,800)
    while not searching('auto/exit.jpg'):#退出按钮
        pa.sleep(1)
    pa.sleep(1)
    pa.press('esc')

def wei_tuo():#每日委托
    enter()
    pa.press('esc')
    click('auto/4.jpg')
    pa.sleep(1)
    if searching('auto/weituo.jpg'):
        click('auto/6.jpg')
        pa.press('esc')
    pa.press('esc')
    pa.press('esc')

def nei_quan(times=1):#刷仪器内圈
    enter()
    pa.press('f4')
    searching('auto/daohang.jpg')
    click('auto/go.jpg')
    pa.sleep(1)
    click('auto/neiquan.jpg')
    searching('auto/queren.jpg')
    pa.sleep(1)
    pa.keyDown('w')
    pa.sleep(2.1)
    pa.keyUp('w')
    pa.press('e')
    pa.click()
    pa.sleep(5)
    searching('auto/10.jpg')
    pa.sleep(10)
    if times-1!=0:
        for _ in range(times-1):
            while not searching('auto/12.jpg'):
                pa.sleep(1)
            pa.moveTo(1280,800)
    while not searching('auto/exit.jpg'):#退出按钮
        pa.sleep(1)

def xun_li():#无名巡礼f2
    enter()
    pa.press('f2')
    click('auto/2.jpg')
    if not searching('auto/xunli.jpg'):
        pa.press('esc')
        return 
    pa.press('esc')
    pa.press('esc')

def huo_yue():#每日活跃奖励f4
    enter()
    pa.press('f4')
    while searching('auto/huoyue.jpg',c=0.8):
        pa.sleep(1)
    if searching('auto/prize.jpg',c=0.95):
        pa.press('esc')
    pa.press('esc')

run_as_admin()
root=tk.Tk()
root.title('崩铁自动点击模拟器')
root.geometry('560x450')
root.attributes(topmost=True)
tk.Label(text='注意：请确保游戏运行').pack()
def start_actions():#选择执行的指令
    if var_wai_quan.get():
        wai_quan(v1.get())
    if var_nei_quan.get():
        nei_quan(v2.get())
    if var_wei_tuo.get():
        wei_tuo()    
    if var_huo_yue.get():
        huo_yue()
    if var_xun_li.get():
        xun_li()

var_wai_quan=tk.BooleanVar()
var_nei_quan=tk.BooleanVar()
var_huo_yue=tk.BooleanVar()
var_wei_tuo=tk.BooleanVar()
var_xun_li=tk.BooleanVar()
v1=tk.IntVar()
v1.set(1)
v2=tk.IntVar()
v2.set(1)

# 重新创建带变量的Checkbutton
for widget in root.pack_slaves():
    widget.destroy()
    
tk.Label(text='注意：请确保游戏运行！').pack()
tk.Checkbutton(text='遗器外圈', variable=var_wai_quan,font=('',20)).pack()
tk.Checkbutton(text='遗器内圈', variable=var_nei_quan,font=('',20)).pack()
tk.Checkbutton(text='每日活跃', variable=var_huo_yue,font=('',20)).pack()
tk.Checkbutton(text='无名勋礼', variable=var_xun_li,font=('',20)).pack()
tk.Checkbutton(text='每日委托', variable=var_wei_tuo,font=('',20)).pack()
tk.Button(text='开始', command=start_actions,font=('',20),width=10).pack()
tk.Label(text='刷的次数：').place(relx=0.7,rely=0.1)
tk.OptionMenu(root,v1,1,2,3,4,5,6).place(relx=0.87,rely=0.1)
tk.Label(text='刷的次数：').place(relx=0.7,rely=0.24)
tk.OptionMenu(root,v2,1,2,3,4,5,6).place(relx=0.87,rely=0.24)
root.mainloop()
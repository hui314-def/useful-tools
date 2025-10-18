import tkinter as tk
from PIL import ImageGrab,ImageTk
from tkinter import filedialog
from pyautogui import position
import os, time, psutil

def memory_usage():
    """返回当前进程内存使用量(MB)"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

class MyWin:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title('截图工具');self.root.geometry('500x280')
        self.root.attributes(topmost=True)
        self.icon_path = '剪刀.ico'# 设置窗口图标
        if os.path.exists(self.icon_path):
            self.root.iconbitmap(self.icon_path)
        self.v=tk.IntVar();self.v.set(0)
        self.var=tk.IntVar();self.var.set(0)
        self.x1=self.x2=self.y1=self.y2=None
        tk.Label(text='预览的截图可按中键保存\n注意：点击开始截屏后要从左上角按住\n拖动到右下角松开进行鼠标选取截屏!').pack()
        tk.Button(self.root,text='点击开始截屏',command=self.go,width=14,height=2,font=('',20)).pack()
        tk.Button(self.root,text='查看内存信息',command=self.print,width=14,height=2,font=('',20)).pack()
        tk.Checkbutton(text='截屏时是否隐藏该窗口',onvalue=1,offvalue=0,variable=self.v).pack()
        tk.Checkbutton(text='是否沿用上次截屏的取景框',onvalue=1,offvalue=0,variable=self.var).pack()
        self.root.mainloop()

    def print(self):
        print(memory_usage())

    def go(self):
        if self.v.get() == 1:
            self.root.iconify()
            time.sleep(0.5)

        class ViewFinder:
            def __init__(self, parent):
                self.parent = parent
                self.screen = None
                self.canvas = None
                if self.parent.var.get() == 0:
                    self.screen = tk.Tk()
                    self.screen.attributes(topmost=True, fullscreen=True, alpha=0.2)
                    self.screen.overrideredirect(True)
                    self.canvas = tk.Canvas(self.screen, highlightthickness=0)
                    self.canvas.pack(fill='both', expand=True)
                    self.screen.bind('<Button-1>', self.start_draw)
                else:
                    try:
                        self.get()
                    except Exception:
                        tk.messagebox.showerror("错误", "没有上次的取景框，请先取消选项")

            def draw_rect(self, e):
                MyWin.x2, MyWin.y2 = position()
                self.canvas.delete("rect")
                self.canvas.create_rectangle(MyWin.x1, MyWin.y1, MyWin.x2, MyWin.y2, outline='black', width=4, tags="rect")

            def start_draw(self, e):
                MyWin.x1, MyWin.y1 = position()
                self.canvas.bind('<B1-Motion>', self.draw_rect)
                self.screen.bind('<ButtonRelease-1>', self.get)

            def get(self, e=None):
                if self.parent.var.get() == 0 and self.screen:
                    self.screen.destroy()
                img = ImageGrab.grab((MyWin.x1, MyWin.y1, MyWin.x2, MyWin.y2))
                show = tk.Toplevel()
                show.attributes(topmost=True)
                show.title("截图预览")
                show.geometry(f'+{MyWin.x1-14}+{MyWin.y1-47}')
                show.resizable(False, False)
                if os.path.exists(self.parent.icon_path):
                    show.iconbitmap(self.parent.icon_path)
                i = ImageTk.PhotoImage(img)
                label = tk.Label(show, image=i)
                label.pack()
                original_img = img.copy()
                current_scale = [1.0]

                def save_img(e):
                    file_path = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=[('JPG files', '*.jpg')])
                    if file_path:
                        img.save(file_path)

                def on_mousewheel(event):
                    scale = 1.1 if event.delta > 0 else 0.9
                    current_scale[0] *= scale
                    w, h = original_img.size
                    new_w = max(1, int(w * current_scale[0]))
                    new_h = max(1, int(h * current_scale[0]))
                    resized_img = original_img.resize((new_w, new_h), ImageGrab.Image.LANCZOS)
                    new_i = ImageTk.PhotoImage(resized_img)
                    show.geometry(f"{new_w}x{new_h}")
                    label.config(image=new_i)
                    label.image = new_i
                
                show.bind('<Button-2>', save_img)
                show.bind('<MouseWheel>', on_mousewheel)
                show.mainloop()

        ViewFinder(self)

if __name__=='__main__':
    root=MyWin()

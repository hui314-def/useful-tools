import pyautogui as pa
import tkinter as tk

running = False

def change():
    global running
    running = not running
    if running:
        get()

def get():
    x, y = pa.position()
    t.config(text=f'({x},{y})')
    if running:
        root.after(10, get)

root=tk.Tk()
root.attributes(topmost=True)
root.geometry('350x100+2200+50')
t=tk.Label(text='(     )')
t.pack()
btn=tk.Button(text='获取鼠标位置',command=change)
btn.pack()
root.mainloop()
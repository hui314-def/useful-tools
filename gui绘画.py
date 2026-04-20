import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab
color='black'
width=2
eraser_radius = 10

def clear_all():
    picture.delete('all')

def pen():
    picture.unbind('<Motion>')
    picture.unbind('<MouseWheel>')
    picture.bind('<Button-1>',start_drawing)
    picture.bind('<B1-Motion>',drawing)
def start_drawing(e):
    global x,y
    x,y=e.x,e.y
def drawing(e):
    global x,y
    picture.create_line(x, y, e.x, e.y, fill=color, width=width)
    x,y=e.x,e.y

def clearing(e):
    global x, y
    r = eraser_radius
    picture.create_oval(e.x - r, e.y - r, e.x + r, e.y + r, fill='white', outline='white')
    x, y = e.x, e.y
    show_eraser_circle(e)

def show_eraser_circle(e):
    picture.delete('eraser_preview')
    r = eraser_radius
    picture.create_oval(e.x - r, e.y - r, e.x + r, e.y + r, outline='gray', width=1, tags='eraser_preview')

def update_eraser_circle(e):
    show_eraser_circle(e)

def adjust_eraser_radius(event):
    global eraser_radius
    if event.delta > 0 or getattr(event, 'num', None) == 4:
        eraser_radius = min(eraser_radius + 2, 100)
    else:
        eraser_radius = max(2, eraser_radius - 2)
    show_eraser_circle(event)

def rubber():
    picture.bind('<Button-1>', clearing)
    picture.bind('<B1-Motion>', clearing)
    picture.bind('<Motion>', update_eraser_circle)
    picture.bind('<MouseWheel>', adjust_eraser_radius)
    picture.bind('<Button-4>', adjust_eraser_radius)  # For Linux scroll up
    picture.bind('<Button-5>', adjust_eraser_radius)  # For Linux scroll down

def set():
    def ok():
        global color,width
        color=v1.get()
        width=v2.get()
        a.destroy()
        root.attributes(disabled=False)
        root.focus_force()
    a=tk.Toplevel()
    root.attributes(disabled=True)
    a.grab_set()
    a.geometry('200x100+300+300')
    v1=tk.StringVar()
    v1.set(color)
    v2=tk.IntVar()
    v2.set(width)
    tk.Label(a,text='颜色：').place(x=10,y=10)
    tk.OptionMenu(a,v1,'black','white','red','green','blue','yellow','purple','orange','brown').place(x=50,y=10)
    tk.Label(a,text='线段粗细：').place(x=10,y=50)
    tk.OptionMenu(a,v2,'1','2','3','4','5','6','7','8','9').place(x=80,y=40)
    tk.Button(a,text='确定',command=ok).place(x=50,y=70)

def save():
    x = root.winfo_rootx()+5
    y = root.winfo_rooty()+32
    x1 = x + picture.winfo_width()
    y1 = y + picture.winfo_height()-2
    a=1.74
    file_path = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=[('JPG files', '*.jpg')])
    if file_path:
        ImageGrab.grab().crop((a*x, a*y, a*x1, a*y1)).save(file_path)

root=tk.Tk()
root.geometry('1000x600+100+100')
root.title('画图软件')
canva=tk.Canvas(root,width=1000,height=30)
canva.pack()
picture=tk.Canvas(root,width=1000,height=570,bg='white')
picture.place(x=0,y=30)
btn2=tk.Button(text='保存',command=save)
btn2.place(x=60,y=0)
btn3=tk.Button(text='设置',command=set)
btn3.place(x=120,y=0)
btn4=tk.Button(text='画笔',command=pen)
btn4.place(x=180,y=0)
btn5=tk.Button(text='橡皮',command=rubber)
btn5.place(x=240,y=0)
btn6=tk.Button(text='清屏',command=clear_all)
btn6.place(x=300,y=0)
root.mainloop()
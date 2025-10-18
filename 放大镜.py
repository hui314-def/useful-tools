import tkinter as tk
from PIL import ImageGrab, ImageTk
import pyautogui as pa

zoom = 3  # 初始放大倍数

def on_key(event):
    global zoom
    if event.keysym == 'w':
        zoom = min(zoom + 1, 10)
    elif event.keysym == 's':
        zoom = max(zoom - 1, 2)

def f():
    x, y = pa.position()
    size = 200
    screen = ImageGrab.grab((x - size, y - size, x + size, y + size))
    screen = screen.resize((200 * zoom, 200 * zoom))
    img = ImageTk.PhotoImage(screen)
    canvas.delete("all")
    canvas.create_image(200, 200, image=img, anchor="center")
    canvas.image = img
    root.after(5, f)
    
root = tk.Tk()
root.title("放大器")
root.attributes(topmost=True)
root.resizable(False, False)
root.bind('<Key>', on_key)
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
f()
root.mainloop()

#import tkinter as tk

'''
class ShowSource(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)#去除标题栏
        self.attributes(alpha=0.7)
        self.attributes(topmost=True)#置顶显示窗口
        self.geometry('280x40+700+400')#窗口正中间显示
        self.bind('<B1-Motion>',self.move)
        self.bind('<ButtonRelease-1>',self.stop)
        self.bind('<Button-7>',self.esc)#鼠标右键退出
        self.get_system_info()
        self.a=tk.Label(text=info)#显示资源占用情况
        self.a.pack()
        self.time()

    def move(self,a0):#移动窗口
        self.geometry(f'280x40+{a0.x_root-140}+{a0.y_root-20}')
        self.attributes(alpha=1)
    def stop(self,e):#停止移动时恢复透明
        self.attributes(alpha=0.7)
    def esc(self,e):#退出
        sys.exit()

    def time(self):
        threading.Thread(target=self.get_system_info).start()
        self.a.config(text=info)
        self.a.after(1500, self.time)#每1.5秒更新信息

    def get_system_info(self):#获取资源占用信息
        global info
        #获取CPU和内存占用信息
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        #获取GPU占用信息
        gpus = GPUtil.getGPUs()
        gpu_usage = gpus[0].load * 100
        # 获取网络上传和下载速度
        net1 = psutil.net_io_counters()
        net2 = psutil.net_io_counters()
        upload_speed = (net2.bytes_sent - net1.bytes_sent) / 1024  # KB/s
        download_speed = (net2.bytes_recv - net1.bytes_recv) / 1024  # KB/s
        info=f'CPU: {cpu_usage}% | 内存: {mem_usage}% | GPU: {gpu_usage:.1f}% \n 上行: {upload_speed:.1f}KB/s | 下行: {download_speed:.1f}KB/s'


if __name__=='__main__':
    app=ShowSource()
    app.mainloop()
'''
# PyQt5版本实现
import sys,psutil,GPUtil,threading
from PyQt5 import QtWidgets, QtCore

class ShowSourceQt(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.7)
        self.setGeometry(700, 400, 400, 60)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(0, 0, 400, 60)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.info = ""
        self.update_info()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1500)
        self._drag_pos = None

    def mousePressEvent(self, a0):
        if a0.button() == QtCore.Qt.LeftButton:
            self._drag_pos = a0.globalPos() - self.frameGeometry().topLeft()
            self.setWindowOpacity(1)
        elif a0.button() == QtCore.Qt.RightButton:
            QtWidgets.qApp.quit()

    def mouseMoveEvent(self, a0):
        if self._drag_pos and a0.buttons() == QtCore.Qt.LeftButton:
            self.move(a0.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, a0):
        self.setWindowOpacity(0.7)
        self._drag_pos = None

    def update_info(self):
        def get_info():
            cpu_usage = psutil.cpu_percent(interval=1)
            mem_usage = psutil.virtual_memory().percent
            gpus = GPUtil.getGPUs()
            gpu_usage = gpus[0].load * 100 if gpus else 0
            net1 = psutil.net_io_counters()
            net2 = psutil.net_io_counters()
            upload_speed = (net2.bytes_sent - net1.bytes_sent) / 1024
            download_speed = (net2.bytes_recv - net1.bytes_recv) / 1024
            self.info = f'CPU: {cpu_usage}% | 内存: {mem_usage}% | GPU: {gpu_usage:.1f}% \n 上行: {upload_speed:.1f}KB/s | 下行: {download_speed:.1f}KB/s'
            self.label.setText(self.info)
        threading.Thread(target=get_info).start()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ShowSourceQt()
    win.show()
    sys.exit(app.exec_())
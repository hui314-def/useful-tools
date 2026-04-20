import sys
import os
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFileDialog, QMessageBox)
from PyQt5.QtCore import QUrl, pyqtSignal, QThread
from PyQt5.QtGui import QDesktopServices
from pynput import keyboard

class GlobalHotkeyListener(QThread):
    """全局热键监听线程，检测到 'n' 键时发射信号"""
    hotkey_pressed = pyqtSignal()

    def run(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        try:
            # 检测是否按下 'n' 键（不区分大小写）
            if hasattr(key, 'char') and key.char and key.char.lower() == 'n':
                self.hotkey_pressed.emit()
        except AttributeError:
            pass  # 忽略特殊键

class RandomVideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.current_folder = None
        self.video_files = None
        self.init_ui()
        self.installEventFilter(self)

        # 启动全局热键监听线程
        self.hotkey_listener = GlobalHotkeyListener()
        self.hotkey_listener.hotkey_pressed.connect(self.random_play)
        self.hotkey_listener.start()

    def init_ui(self):
        self.setWindowTitle('随机视频播放器')
        self.setMinimumSize(400, 150)

        # 创建控件
        self.select_folder_btn = QPushButton('选择文件夹')
        self.folder_label = QLabel('未选择文件夹')
        self.folder_label.setWordWrap(True)
        self.random_play_btn = QPushButton('随机播放')
        self.random_play_btn.setEnabled(False)  # 初始状态不可用
        self.file_label = QLabel('')  # 显示当前选中的文件名

        # 布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.select_folder_btn)
        vbox.addWidget(self.folder_label)

        hbox = QHBoxLayout()
        hbox.addWidget(self.random_play_btn)
        hbox.addStretch()
        vbox.addLayout(hbox)

        vbox.addWidget(self.file_label)
        vbox.addStretch()

        self.setLayout(vbox)

        # 信号连接
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.random_play_btn.clicked.connect(self.random_play)

    def select_folder(self):
        """打开文件夹选择对话框，并更新界面"""
        folder = QFileDialog.getExistingDirectory(self, '选择视频文件夹')
        if folder:
            self.current_folder = folder
            self.folder_label.setText(folder)
            self.random_play_btn.setEnabled(True)
            self.file_label.clear()
            self.video_files = self.get_video_files(folder)
            if not self.video_files:
                QMessageBox.information(self, '提示', '该文件夹中没有找到视频文件')
                self.random_play_btn.setEnabled(False)

    def get_video_files(self, folder):
        """返回文件夹中所有视频文件的完整路径列表"""
        video_files = []
        try:
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                if os.path.isfile(filepath):
                    ext = os.path.splitext(filename)[1].lower()
                    if ext == '.mp4':
                        video_files.append(filepath)
        except Exception as e:
            QMessageBox.critical(self, '错误', f'读取文件夹失败：{str(e)}')
        return video_files

    def random_play(self):
        """随机选择一个视频文件并用默认播放器打开"""
        if not self.current_folder:
            QMessageBox.warning(self, '警告', '请先选择一个文件夹')
            return
        
        if not self.video_files:
            QMessageBox.information(self, '提示', '该文件夹中没有找到视频文件')
            return

        # 随机选择一个
        chosen = random.choice(self.video_files)
        filename = os.path.basename(chosen)
        self.file_label.setText(f'正在播放：{filename}')

        # 使用系统默认程序打开文件
        url = QUrl.fromLocalFile(chosen)
        if not QDesktopServices.openUrl(url):
            QMessageBox.critical(self, '错误', '无法打开文件，请检查默认播放器设置')
    
    def closeEvent(self, event):
        """窗口关闭时停止监听线程"""
        self.hotkey_listener.terminate()  # 强制结束线程（简单处理）
        # 更优雅的方式是设置标志让 run() 退出，但 terminate 对本例足够
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RandomVideoPlayer()
    window.show()
    sys.exit(app.exec_())
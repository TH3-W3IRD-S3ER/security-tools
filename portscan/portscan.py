"""portscan.py - a simple TCP connect port scanner with banner grabbing.

Usage: python3 portscan.py <target> [start_port end_port]
Scan only systems you own or have written permission to test.
"""
import socket
import sys

if len(sys.argv) not in (2, 4):
    print("Usage: python3 portscan.py <target> [start_port end_port]")
    sys.exit(1)

target = sys.argv[1]

if len(sys.argv) == 4:
    try:
        start = int(sys.argv[2])
        end = int(sys.argv[3])
    except ValueError:
        print("Ports must be numbers.")
        sys.exit(1)
else:
    start, end = 1, 1024

if not (1 <= start <= end <= 65535):
    print("Ports must be between 1 and 65535, and start must not be bigger than end.")
    sys.exit(1)

print("[!] Scan only systems you own or have written permission to test.")

def check_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))
    s.close()
    return result == 0

def get_service(port):
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"

def grab_banner(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(12)
        s.connect((target, port))
        data = s.recv(1024)
        s.close()
        text = data.decode(errors="ignore").strip()
        return text.split("\n")[0][:80]
    except (socket.timeout, OSError) as e:
        print(f"    (banner error: {e})")
        return ""

for port in range(start, end + 1):
    if check_port(target, port):
        print(f"Port {port} is open ({get_service(port)})")
        banner = grab_banner(target, port)
        if banner:
            print(f"    banner: {banner}")

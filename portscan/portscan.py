"""portscan.py - a simple TCP connect port scanner.

Usage: python3 portscan.py <target>
Scan only systems you own or have written permission to test.
"""
import socket
import sys

if len(sys.argv) != 2:
    print("Usage: python3 portscan.py <target>")
    sys.exit(1)

target = sys.argv[1]
print("[!] Scan only systems you own or have written permission to test.")


def check_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))
    s.close()
    return result == 0


for port in range(1, 1025):
    if check_port(target, port):
        print(f"Port {port} is open")

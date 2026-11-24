# portscan

A simple TCP connect port scanner written in Python, built while learning offensive security.

**For authorized use only.** Scan only systems you own or have written permission to test.

## Usage

```
python3 portscan.py <target>
```

Example:

```
python3 portscan.py 192.168.241.128
```

## Example output

Run against Metasploitable2, an intentionally vulnerable VM in my isolated lab:

```
[!] Scan only systems you own or have written permission to test.
Port 21 is open
Port 22 is open
Port 23 is open
Port 25 is open
Port 53 is open
Port 80 is open
Port 111 is open
Port 139 is open
Port 445 is open
Port 512 is open
Port 513 is open
Port 514 is open
```

## How it works

- For each port from 1 to 1024, the script creates a TCP socket and tries to connect with `connect_ex`, with a 1-second timeout.
- `connect_ex` returns `0` if the full TCP handshake completes, which means the port is **open**.
- A refused connection (error `111` on Linux, a reset from the target) means the port is **closed**.
- The target is passed on the command line using `sys.argv`, and the script prints a usage message if it is missing.

## Limitations

- Checks TCP only, ports 1 to 1024 only, one port at a time.
- It completes the full handshake (a "connect scan"), so it is noisier than a SYN scan, and the target's services may log the connection.
- No service or version detection yet.
- IPv4 only.

## Planned improvements

- Show service names for open ports
- Grab service banners
- Custom port ranges
- Faster scanning with threads
- Save results to a file

## What I learned

- How sockets work, including `connect_ex` and timeouts
- Functions, loops and command-line arguments in Python
- How a connect scan differs from Nmap's SYN scan, which I observed in Wireshark in Lab 02

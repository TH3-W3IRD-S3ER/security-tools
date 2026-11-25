# portscan

A simple TCP port scanner with service names and banner grabbing, written in Python with only the standard library.

**For authorized use only.** Scan only systems you own or have written permission to test.

## Usage

```
python3 portscan.py <target> [start_port end_port]
```

Examples:

```
python3 portscan.py 192.168.241.128            # ports 1 to 1024 (default)
python3 portscan.py 192.168.241.128 20 25      # ports 20 to 25 only
```

## Example output

Scan of my Metasploitable2 lab machine (ports 20 to 25):

```
[!] Scan only systems you own or have written permission to test.
Port 21 is open (ftp)
    banner: 220 (vsFTPd 2.3.4)
Port 22 is open (ssh)
    banner: SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1
Port 23 is open (telnet)
    banner: (unreadable binary bytes)
Port 25 is open (smtp)
    banner: 220 metasploitable.localdomain ESMTP Postfix (Ubuntu)
```

## How it works

1. **Connect scan:** for each port it tries to complete a full TCP connection with `connect_ex`. If the connection succeeds, the port is open.
2. **Service name:** it looks the port number up in the system's list of standard services (`socket.getservbyport`).
3. **Banner grab:** it connects again and reads the first message the server sends, which often shows the software and version.
4. **Input checks:** the port range must be numbers from 1 to 65535, with the start not bigger than the end.

## Limitations

- **TCP only.** UDP services are not scanned. On my lab target, DNS was reachable over UDP 53 but not TCP 53, so this scanner could not see it.
- **Service names are guesses.** They come from a list of standard port numbers, not from the target. A service on an unusual port would be mislabeled (for example, port 111 shows `sunrpc` here, while Nmap calls it `rpcbind`).
- **Slow.** Ports are tested one at a time. The banner timeout is 12 seconds because the mail server in my lab waited 10 seconds before greeting me, so every silent port costs up to 12 seconds.
- **Some services stay silent** until the client speaks first (like web servers), so no banner is shown.
- **Telnet banners are binary** negotiation bytes, shown as unreadable characters.
- **Noisy:** it completes the full handshake, so the target's logs record each connection.
- IPv4 only.

## Planned improvements

- Threading, so ports are tested in parallel
- Send a small request to HTTP ports to get a banner
- Clean display of non-text banners
- Save results to a file
- UDP scanning

## What I learned

- A scan is a snapshot of one moment, so results should be checked with a second tool (I compared mine with Nmap and `netcat`).
- A timeout is a trade-off between missing slow services and making the scan slow.
- When debugging, never hide errors. Printing the error showed me the real problem in minutes.
- Banners can reveal exact software versions, which is why defenders should hide or change them.

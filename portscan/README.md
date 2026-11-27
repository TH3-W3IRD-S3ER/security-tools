# portscan

Two TCP port scanners I wrote in Python (standard library only), both with service names, banner grabbing and a custom port range.

| File | What it does |
|---|---|
| `portscan.py` | Sequential version: tests one port at a time. Simple to read. |
| `portscan_fast.py` | Multithreaded version: tests many ports at the same time (100 threads). |

**For authorized use only.** Scan only systems you own or have written permission to test.

## Usage

```
python3 portscan.py <target> [start_port end_port]
python3 portscan_fast.py <target> [start_port end_port]
```

Examples:

```
python3 portscan_fast.py 192.168.241.128            # ports 1 to 1024 (default)
python3 portscan_fast.py 192.168.241.128 20 25      # ports 20 to 25 only
```

## Example output

`portscan_fast.py` against my Metasploitable2 lab machine (ports 1 to 1024), shortened:

```
Port 21 is open (ftp)
    banner: 220 (vsFTPd 2.3.4)
Port 22 is open (ssh)
    banner: SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1
Port 25 is open (smtp)
    banner: 220 metasploitable.localdomain ESMTP Postfix (Ubuntu)
Port 80 is open (http)
    banner: (error: timed out)
Port 514 is open (shell)
    banner: getnameinfo: Temporary failure in name resolution
```

The full scan took about 12 seconds.

## How it works

1. **Connect scan:** it tries to complete a full TCP connection to each port (`connect_ex`). If it succeeds, the port is open.
2. **Service name:** it looks the port number up in the system's list of standard services (`socket.getservbyport`).
3. **Banner grab:** it connects again and reads the first message the server sends, which often reveals the software and version. Non-printable characters are removed so binary data cannot garble the terminal.
4. **Threading (`portscan_fast.py`):** a pool of 100 worker threads (`ThreadPoolExecutor`) each take the next port. Most of a scan is waiting for replies, so waiting on many ports at once is much faster. Results are collected and printed in port order at the end.
5. **Input checks:** ports must be numbers from 1 to 65535, with the start not bigger than the end.

## Why the timeout is 12 seconds

In my lab the mail server waited 10 seconds before sending its greeting, so shorter timeouts missed its banner. A longer timeout finds more banners, but each silent port makes the scanner wait. Threading removes most of that cost: all the waits overlap, so a scan takes about as long as the single slowest wait.

## Limitations

- **TCP only.** UDP services are not scanned (in my lab DNS was reachable over UDP 53 while TCP 53 was closed at one point).
- **Service names are guesses.** They come from a list of standard port numbers, not from the target. A service on an unusual port would be mislabeled.
- **Banners are best-effort.** Web servers and others stay silent until the client speaks first, so they show a timeout. Telnet sends binary negotiation bytes, so only leftover characters appear.
- **Noisy.** It completes the full handshake, so the target's logs record every connection.
- Fixed number of threads and timeout (editable in the code), IPv4 only, and results appear only when the scan finishes.

## Planned improvements

- Command-line options for thread count and timeout
- Send a small request to HTTP ports to get a real banner
- Save results to a file
- UDP scanning

## What I learned

- A scan is a snapshot of one moment, so results should be checked with a second tool (I compared mine with Nmap and `netcat`).
- A timeout is a trade-off between missing slow services and making the scan slow.
- Never hide errors when debugging: printing the real error found the problem in minutes.
- Threads help when a program spends its time waiting, and a pool of workers is better than one thread per task.
- Terminals can be garbled by binary data, so output from the network should be cleaned before printing.
- 
## A bug I found and fixed

In the first threaded version, some service names were wrong: port 21 showed `telnet` and port 25 showed `ssh`. The single-threaded version never did this.

- **Cause:** `socket.getservbyport` is not safe to call from many threads at once. It uses one shared slot for its answer, so threads overwrote each other's results (a race condition).
- **How I confirmed it:** I saved the output to a file and used `grep` on specific lines. The file itself had the wrong labels, so it was not a display glitch. (My first guess was a screen glitch, and it was wrong.)
- **Fix:** the threads now only do the slow network work. Service names are looked up one at a time, in the main thread, after all threads finish.
- **Result:** after the fix, ports 21, 25, 513 and 514 correctly showed `ftp`, `smtp`, `login` and `shell`.

**Lesson:** when many threads share something, check whether it is safe to share. And when a result looks wrong, test your guess before trusting it.

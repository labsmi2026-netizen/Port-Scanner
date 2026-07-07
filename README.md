# Advanced Port Scanner & Vulnerability Assessment Tool

## Project Overview

A professional-grade, multi-threaded TCP port scanner developed in Python 3. The tool automates network reconnaissance and security auditing by identifying open ports, capturing service banners, fingerprinting host operating systems, and mapping exposures to known critical vulnerabilities (CVEs).

This project was built and fully tested within a dedicated VMware virtual network infrastructure.

---

## Key Features & Capabilities

- **High-Speed Concurrency**: Leverages `ThreadPoolExecutor` running 200 concurrent threads to scan ranges rapidly.
- **Reliable Reconnaissance**: Implements low-level `socket.connect_ex()` TCP connect scanning.
- **Deep Fingerprinting**: Performs live banner grabbing with custom HTTP, FTP, and SMTP application layer probes.
- **Vulnerability Mapping**: Matches extracted service signatures to active critical CVE databases.
- **Dual-Format Exports**: Automatically generates an interactive dark-themed HTML visual dashboard along with clean CSV data files for security analysis.

---

## Technical Specifications

| Category | Details |
|----------|---------|
| **Language** | Python 3.13.1 |
| **Core Libraries** | `socket`, `threading`, `concurrent.futures`, `argparse`, `csv`, `datetime`, `collections` |
| **Attacker Machine** | Kali Linux 2024 (192.168.229.159) |
| **Target Environment** | Windows 10 x64 VM (192.168.229.164) |
| **Validation Baseline** | Nmap 7.99 |

---

## Usage Instructions

Run the scanner against your target machine in your lab environment:

```bash
# Basic scan with verbose output
python3 scanner_v2.py -t 192.168.229.164 -p 1-1024 -v

# Full scan with HTML report and CSV export
python3 scanner_v2.py -t 192.168.229.164 -p 1-1024 -v -T 200 --report --csv
---

## Results & Findings

Scan of the Windows 10 target (`192.168.229.164`, confirmed Windows via TTL=128):

| Metric | Result |
|---|---|
| Ports scanned | 1–1024 (1,024 total) |
| Scan time | ~1.15 s (200 threads) |
| Open ports found | **39** |
| Critical CVEs | **2** (on port 445 / SMB) |
| Validation | Nmap 7.99 `-sn` host discovery + TTL=128 |
| Output | HTML dashboard + CSV export |

### Critical Vulnerabilities Identified

| CVE | Port | Severity | Description |
|---|---|---|---|
| CVE-2017-0144 | 445/tcp | CRITICAL | **EternalBlue** — SMBv1 remote code execution, exploited by the WannaCry ransomware. |
| CVE-2020-0796 | 445/tcp | CRITICAL | **SMBGhost** — SMBv3 pre-auth remote code execution. |

Port 139 (NetBIOS-SSN) was flagged **MEDIUM**; all remaining open ports were classified **LOW**.

---

## Disclaimer

This tool was created for **educational purposes** as part of a Certified Ethical Hacker (CEH) practical training program. Only run it against systems you own or are explicitly authorized to test.

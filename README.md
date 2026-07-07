# Advanced Port Scanner & Vulnerability Assessment Tool

## 📌 Project Overview
A professional-grade, multi-threaded TCP port scanner developed in Python 3. The tool automates network reconnaissance and security auditing by identifying open ports, capturing service banners, fingerprinting host operating systems, and mapping exposures to known critical vulnerabilities (CVEs).

This project was built and fully tested within a dedicated VMware virtual network infrastructure.

## 🚀 Key Features & Capabilities
*   **High-Speed Concurrency:** Leverages `ThreadPoolExecutor` running 200 concurrent threads to scan ranges rapidly.
*   **Reliable Reconnaissance:** Implements low-level `socket.connect_ex()` TCP connect scanning.
*   **Deep Fingerprinting:** Performs live banner grabbing with custom HTTP, FTP, and SMTP application layer probes.
*   **Vulnerability Mapping:** Matches extracted service signatures to active critical CVE databases.
*   **Dual-Format Exports:** Automatically generates an interactive dark-themed HTML visual dashboard along with clean CSV data files for security analysis.

## 🛠️ Technical Specifications
*   **Language:** Python 3.13.1
*   **Core Libraries:** `socket`, `threading`, `concurrent.futures`, `argparse`, `csv`, `datetime`, `collections`
*   **Testing Infrastructure:** 
    *   **Attacker Machine:** Kali Linux 2024 (`192.168.229.130`)
    *   **Target Environment:** Windows 10 x64 Virtual Machine (`192.168.229.152`)
*   **Validation Baseline:** Nmap 7.99

## 💻 Usage Instructions
Run the scanner against your target machine inside your lab environment:

```bash
python3 scanner_v2.py -t 192.168.229.152 -p 1-1024 --report --csv
```

## 📊 Live Metrics & Validation Results
Our custom script was thoroughly cross-validated against industry-standard Nmap to audit accuracy.

### 1. Performance Summary
*   **Target Scope:** 1,024 total ports scanned (Range 1–1024)
*   **Execution Time:** Complete scan in **2.06 seconds** using 200 threads
*   **Findings:** 3 open ports discovered, 2 critical CVEs mapped

### 2. Discovered Vulnerabilities

| Port | State | Service | Mapped CVE ID | Severity | Threat Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **135/tcp** | OPEN | MSRPC | None | Medium | Windows Remote Procedure Call |
| **139/tcp** | OPEN | NetBIOS | None | Medium | NetBIOS Session Service |
| **445/tcp** | OPEN | SMB | **CVE-2017-0144** | CRITICAL | **EternalBlue** Remote Code Execution (WannaCry) |
| **445/tcp** | OPEN | SMB | **CVE-2020-0796** | CRITICAL | **SMBGhost** Pre-authentication execution exploit |

### 3. Nmap Accuracy Cross-Check (100% Match)

| Port | Nmap 7.99 Findings | Custom Scanner Findings | Verification |
| :--- | :--- | :--- | :--- |
| 135/tcp | Microsoft Windows RPC | OPEN — MSRPC | ✅ Match |
| 139/tcp | Microsoft Windows netbios-ssn | OPEN — NetBIOS-SSN | ✅ Match |
| 445/tcp | microsoft-ds (SMB) | OPEN — SMB + 2 CVEs | ✅ Match |

## 🛡️ Educational Disclaimer
This utility is intended exclusively for authorized educational labs, defensive auditing, and approved penetration testing workflows. Never execute scanning tools against systems without clear, documented ownership permissions.

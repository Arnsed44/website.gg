#!/usr/bin/env python3
"""
Standalone Data Collector Script
This script can be used to send data to the analytics platform from external sources.
"""

import requests
import json
import hashlib
import uuid
import platform
import socket
import time
from datetime import datetime

class DataCollector:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url.rstrip('/')
        self.session = requests.Session()
        
    def get_system_info(self):
        """Collect system information"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except:
            hostname = "unknown"
            local_ip = "127.0.0.1"
            
        return {
            'platform': platform.platform(),
            'system': platform.system(),
            'processor': platform.processor(),
            'machine': platform.machine(),
            'node': platform.node(),
            'hostname': hostname,
            'local_ip': local_ip,
            'python_version': platform.python_version()
        }
    
    def generate_hwid(self):
        """Generate hardware ID"""
        system_info = self.get_system_info()
        hwid_string = json.dumps(system_info, sort_keys=True)
        return hashlib.md5(hwid_string.encode()).hexdigest()
    
    def collect_and_send(self, additional_data=None):
        """Collect system data and send to server"""
        try:
            # Get public IP
            try:
                public_ip_response = self.session.get('https://httpbin.org/ip', timeout=5)
                public_ip = public_ip_response.json().get('origin', 'unknown')
            except:
                public_ip = 'unknown'
            
            # Prepare data payload
            data = {
                'browser': 'Python Script',
                'user_agent': f'DataCollector/1.0 ({platform.system()})',
                'os': platform.system(),
                'platform': platform.platform(),
                'screen_resolution': 'N/A',
                'timezone': str(datetime.now().astimezone().tzinfo),
                'language': 'en-US',
                'hardware_info': self.get_system_info(),
                'public_ip': public_ip,
                'hwid': self.generate_hwid(),
                'session_id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'collector_type': 'python_script'
            }
            
            # Add any additional data
            if additional_data:
                data.update(additional_data)
            
            # Send to server
            response = self.session.post(
                f'{self.server_url}/collect',
                json=data,
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Data sent successfully!")
                print(f"Session ID: {result.get('session_id')}")
                print(f"Hardware ID: {result.get('hwid')}")
                return True
            else:
                print(f"❌ Failed to send data: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error collecting/sending data: {e}")
            return False

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Data Collector for Analytics Platform')
    parser.add_argument('--server', default='http://localhost:5000', 
                       help='Server URL (default: http://localhost:5000)')
    parser.add_argument('--interval', type=int, default=0,
                       help='Repeat interval in seconds (0 = run once)')
    parser.add_argument('--data', type=str,
                       help='Additional JSON data to send')
    
    args = parser.parse_args()
    
    collector = DataCollector(args.server)
    
    # Parse additional data if provided
    additional_data = None
    if args.data:
        try:
            additional_data = json.loads(args.data)
        except json.JSONDecodeError:
            print("❌ Invalid JSON in --data parameter")
            return
    
    print(f"🚀 Data Collector started")
    print(f"Server: {args.server}")
    
    if args.interval > 0:
        print(f"Repeat interval: {args.interval} seconds")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                collector.collect_and_send(additional_data)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n👋 Data collection stopped")
    else:
        collector.collect_and_send(additional_data)

if __name__ == "__main__":
    main()
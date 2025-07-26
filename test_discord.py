#!/usr/bin/env python3
"""
Test script to verify Discord webhook integration
"""

import requests
import json
from datetime import datetime

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1398769513968697505/nWEKb051aJAzOkIKFQPHLqM_KTKJZ7mtyCp-xyBQIH8gWPBTuCylDp0je14EJ2Mdo9kb'

def test_discord_webhook():
    """Test the Discord webhook with a sample message"""
    try:
        # Test embed message
        test_embed = {
            "embeds": [{
                "title": "🧪 Privacy Protection Suite - Test Message",
                "color": 3447003,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "fields": [
                    {"name": "🚀 Status", "value": "System Online", "inline": True},
                    {"name": "🔧 Test Type", "value": "Discord Integration", "inline": True},
                    {"name": "⏰ Test Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": True}
                ],
                "footer": {"text": "Privacy Protection Suite - Test"}
            }]
        }
        
        print("🧪 Testing Discord webhook...")
        response = requests.post(DISCORD_WEBHOOK_URL, json=test_embed, timeout=10)
        
        if response.status_code == 204:
            print("✅ Discord webhook test successful!")
            
            # Test file upload
            test_data = {
                "test_message": "Discord integration working",
                "timestamp": datetime.now().isoformat(),
                "system_status": "operational"
            }
            
            files = {
                'file': ('test_data.json', json.dumps(test_data, indent=2), 'application/json')
            }
            
            file_message = {
                "content": "📄 Test file upload for Privacy Protection Suite"
            }
            
            print("📄 Testing file upload...")
            file_response = requests.post(DISCORD_WEBHOOK_URL, data=file_message, files=files, timeout=10)
            
            if file_response.status_code == 200:
                print("✅ File upload test successful!")
                return True
            else:
                print(f"❌ File upload failed: {file_response.status_code}")
                return False
        else:
            print(f"❌ Discord webhook test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Discord webhook: {e}")
        return False

if __name__ == "__main__":
    print("🔒 Privacy Protection Suite - Discord Integration Test")
    print("=" * 50)
    
    success = test_discord_webhook()
    
    if success:
        print("\n🎉 All tests passed! Discord integration is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check your Discord webhook URL and network connection.")
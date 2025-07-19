#!/usr/bin/env python
"""
Wazuh MOPH Notify Integration v2.0
LINE OA หมอพร้อม Integration สำหรับ Wazuh Security Alerts

Author: Your Organization
License: MIT
Repository: https://github.com/yourusername/wazuh-moph-notify
"""

import sys
import json
import requests
from datetime import datetime

# MOPH Notify Configuration
MOPH_BASE_URL = "https://morpromt2f.moph.go.th"  # UAT URL (เปลี่ยนเป็น PROD ตามต้องการ)
CLIENT_KEY = "YOUR_CLIENT_KEY"  # client-key จากเมนูหน่วยบริการ ใน CMS MOPH Notify
SECRET_KEY = "YOUR_SECRET_KEY"  # secret-key จากเมนูหน่วยบริการ ใน CMS MOPH Notify

# Version Information
VERSION = "2.0.0"
SCRIPT_NAME = "Wazuh MOPH Notify Integration"

def print_help():
    """แสดงข้อมูลวิธีการใช้งาน"""
    print(f"""
{SCRIPT_NAME} v{VERSION}
Usage: custom-moph-notify <alert_file> <dummy> <hook_url>

Parameters:
  alert_file  : Path to JSON alert file from Wazuh
  dummy       : Placeholder parameter (required by Wazuh)
  hook_url    : MOPH Notify API endpoint URL

Features:
  🎨 LINE Flex Message with beautiful UI
  🚦 Priority-based color coding and display
  📊 Smart data display based on alert level
  ✂️ Intelligent message truncation
  🛡️ Comprehensive error handling
  🔧 Production-ready configuration

Examples:
  # Basic usage
  custom-moph-notify /var/ossec/logs/alerts/alerts.json dummy https://morpromt2f.moph.go.th/api/notify/send
  
  # Show help
  custom-moph-notify --help

Configuration:
  CLIENT_KEY and SECRET_KEY must be configured in this script.
  Get these keys from: CMS MOPH Notify -> หน่วยบริการ menu

Priority Levels:
  Level 15+  → CRITICAL (🚨🔥) → ดำเนินการทันที
  Level 12+  → HIGH (🚨🔴)     → ดำเนินการด่วนภายใน 15 นาที  
  Level 7+   → MEDIUM (⚠️🟡)   → ตรวจสอบภายใน 1 ชั่วโมง
  Level 3+   → LOW (ℹ️🟢)      → บันทึกและติดตาม
  Level 0+   → INFO (📋🔵)     → ข้อมูลสำหรับการวิเคราะห์

Version: {VERSION}
Repository: https://github.com/yourusername/wazuh-moph-notify
""")

def get_max_length_by_priority(priority):
    """กำหนดความยาวของข้อความตาม Priority"""
    length_map = {
        "CRITICAL": 400,    # Alert วิกฤต - ให้ดูข้อมูลเยอะ
        "HIGH": 300,        # Alert สูง - ข้อมูลปานกลาง
        "MEDIUM": 200,      # Alert กลาง - ข้อมูลพอดี
        "LOW": 150,         # Alert ต่ำ - ข้อมูลสั้น
        "INFO": 100         # ข้อมูลทั่วไป - สั้นที่สุด
    }
    return length_map.get(priority, 200)

def smart_truncate(message, max_length=200):
    """ตัดข้อความแบบฉลาด - หาจุดตัดที่เหมาะสม"""
    if not message or len(message) <= max_length:
        return message
    
    truncated = message[:max_length]
    
    # หาจุดตัดที่เหมาะสม - ตามลำดับความสำคัญ
    # 1. หาจุดจบประโยค
    sentence_endings = ['. ', '! ', '? ', '\n', '; ']
    best_cut = -1
    
    for ending in sentence_endings:
        pos = truncated.rfind(ending)
        if pos > max_length * 0.7:  # อย่างน้อย 70% ของความยาวที่ต้องการ
            best_cut = max(best_cut, pos + len(ending) - 1)
    
    # 2. หา space ถ้าไม่เจอจุดจบประโยค
    if best_cut == -1:
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.8:  # อย่างน้อย 80% ของความยาว
            best_cut = last_space
    
    # 3. ตัดตรงความยาวที่กำหนดถ้าไม่เจออะไร
    if best_cut == -1:
        best_cut = max_length
    
    return message[:best_cut] + "... (ดูเพิ่มเติมใน Wazuh Dashboard)"

def create_flex_message(alert_data, severity_info):
    """สร้าง LINE Flex Message ตามระดับความรุนแรง"""
    
    # Header สำหรับแต่ละระดับ
    header_colors = {
        "CRITICAL": "#8B0000",  # แดงเข้ม
        "HIGH": "#DC143C",      # แดงสด
        "MEDIUM": "#FF6347",    # ส้มแดง  
        "LOW": "#32CD32",       # เขียวสด
        "INFO": "#4169E1"       # น้ำเงินสด
    }
    
    # Emoji และข้อความสำหรับแต่ละระดับ
    priority_config = {
        "CRITICAL": {
            "emoji": "🚨🔥",
            "footer": "🆘 ต้องดำเนินการทันที! ติดต่อทีม SOC",
            "urgency": "CRITICAL ALERT"
        },
        "HIGH": {
            "emoji": "🚨🔴", 
            "footer": "🚀 ดำเนินการด่วนภายใน 15 นาที",
            "urgency": "HIGH PRIORITY"
        },
        "MEDIUM": {
            "emoji": "⚠️🟡",
            "footer": "⏰ ตรวจสอบภายใน 1 ชั่วโมง",
            "urgency": "MEDIUM PRIORITY"
        },
        "LOW": {
            "emoji": "ℹ️🟢",
            "footer": "📝 บันทึกและติดตาม",
            "urgency": "LOW PRIORITY"
        },
        "INFO": {
            "emoji": "📋🔵",
            "footer": "📊 ข้อมูลสำหรับการวิเคราะห์",
            "urgency": "INFORMATION"
        }
    }
    
    priority = severity_info['priority']
    config = priority_config.get(priority, priority_config["INFO"])
    color = header_colors.get(priority, "#666666")
    
    # สร้าง body contents
    body_contents = [
        {
            "type": "text",
            "text": f"📋 {alert_data['description']}",
            "wrap": True,
            "weight": "bold",
            "margin": "md",
            "size": "md",
            "color": "#333333"
        },
        {
            "type": "separator",
            "margin": "md",
            "color": "#E0E0E0"
        }
    ]
    
    # ข้อมูลแบบ 2 คอลัมน์
    info_rows = [
        ("⚠️ ระดับ:", f"{alert_data['level']} ({priority})", color),
        ("🖥️ Agent:", alert_data['agent'], "#333333"),
        ("🔢 Rule ID:", alert_data['rule_id'], "#666666"),
        ("🌐 Source IP:", alert_data['source_ip'], "#666666")
    ]
    
    for label, value, text_color in info_rows:
        if value and str(value) != "N/A":  # แสดงเฉพาะข้อมูลที่มี
            body_contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": label,
                        "size": "sm",
                        "color": "#888888",
                        "flex": 3,
                        "weight": "bold"
                    },
                    {
                        "type": "text", 
                        "text": str(value),
                        "size": "sm",
                        "color": text_color,
                        "flex": 5,
                        "wrap": True,
                        "weight": "bold" if label.startswith("⚠️") else "regular"
                    }
                ],
                "margin": "sm"
            })
    
    # แสดง full_log หรือ message ถ้ามี
    if alert_data.get('full_log'):
        body_contents.extend([
            {
                "type": "separator",
                "margin": "md",
                "color": "#E0E0E0"
            },
            {
                "type": "text",
                "text": "📄 Log Details:",
                "size": "sm",
                "color": "#888888",
                "margin": "md",
                "weight": "bold"
            },
            {
                "type": "text",
                "text": alert_data['full_log'],
                "size": "xs",
                "color": "#444444",
                "wrap": True,
                "margin": "sm"
            }
        ])
    
    # แสดงเวลา
    body_contents.extend([
        {
            "type": "separator",
            "margin": "md",
            "color": "#E0E0E0"
        },
        {
            "type": "text",
            "text": f"⏰ {alert_data['timestamp']}",
            "size": "xs",
            "color": "#999999",
            "margin": "sm"
        }
    ])

    flex_message = {
        "type": "flex",
        "altText": f"🚨 Wazuh Alert: {alert_data['description'][:50]}...",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": color,
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{config['emoji']} Wazuh Security Alert",
                        "color": "#FFFFFF", 
                        "weight": "bold",
                        "size": "lg",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": config['urgency'],
                        "color": "#FFFFFF",
                        "size": "sm",
                        "margin": "sm",
                        "weight": "bold"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical", 
                "contents": body_contents,
                "paddingAll": "16px",
                "spacing": "sm"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#F8F9FA",
                "paddingAll": "14px",
                "contents": [
                    {
                        "type": "text",
                        "text": config['footer'],
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                        "weight": "bold"
                    }
                ]
            },
            "styles": {
                "header": {
                    "separator": False
                },
                "body": {
                    "separator": False
                },
                "footer": {
                    "separator": True,
                    "separatorColor": "#E0E0E0"
                }
            }
        }
    }
    
    return flex_message

def extract_alert_data(alert_json):
    """ดึงข้อมูลจาก Wazuh alert JSON"""
    # Extract basic fields
    alert_level = alert_json.get('rule', {}).get('level', 0)
    description = alert_json.get('rule', {}).get('description', "Unknown Alert")
    agent = alert_json.get('agent', {}).get('name', "Unknown Agent")
    timestamp = alert_json.get('timestamp', datetime.now().isoformat())
    rule_id = alert_json.get('rule', {}).get('id', "N/A")
    
    # Extract Source IP from multiple possible locations
    source_ip = "N/A"
    data_section = alert_json.get('data', {})
    
    for field in ['srcip', 'src_ip', 'source_ip', 'remote_ip']:
        if field in data_section:
            source_ip = data_section[field]
            break
    
    if source_ip == "N/A" and 'srcip' in alert_json:
        source_ip = alert_json['srcip']
    
    # Extract log message from multiple possible locations
    full_log = None
    for field in ['full_log', 'message', 'log', 'data']:
        if field in alert_json:
            if field == 'data' and isinstance(alert_json[field], dict):
                # ถ้าเป็น data object ให้ดูใน message หรือ log
                for sub_field in ['message', 'log', 'original_message']:
                    if sub_field in alert_json[field]:
                        full_log = alert_json[field][sub_field]
                        break
            else:
                full_log = alert_json[field]
                break
    
    return {
        'level': alert_level,
        'description': description,
        'agent': agent,
        'timestamp': timestamp,
        'rule_id': rule_id,
        'source_ip': source_ip,
        'raw_log': full_log
    }

def determine_priority(alert_level):
    """กำหนด priority ตาม alert level"""
    try:
        level = int(alert_level)
    except (ValueError, TypeError):
        level = 0
    
    if level >= 15:
        return "CRITICAL"
    elif level >= 12:
        return "HIGH"
    elif level >= 7:
        return "MEDIUM"
    elif level >= 3:
        return "LOW"
    else:
        return "INFO"

def validate_config():
    """ตรวจสอบการกำหนดค่า"""
    errors = []
    
    if CLIENT_KEY == "YOUR_CLIENT_KEY":
        errors.append("CLIENT_KEY ยังไม่ได้ตั้งค่า")
    
    if SECRET_KEY == "YOUR_SECRET_KEY":
        errors.append("SECRET_KEY ยังไม่ได้ตั้งค่า")
    
    if not CLIENT_KEY or not SECRET_KEY:
        errors.append("CLIENT_KEY หรือ SECRET_KEY เป็นค่าว่าง")
    
    return errors

def send_to_moph_notify(message_data, hook_url):
    """ส่งข้อความไปยัง MOPH Notify API"""
    headers = {
        'Content-Type': 'application/json',
        'client-key': CLIENT_KEY,
        'secret-key': SECRET_KEY,
        'User-Agent': f'{SCRIPT_NAME}/{VERSION}'
    }
    
    try:
        response = requests.post(
            hook_url,
            headers=headers,
            data=json.dumps(message_data),
            timeout=30
        )
        
        return response
        
    except requests.exceptions.Timeout:
        raise Exception("Request timed out after 30 seconds")
    except requests.exceptions.ConnectionError:
        raise Exception("Unable to connect to MOPH Notify API")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {str(e)}")

def main():
    """ฟังก์ชันหลัก"""
    # Check for help parameter
    if len(sys.argv) == 2 and sys.argv[1] in ['--help', '-h', 'help']:
        print_help()
        sys.exit(0)
    
    # Check minimum required parameters
    if len(sys.argv) < 4:
        print("❌ Error: Missing required parameters")
        print_help()
        sys.exit(1)
    
    # Validate configuration
    config_errors = validate_config()
    if config_errors:
        print("❌ Configuration Error:")
        for error in config_errors:
            print(f"   - {error}")
        print("\nPlease edit this script and set your actual keys from CMS MOPH Notify")
        sys.exit(1)
    
    try:
        # Read alert file
        alert_file_path = sys.argv[1]
        hook_url = sys.argv[3] if len(sys.argv) > 3 else f"{MOPH_BASE_URL}/api/notify/send"
        
        with open(alert_file_path, 'r', encoding='utf-8') as alert_file:
            alert_json = json.loads(alert_file.read())
    
    except FileNotFoundError:
        print(f"❌ Error: Alert file '{sys.argv[1]}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in alert file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading alert file: {e}")
        sys.exit(1)
    
    # Extract alert data
    alert_data = extract_alert_data(alert_json)
    priority = determine_priority(alert_data['level'])
    
    # Process log message with smart truncation
    if alert_data['raw_log']:
        max_length = get_max_length_by_priority(priority)
        alert_data['full_log'] = smart_truncate(alert_data['raw_log'], max_length)
    else:
        alert_data['full_log'] = None
    
    # Format timestamp for better readability
    try:
        dt = datetime.fromisoformat(alert_data['timestamp'].replace('Z', '+00:00'))
        alert_data['timestamp'] = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        pass  # ใช้ timestamp เดิมถ้า format ไม่ได้
    
    # Create severity info
    severity_info = {'priority': priority}
    
    # Create Flex Message
    flex_message = create_flex_message(alert_data, severity_info)
    
    # Prepare message data
    msg_data = {
        "messages": [flex_message]
    }
    
    # Debug information
    print(f"📤 Sending alert to MOPH Notify...")
    print(f"🔗 URL: {hook_url}")
    print(f"📊 Alert Level: {alert_data['level']} ({priority})")
    print(f"🖥️ Agent: {alert_data['agent']}")
    print(f"🔢 Rule ID: {alert_data['rule_id']}")
    print(f"🌐 Source IP: {alert_data['source_ip']}")
    
    if alert_data['full_log']:
        print(f"📄 Has Log Data: Yes ({len(alert_data['full_log'])} chars)")
    else:
        print("📄 Has Log Data: No")
    
    try:
        # Send the request to MOPH Notify
        response = send_to_moph_notify(msg_data, hook_url)
        
        # Check response
        if response.status_code == 200:
            print("✅ Alert sent successfully to MOPH Notify (หมอพร้อม LINE OA)")
            try:
                response_data = response.json()
                print(f"📝 Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"📝 Response: {response.text}")
        else:
            print(f"❌ Failed to send alert to MOPH Notify. Status code: {response.status_code}")
            print(f"📝 Response: {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error sending alert to MOPH Notify: {str(e)}")
        sys.exit(1)
    
    print("🎉 Integration completed successfully")
    sys.exit(0)

if __name__ == "__main__":
    main()
# 🎨 ตัวอย่าง Flex Message - Wazuh MOPH Notify Integration


## 🎨 ภาพรวม Flex Message

LINE Flex Message เป็นรูปแบบข้อความที่ให้การแสดงผลที่สวยงามและยืดหยุ่น สำหรับ Wazuh MOPH Notify Integration เราได้ออกแบบ Flex Message ที่:

- 🚦 **แยกสีตาม Priority** - ง่ายต่อการแยกแยะความสำคัญ
- 📊 **แสดงข้อมูลตาม Level** - Level สูงแสดงข้อมูลเพิ่มเติม
- 🎯 **Responsive Design** - แสดงผลดีทั้งมือถือและ Desktop
- 🛠️ **Customizable** - สามารถปรับแต่งได้ตามต้องการ

### Priority Level และสี

| Level | Priority | สี Header | Emoji | การใช้งาน |
|-------|----------|-----------|-------|-----------|
| 15+ | CRITICAL | `#8B0000` (แดงเข้ม) | 🚨🔥 | ภาวะฉุกเฉิน - ดำเนินการทันที |
| 12+ | HIGH | `#DC143C` (แดงสด) | 🚨🔴 | ความเร่งด่วนสูง - 15 นาที |
| 7+ | MEDIUM | `#FF6347` (ส้มแดง) | ⚠️🟡 | ความสำคัญปานกลาง - 1 ชั่วโมง |
| 3+ | LOW | `#32CD32` (เขียวสด) | ℹ️🟢 | ความสำคัญต่ำ - บันทึกและติดตาม |
| 0+ | INFO | `#4169E1` (น้ำเงินสด) | 📋🔵 | ข้อมูลทั่วไป - วิเคราะห์ |

---

## 🔥 ตัวอย่างตาม Priority Level

### 1. CRITICAL Alert (Level 15+)

```
🚨🔥 Wazuh Security Alert
CRITICAL ALERT
━━━━━━━━━━━━━━━━━━━━━━━━

📋 Critical system compromise detected - Multiple rootkit signatures found

⚠️ ระดับ:          15 (CRITICAL)
🖥️ Agent:          production-server-01  
🔢 Rule ID:         510002
🌐 Source IP:       10.0.1.50

📄 Log Details:
Jan 18 14:30:22 production-server-01 kernel: [malware] Suspicious rootkit activity detected in /usr/lib/systemd. Multiple system files modified. Immediate investigation required...

⏰ 2025-01-18 14:30:22 UTC

🆘 ต้องดำเนินการทันที! ติดต่อทีม SOC
```

**การแสดงผล**:
- Header สีแดงเข้ม (#8B0000)
- แสดงข้อมูลครบถ้วนทุกส่วน
- Log details แสดงเต็ม (400 characters)
- Footer เน้นความเร่งด่วน

---

### 2. HIGH Alert (Level 12+)

```
🚨🔴 Wazuh Security Alert  
HIGH PRIORITY
━━━━━━━━━━━━━━━━━━━━━━━━

📋 Multiple authentication failures from same source IP

⚠️ ระดับ:          12 (HIGH)
🖥️ Agent:          web-server-01
🔢 Rule ID:         5712  
🌐 Source IP:       192.168.1.100

📄 Log Details:
Dec 18 10:30:00 web-server-01 sshd[1234]: Failed password for admin from 192.168.1.100 port 22 ssh2. This is the 5th consecutive failed attempt from this IP address within 10 minutes...

⏰ 2025-01-18 10:30:00 UTC

🚀 ดำเนินการด่วนภายใน 15 นาที
```

**การแสดงผล**:
- Header สีแดงสด (#DC143C)
- แสดงข้อมูลครบถ้วน รวม Rule ID และ Source IP
- Log details ปานกลาง (300 characters)
- Footer แนะนำการดำเนินการ

---

### 3. MEDIUM Alert (Level 7+)

```
⚠️🟡 Wazuh Security Alert
MEDIUM PRIORITY  
━━━━━━━━━━━━━━━━━━━━━━━━

📋 SSH login from unusual location

⚠️ ระดับ:          8 (MEDIUM)
🖥️ Agent:          app-server-02
🔢 Rule ID:         5501
🌐 Source IP:       203.0.113.25

📄 Log Details:
Jan 18 09:15:30 app-server-02 sshd[5678]: Accepted publickey for user from 203.0.113.25 port 45123 ssh2...

⏰ 2025-01-18 09:15:30 UTC

⏰ ตรวจสอบภายใน 1 ชั่วโมง
```

**การแสดงผล**:
- Header สีส้มแดง (#FF6347)
- แสดงข้อมูลหลักครบถ้วน
- Log details สั้นกว่า (200 characters)
- Footer ให้เวลาปานกลาง

---

### 4. LOW Alert (Level 3+)

```
ℹ️🟢 Wazuh Security Alert
LOW PRIORITY
━━━━━━━━━━━━━━━━━━━━━━━━

📋 User logged in successfully

⚠️ ระดับ:          5 (LOW)
🖥️ Agent:          office-workstation-05
🔢 Rule ID:         5502
🌐 Source IP:       192.168.10.25

⏰ 2025-01-18 08:45:15 UTC

📝 บันทึกและติดตาม
```

**การแสดงผล**:
- Header สีเขียวสด (#32CD32)
- แสดงข้อมูลพื้นฐาน ไม่มี Log details
- ข้อมูลสั้นกระชับ (150 characters)
- Footer บอกให้บันทึก

---

### 5. INFO Alert (Level 0+)

```
📋🔵 Wazuh Security Alert
INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━

📋 System backup completed successfully

⚠️ ระดับ:          3 (INFO)
🖥️ Agent:          backup-server-01

⏰ 2025-01-18 02:00:00 UTC

📊 ข้อมูลสำหรับการวิเคราะห์
```

**การแสดงผล**:
- Header สีน้ำเงินสด (#4169E1)
- แสดงข้อมูลพื้นฐานเท่านั้น
- ไม่มี Rule ID, Source IP, Log details
- Footer เน้นการวิเคราะห์

---

## 🏗️ โครงสร้าง Flex Message

### Component Layout

```
┌─────────────────────────────────┐
│           HEADER                │  ← Priority-based color + emoji
│   🚨🔴 Wazuh Security Alert    │
│     HIGH PRIORITY               │
├─────────────────────────────────┤
│           BODY                  │
│                                 │
│ 📋 Alert Description           │  ← Main alert info
│ ───────────────────────────     │
│ ⚠️ ระดับ:    12 (HIGH)         │  ← Level & Priority
│ 🖥️ Agent:    web-server-01     │  ← Agent name
│ 🔢 Rule ID:  5712              │  ← Rule ID (if available)
│ 🌐 Source IP: 192.168.1.100    │  ← Source IP (if available)
│                                 │
│ 📄 Log Details:                │  ← Log section (if available)
│ Failed password for admin...    │
│                                 │
│ ⏰ 2025-01-18 10:30:00 UTC     │  ← Timestamp
│                                 │
├─────────────────────────────────┤
│           FOOTER                │  ← Action guidance
│ 🚀 ดำเนินการด่วนภายใน 15 นาที │
└─────────────────────────────────┘
```

### JSON Structure

```json
{
  "type": "flex",
  "altText": "🚨 Wazuh Alert: Alert description...",
  "contents": {
    "type": "bubble",
    "size": "kilo",
    "header": {
      "type": "box",
      "layout": "vertical", 
      "backgroundColor": "#DC143C",
      "contents": [...]
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [...]
    },
    "footer": {
      "type": "box", 
      "layout": "vertical",
      "backgroundColor": "#F8F9FA",
      "contents": [...]
    }
  }
}
```

---

## 🎨 การปรับแต่ง Design

### 1. เปลี่ยนสี Header

```python
# ใน custom-moph-notify.py, แก้ไข header_colors
header_colors = {
    "CRITICAL": "#B22222",    # เปลี่ยนเป็นสีแดงอ่อนขึ้น
    "HIGH": "#FF4500",        # เปลี่ยนเป็นสีส้มแดง
    "MEDIUM": "#FFA500",      # เปลี่ยนเป็นสีส้ม
    "LOW": "#228B22",         # เปลี่ยนเป็นสีเขียวเข้ม
    "INFO": "#4682B4"         # เปลี่ยนเป็นสีน้ำเงินเข้ม
}
```

### 2. เปลี่ยน Emoji และข้อความ

```python
# แก้ไข priority_config
priority_config = {
    "CRITICAL": {
        "emoji": "🔴💥",      # เปลี่ยน emoji
        "footer": "🆘 URGENT: Contact SOC immediately!",
        "urgency": "CRITICAL ALERT"
    },
    "HIGH": {
        "emoji": "🟠⚡", 
        "footer": "⚡ Action required within 30 minutes",
        "urgency": "HIGH PRIORITY"
    }
    # ... เปลี่ยนตามต้องการ
}
```

### 3. เพิ่ม Action Buttons

```python
# เพิ่มใน footer section
"footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
        {
            "type": "text",
            "text": footer_msg,
            "size": "sm",
            "color": "#666666",
            "wrap": True
        },
        {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#FF0000",
                    "action": {
                        "type": "uri",
                        "uri": f"https://wazuh-dashboard.yourorg.com/app/wazuh#/manager/rules?tab=rules&redirectRule={alert_data['rule_id']}"
                    },
                    "text": "View Rule"
                },
                {
                    "type": "button", 
                    "style": "secondary",
                    "action": {
                        "type": "uri",
                        "uri": f"https://wazuh-dashboard.yourorg.com/app/wazuh#/agents?tab=welcome&agent={alert_data['agent']}"
                    },
                    "text": "View Agent"
                }
            ]
        }
    ]
}
```

### 4. เพิ่ม Hero Image

```python
# เพิ่มใน bubble structure หลัง header
"hero": {
    "type": "image",
    "url": "https://your-cdn.com/wazuh-alert-icon.png",
    "size": "sm",
    "aspectRatio": "20:13",
    "aspectMode": "cover"
}
```

---

## 📄 ตัวอย่าง JSON Output

### CRITICAL Alert JSON

```json
{
  "type": "flex",
  "altText": "🚨 Wazuh Alert: Critical system compromise detected...",
  "contents": {
    "type": "bubble",
    "size": "kilo",
    "header": {
      "type": "box",
      "layout": "vertical",
      "backgroundColor": "#8B0000",
      "paddingAll": "16px",
      "contents": [
        {
          "type": "text",
          "text": "🚨🔥 Wazuh Security Alert",
          "color": "#FFFFFF",
          "weight": "bold",
          "size": "lg",
          "wrap": true
        },
        {
          "type": "text",
          "text": "CRITICAL ALERT",
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
      "contents": [
        {
          "type": "text",
          "text": "📋 Critical system compromise detected - Multiple rootkit signatures found",
          "wrap": true,
          "weight": "bold",
          "margin": "md",
          "size": "md",
          "color": "#333333"
        },
        {
          "type": "separator",
          "margin": "md",
          "color": "#E0E0E0"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "text",
              "text": "⚠️ ระดับ:",
              "size": "sm",
              "color": "#888888",
              "flex": 3,
              "weight": "bold"
            },
            {
              "type": "text",
              "text": "15 (CRITICAL)",
              "size": "sm",
              "color": "#8B0000",
              "flex": 5,
              "wrap": true,
              "weight": "bold"
            }
          ],
          "margin": "sm"
        }
        // ... เนื้อหาที่เหลือ
      ],
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
          "text": "🆘 ต้องดำเนินการทันที! ติดต่อทีม SOC",
          "size": "sm",
          "color": "#666666",
          "wrap": true,
          "weight": "bold"
        }
      ]
    },
    "styles": {
      "header": {
        "separator": false
      },
      "body": {
        "separator": false
      },
      "footer": {
        "separator": true,
        "separatorColor": "#E0E0E0"
      }
    }
  }
}
```

---

## 🧪 การทดสอบ Flex Message

### 1. ทดสอบด้วย Sample Alerts

```bash
# สร้างไฟล์ทดสอบสำหรับแต่ละ level
cat > /tmp/test_critical.json << 'EOF'
{
    "timestamp": "2025-01-18T14:30:22.000+0000",
    "rule": {
        "level": 15,
        "description": "Critical system compromise detected - Multiple rootkit signatures found",
        "id": "510002"
    },
    "agent": {
        "name": "production-server-01"
    },
    "data": {
        "srcip": "10.0.1.50"
    },
    "full_log": "Jan 18 14:30:22 production-server-01 kernel: [malware] Suspicious rootkit activity detected in /usr/lib/systemd. Multiple system files modified. Immediate investigation required."
}
EOF

# ทดสอบ
sudo /var/ossec/integrations/custom-moph-notify /tmp/test_critical.json dummy https://morpromt2f.moph.go.th/api/notify/send
```

### 2. ทดสอบการตัดข้อความ

```bash
# สร้าง alert ที่มี log ยาวมาก
cat > /tmp/test_long_message.json << 'EOF'
{
    "timestamp": "2025-01-18T10:30:00.000+0000",
    "rule": {
        "level": 10,
        "description": "Test long message truncation",
        "id": "99999"
    },
    "agent": {
        "name": "test-server"
    },
    "full_log": "This is a very long log message that should be truncated by the smart truncation function. It contains multiple sentences and should be cut at an appropriate point. The system should find the best place to cut this message, preferably at a sentence boundary or at least at a word boundary. This message is intentionally long to test the truncation functionality and ensure that it works properly in all scenarios."
}
EOF

# ทดสอบ
sudo /var/ossec/integrations/custom-moph-notify /tmp/test_long_message.json dummy https://morpromt2f.moph.go.th/api/notify/send
```

### 3. ตรวจสอบ JSON Structure

```bash
# เพิ่ม debug output ใน script เพื่อดู JSON structure
# แก้ไขใน custom-moph-notify.py:

# ก่อน send_to_moph_notify() เพิ่ม:
print("🔍 Debug: Flex Message JSON Structure:")
print(json.dumps(flex_message, indent=2, ensure_ascii=False))
```

### 4. ทดสอบกับ LINE Flex Message Simulator

1. ไปที่ [LINE Flex Message Simulator](https://developers.line.biz/flex-simulator/)
2. คัดลอก JSON ของ Flex Message จาก debug output
3. วาง JSON ใน simulator
4. ตรวจสอบการแสดงผลและปรับแต่งตามต้องการ

---

## 📱 Responsive Design Considerations

### Mobile View
- Text size ปรับอัตโนมัติ
- 2-column layout แสดงผลดีบนหน้าจอเล็ก
- Long text wrap properly
- Separator lines ช่วยแบ่งส่วน

### Desktop/Web View  
- ความกว้างเต็มศักยภาพ
- Font size ใหญ่ขึ้น
- Better spacing และ padding
- Action buttons แสดงผลชัดเจน

### Accessibility
- High contrast colors
- Clear font sizes
- Semantic text structure
- Alt text สำหรับ images (ถ้ามี)

---

## 🔧 Advanced Customization

### การเพิ่ม Conditional Logic

```python
def create_advanced_flex_message(alert_data, severity_info):
    # เพิ่มเงื่อนไขตาม alert type
    if "authentication" in alert_data['description'].lower():
        # ใช้ template สำหรับ auth alerts
        return create_auth_flex_message(alert_data, severity_info)
    elif "malware" in alert_data['description'].lower():
        # ใช้ template สำหรับ malware alerts  
        return create_malware_flex_message(alert_data, severity_info)
    else:
        # ใช้ template ทั่วไป
        return create_default_flex_message(alert_data, severity_info)
```

### การเพิ่ม Rich Content

```python
# เพิ่ม progress bar สำหรับ severity
def add_severity_progress_bar(level):
    max_level = 15
    progress = min(int(level) / max_level * 100, 100)
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": f"Severity: {level}/15",
                "size": "xs",
                "color": "#888888"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "flex": progress,
                        "backgroundColor": "#FF0000" if level >= 12 else "#FFA500" if level >= 7 else "#00FF00",
                        "height": "6px"
                    },
                    {
                        "type": "box", 
                        "layout": "vertical",
                        "flex": 100 - progress,
                        "backgroundColor": "#E0E0E0",
                        "height": "6px"
                    }
                ]
            }
        ]
    }
```

---

## 📊 Performance และ Limitations

### ขีดจำกัดของ LINE Flex Message
- **JSON Size**: สูงสุด ~10KB
- **Text Length**: แต่ละ text element สูงสุด ~2000 characters
- **Nested Levels**: สูงสุด 5 levels
- **Elements**: สูงสุด 50 elements ต่อ bubble

### Optimization Tips
- ใช้ `smart_truncate()` เพื่อจำกัดความยาว
- หลีกเลี่ยง nested structure ที่ซับซ้อน
- ใช้ `altText` ที่สื่อความหมาย
- Test กับ LINE Simulator ก่อน deploy

---

<div align="center">

**🎨 Flex Message ที่สวยงามและใช้งานได้จริง! 🎨**

**💡 ต้องการปรับแต่งเพิ่มเติม? ดู source code ใน `create_flex_message()`**

**🤝 แชร์ design ของคุณกับ community!**

</div>
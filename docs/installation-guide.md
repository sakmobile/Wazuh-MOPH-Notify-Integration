# 📖 คู่มือการติดตั้ง Wazuh MOPH Notify Integration

## 📋 สารบัญ

- [ข้อกำหนดเบื้องต้น](#ข้อกำหนดเบื้องต้น)
- [การเตรียมความพร้อม](#การเตรียมความพร้อม)
- [การติดตั้งแบบละเอียด](#การติดตั้งแบบละเอียด)
- [การกำหนดค่า](#การกำหนดค่า)
- [การทดสอบ](#การทดสอบ)
- [Production Deployment](#production-deployment)
- [การแก้ไขปัญหา](#การแก้ไขปัญหา)

## 🔧 ข้อกำหนดเบื้องต้น

### ระบบ Wazuh
- **Wazuh Manager**: >= 4.0
- **Operating System**: 
  - Ubuntu 18.04+
  - CentOS 7+
  - RHEL 7+
  - Debian 9+

### Python Environment
```bash
# ตรวจสอบ Python version
/var/ossec/framework/python/bin/python3 --version
# ต้องเป็น Python 3.6 หรือสูงกว่า
```

### Network Requirements
- **HTTPS connectivity** ไปยัง `morpromt2f.moph.go.th`
- **Port 443** (HTTPS) เปิดสำหรับ outbound
- **DNS resolution** สำหรับ MOPH domain

### MOPH Notify API
- **Client Key** จาก CMS MOPH Notify
- **Secret Key** จาก CMS MOPH Notify
- **LINE OA** หมอพร้อม ที่ configured แล้ว

---

## 🚀 การเตรียมความพร้อม

### 1. ตรวจสอบสถานะ Wazuh
```bash
# ตรวจสอบ service status
sudo systemctl status wazuh-manager

# ตรวจสอบ Wazuh version
sudo /var/ossec/bin/wazuh-control info

# ตรวจสอบ log space
df -h /var/ossec/logs/
```

### 2. Backup Configuration
```bash
# สร้าง backup directory
sudo mkdir -p /var/ossec/backup/$(date +%Y%m%d_%H%M%S)

# Backup ossec.conf
sudo cp /var/ossec/etc/ossec.conf /var/ossec/backup/$(date +%Y%m%d_%H%M%S)/

# Backup existing integrations (ถ้ามี)
sudo cp -r /var/ossec/integrations /var/ossec/backup/$(date +%Y%m%d_%H%M%S)/integrations.backup 2>/dev/null || echo "No existing integrations"
```

### 3. ขอ API Credentials จาก MOPH
1. **เข้าระบบ**: https://morpromt2f.moph.go.th (UAT)
2. **ไปที่เมนู**: "หน่วยบริการ" 
3. **คัดลอกข้อมูล**:
   - `client-key`
   - `secret-key`
4. **บันทึกไว้ในที่ปลอดภัย**

---

## 🛠️ การติดตั้งแบบละเอียด

### ขั้นตอนที่ 1: ดาวน์โหลดและติดตั้งไฟล์

#### วิธีที่ 1: ใช้ Git (แนะนำ)
```bash
# Clone repository
cd /tmp
git clone https://github.com/yourusername/wazuh-moph-notify.git
cd wazuh-moph-notify

# คัดลอกไฟล์ไปยัง Wazuh directory
sudo cp scripts/custom-moph-notify /var/ossec/integrations/
sudo cp scripts/custom-moph-notify.py /var/ossec/integrations/
```

#### วิธีที่ 2: ดาวน์โหลดแบบ Manual
```bash
# ดาวน์โหลดไฟล์แยก
cd /var/ossec/integrations/

# ดาวน์โหลด shell script
sudo wget https://raw.githubusercontent.com/yourusername/wazuh-moph-notify/main/scripts/custom-moph-notify

# ดาวน์โหลด Python script  
sudo wget https://raw.githubusercontent.com/yourusername/wazuh-moph-notify/main/scripts/custom-moph-notify.py
```

### ขั้นตอนที่ 2: ตั้งค่า File Permissions
```bash
# กำหนด executable permission
sudo chmod 750 /var/ossec/integrations/custom-moph-notify
sudo chmod 750 /var/ossec/integrations/custom-moph-notify.py

# กำหนด ownership
sudo chown root:wazuh /var/ossec/integrations/custom-moph-notify
sudo chown root:wazuh /var/ossec/integrations/custom-moph-notify.py

# ตรวจสอบ permissions
ls -la /var/ossec/integrations/custom-moph-notify*
```

**ผลลัพธ์ที่ถูกต้อง**:
```
-rwxr-x--- 1 root wazuh [size] [date] custom-moph-notify
-rwxr-x--- 1 root wazuh [size] [date] custom-moph-notify.py
```

### ขั้นตอนที่ 3: ติดตั้ง Python Dependencies
```bash
# ตรวจสอบ requests module
sudo /var/ossec/framework/python/bin/python3 -c "import requests; print('✅ requests module OK')"

# ถ้าไม่มี requests ให้ติดตั้ง
sudo /var/ossec/framework/python/bin/python3 -m pip install requests

# ตรวจสอบ modules อื่นๆ
sudo /var/ossec/framework/python/bin/python3 -c "
import sys, json, requests
from datetime import datetime
print('✅ All required modules available')
print(f'Python: {sys.version}')
print(f'Requests: {requests.__version__}')
"
```

---

## ⚙️ การกำหนดค่า

### ขั้นตอนที่ 4: กำหนด API Credentials
```bash
# แก้ไข Python script
sudo nano /var/ossec/integrations/custom-moph-notify.py
```

**ค้นหาและแก้ไขบรรทัดเหล่านี้**:
```python
CLIENT_KEY = "YOUR_CLIENT_KEY"  # แทนที่ด้วย client-key จริง
SECRET_KEY = "YOUR_SECRET_KEY"  # แทนที่ด้วย secret-key จริง
```

**ตัวอย่าง**:
```python
CLIENT_KEY = "moph_client_abc123xyz789"
SECRET_KEY = "moph_secret_def456uvw012"
```

### ขั้นตอนที่ 5: แก้ไข ossec.conf
```bash
# แก้ไข configuration file
sudo nano /var/ossec/etc/ossec.conf
```

**หาส่วน `<global>` และเพิ่มก่อนปิด tag `</global>`**:
```xml
<!-- MOPH Notify Integration for LINE OA หมอพร้อม -->
<integration>
    <n>custom-moph-notify</n>
    <level>7</level>
    <hook_url>https://morpromt2f.moph.go.th/api/notify/send</hook_url>
    <alert_format>json</alert_format>
    <options>max_log=1</options>
</integration>
```

### ขั้นตอนที่ 6: ตรวจสอบ Configuration
```bash
# ตรวจสอบ XML syntax
sudo xmllint --noout /var/ossec/etc/ossec.conf
echo "✅ XML syntax OK"

# ตรวจสอบ Python syntax
sudo /var/ossec/framework/python/bin/python3 -m py_compile /var/ossec/integrations/custom-moph-notify.py
echo "✅ Python syntax OK"
```

---

## 🧪 การทดสอบ

### ขั้นตอนที่ 7: ทดสอบ Script
```bash
# ทดสอบ help command
sudo /var/ossec/integrations/custom-moph-notify --help

# สร้างไฟล์ test alert
sudo cat > /tmp/test_alert_high.json << 'EOF'
{
    "timestamp": "2025-07-18T10:30:00.000+0000",
    "rule": {
        "level": 12,
        "description": "Multiple authentication failures from same source IP",
        "id": "5712"
    },
    "agent": {
        "name": "web-server-01"
    },
    "data": {
        "srcip": "192.168.1.100",
        "message": "Failed login attempt from user 'admin'"
    },
    "full_log": "Dec 18 10:30:00 web-server-01 sshd[1234]: Failed password for admin from 192.168.1.100 port 22 ssh2. This is the 5th consecutive failed attempt."
}
EOF

# ทดสอบการส่ง alert
sudo /var/ossec/integrations/custom-moph-notify /tmp/test_alert_high.json dummy https://morpromt2f.moph.go.th/api/notify/send
```

### ขั้นตอนที่ 8: ทดสอบ Wazuh Integration
```bash
# Restart Wazuh Manager
sudo /var/ossec/bin/wazuh-control restart

# ตรวจสอบการ start
sudo systemctl status wazuh-manager

# ตรวจสอบ integration loading
sudo grep -i "integration.*moph" /var/ossec/logs/ossec.log

# สร้าง test event
sudo logger -p auth.info "Failed password for testuser from 192.168.1.200 port 22 ssh2"
sudo logger -p auth.info "Failed password for testuser from 192.168.1.200 port 22 ssh2"
sudo logger -p auth.info "Failed password for testuser from 192.168.1.200 port 22 ssh2"

# ตรวจสอบ alert generation
sudo tail -f /var/ossec/logs/alerts/alerts.log | grep testuser
```

---

## 🏭 Production Deployment

### Environment Configuration

#### สำหรับ UAT Environment
```python
# ใน custom-moph-notify.py
MOPH_BASE_URL = "https://morpromt2f.moph.go.th"  # UAT URL
```

#### สำหรับ Production Environment
```python
# ใน custom-moph-notify.py
MOPH_BASE_URL = "https://production.moph.go.th"  # Production URL (ต้องสอบถาม URL จริง)
```

### Production ossec.conf Configuration
```xml
<!-- Production: เฉพาะ Alert สำคัญ -->
<integration>
    <n>custom-moph-notify</n>
    <level>10</level>
    <group>authentication_failed,rootcheck,web_attack,malware</group>
    <hook_url>https://production.moph.go.th/api/notify/send</hook_url>
    <alert_format>json</alert_format>
    <options>max_log=1</options>
</integration>
```

### Health Monitoring Setup
```bash
# สร้าง health check script
sudo nano /usr/local/bin/moph-notify-healthcheck.sh
```

**เพิ่มเนื้อหา**:
```bash
#!/bin/bash
LOG_FILE="/var/log/moph-notify-health.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# ตรวจสอบ Wazuh Manager
if ! systemctl is-active --quiet wazuh-manager; then
    echo "[$DATE] ERROR: Wazuh Manager is not running" >> $LOG_FILE
    exit 1
fi

# ตรวจสอบไฟล์ integration
if [ ! -f "/var/ossec/integrations/custom-moph-notify.py" ]; then
    echo "[$DATE] ERROR: MOPH Notify integration file not found" >> $LOG_FILE
    exit 1
fi

# ทดสอบ connectivity
if ! curl -s --max-time 10 https://morpromt2f.moph.go.th > /dev/null; then
    echo "[$DATE] WARNING: Cannot connect to MOPH Notify API" >> $LOG_FILE
fi

echo "[$DATE] INFO: Health check passed" >> $LOG_FILE
```

```bash
# ทำให้ executable
sudo chmod +x /usr/local/bin/moph-notify-healthcheck.sh

# ตั้งค่า cron job
echo "*/15 * * * * /usr/local/bin/moph-notify-healthcheck.sh" | sudo crontab -
```

### Log Rotation Setup
```bash
# สร้าง logrotate configuration
sudo nano /etc/logrotate.d/wazuh-moph-notify
```

**เพิ่มเนื้อหา**:
```
/var/ossec/logs/integrations.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
    create 640 root wazuh
    postrotate
        /bin/kill -HUP `cat /var/ossec/var/run/wazuh-manager.pid 2>/dev/null` 2>/dev/null || true
    endscript
}

/var/log/moph-notify-health.log {
    weekly
    rotate 12
    compress
    missingok
    notifempty
    create 644 root root
}
```

---

## 🔧 การแก้ไขปัญหา

### ปัญหาที่พบบ่อย

#### 1. Permission Denied
```bash
# Symptoms
# Error: Permission denied when executing script

# Solution
sudo chmod 750 /var/ossec/integrations/custom-moph-notify*
sudo chown root:wazuh /var/ossec/integrations/custom-moph-notify*
```

#### 2. Module Not Found
```bash
# Symptoms  
# ModuleNotFoundError: No module named 'requests'

# Solution
sudo /var/ossec/framework/python/bin/python3 -m pip install requests
```

#### 3. 401 Unauthorized
```bash
# Symptoms
# HTTP 401 error when sending to MOPH API

# Solution
# ตรวจสอบ CLIENT_KEY และ SECRET_KEY
grep -E "CLIENT_KEY|SECRET_KEY" /var/ossec/integrations/custom-moph-notify.py

# ตรวจสอบว่าไม่ใช่ค่า default
if grep -q "YOUR_CLIENT_KEY\|YOUR_SECRET_KEY" /var/ossec/integrations/custom-moph-notify.py; then
    echo "❌ API Keys ยังไม่ได้ตั้งค่า"
else
    echo "✅ API Keys ถูกตั้งค่าแล้ว"
fi
```

#### 4. Connection Timeout
```bash
# Symptoms
# Connection timeout when reaching MOPH API

# Solution
# ทดสอบ network connectivity
curl -I https://morpromt2f.moph.go.th/api/notify/send

# ตรวจสอบ firewall
sudo ufw status
sudo iptables -L OUTPUT | grep -E "443|https"

# ตรวจสอบ DNS resolution
nslookup morpromt2f.moph.go.th
```

#### 5. Wazuh Manager ไม่ Start
```bash
# Symptoms
# Wazuh Manager fails to start after configuration

# Solution
# ตรวจสอบ ossec.conf syntax
sudo xmllint --noout /var/ossec/etc/ossec.conf

# ตรวจสอบ error logs
sudo tail -n 50 /var/ossec/logs/ossec.log | grep -i error

# ถ้ามี syntax error ให้ restore backup
sudo cp /var/ossec/backup/[timestamp]/ossec.conf /var/ossec/etc/ossec.conf
sudo /var/ossec/bin/wazuh-control restart
```

### Debug Commands

#### ตรวจสอบ Configuration
```bash
# ดู integration configuration
sudo grep -A 10 -B 2 "custom-moph-notify" /var/ossec/etc/ossec.conf

# ตรวจสอบ file existence
ls -la /var/ossec/integrations/custom-moph-notify*

# ตรวจสอบ Python imports
sudo /var/ossec/framework/python/bin/python3 -c "
try:
    import sys, json, requests
    from datetime import datetime
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
"
```

#### ตรวจสอบ Log Files
```bash
# Integration logs
sudo tail -f /var/ossec/logs/integrations.log

# Manager logs
sudo tail -f /var/ossec/logs/ossec.log

# Alert logs
sudo tail -f /var/ossec/logs/alerts/alerts.log

# ค้นหา error specific
sudo grep -i "moph\|integration.*error" /var/ossec/logs/ossec.log | tail -20
```

#### Network Debugging
```bash
# ทดสอบ HTTPS connection
curl -v -X POST https://morpromt2f.moph.go.th/api/notify/send \
  -H "Content-Type: application/json" \
  -H "client-key: test" \
  -H "secret-key: test" \
  -d '{"messages":[{"type":"text","text":"test"}]}'

# ตรวจสอบ DNS resolution
dig morpromt2f.moph.go.th

# ตรวจสอบ routing
traceroute morpromt2f.moph.go.th
```

---

## 📊 Verification Checklist

หลังจากติดตั้งเสร็จแล้ว ให้ตรวจสอบรายการต่อไปนี้:

### ✅ File Installation
- [ ] `/var/ossec/integrations/custom-moph-notify` มีอยู่และ executable
- [ ] `/var/ossec/integrations/custom-moph-notify.py` มีอยู่และ readable
- [ ] File permissions เป็น 750 และ owner เป็น root:wazuh
- [ ] CLIENT_KEY และ SECRET_KEY ถูกตั้งค่าแล้ว

### ✅ Configuration
- [ ] ossec.conf มี integration section
- [ ] XML syntax ถูกต้อง (xmllint ผ่าน)
- [ ] Integration level ตั้งค่าเหมาะสม
- [ ] Hook URL ถูกต้อง

### ✅ Dependencies
- [ ] Python 3.6+ พร้อมใช้งาน
- [ ] requests module ติดตั้งแล้ว
- [ ] ไม่มี import errors

### ✅ Network Connectivity
- [ ] เชื่อมต่อ MOPH API ได้
- [ ] HTTPS port 443 เปิด
- [ ] DNS resolution ทำงานปกติ

### ✅ Wazuh Integration
- [ ] Wazuh Manager start สำเร็จ
- [ ] Integration โหลดใน ossec.log
- [ ] Test alert ส่งได้สำเร็จ
- [ ] LINE OA รับข้อความได้

### ✅ Monitoring Setup
- [ ] Health check script ติดตั้งแล้ว
- [ ] Cron job ตั้งค่าแล้ว
- [ ] Log rotation ตั้งค่าแล้ว

---

## 🔄 Upgrade Process

### อัปเกรดจาก Version 1.0 ไป 2.0
```bash
# 1. Backup current version
sudo cp /var/ossec/integrations/custom-moph-notify.py /var/ossec/integrations/custom-moph-notify.py.v1.backup

# 2. ดาวน์โหลด version ใหม่
cd /tmp
git clone https://github.com/yourusername/wazuh-moph-notify.git
cd wazuh-moph-notify

# 3. คัดลอกไฟล์ใหม่
sudo cp scripts/custom-moph-notify.py /var/ossec/integrations/

# 4. คัดลอก configuration จากไฟล์เก่า
OLD_CLIENT_KEY=$(sudo grep "CLIENT_KEY.*=" /var/ossec/integrations/custom-moph-notify.py.v1.backup | cut -d'"' -f2)
OLD_SECRET_KEY=$(sudo grep "SECRET_KEY.*=" /var/ossec/integrations/custom-moph-notify.py.v1.backup | cut -d'"' -f2)

# 5. อัปเดต keys ในไฟล์ใหม่
sudo sed -i "s/YOUR_CLIENT_KEY/$OLD_CLIENT_KEY/" /var/ossec/integrations/custom-moph-notify.py
sudo sed -i "s/YOUR_SECRET_KEY/$OLD_SECRET_KEY/" /var/ossec/integrations/custom-moph-notify.py

# 6. ทดสอบและ restart
sudo /var/ossec/framework/python/bin/python3 -m py_compile /var/ossec/integrations/custom-moph-notify.py
sudo /var/ossec/bin/wazuh-control restart
```

---

## 📞 การได้รับความช่วยเหลือ

หากพบปัญหาในการติดตั้ง:

1. **ตรวจสอบ Log Files ก่อน**:
   ```bash
   sudo tail -n 100 /var/ossec/logs/ossec.log | grep -i error
   ```

2. **ใช้ Debug Mode**:
   ```bash
   sudo bash -x /var/ossec/integrations/custom-moph-notify /tmp/test_alert.json dummy https://morpromt2f.moph.go.th/api/notify/send
   ```

3. **ตรวจสอบ Network**:
   ```bash
   curl -I https://morpromt2f.moph.go.th/api/notify/send
   ```

4. **ส่ง Issue ใน GitHub**:
   - รวม log excerpts
   - รวม configuration (ปิด sensitive data)
   - รวม system information

5. **ติดต่อทีมสนับสนุน**:
   - Email: support@yourorganization.com
   - GitHub Issues: https://github.com/yourusername/wazuh-moph-notify/issues

---

## 🎯 Next Steps

หลังจากติดตั้งเสร็จแล้ว:

1. 📖 อ่าน [Configuration Guide](configuration-guide.md) สำหรับการตั้งค่าขั้นสูง
2. 🔒 อ่าน [Security Guide](security.md) สำหรับ best practices
3. 🎨 ดู [Flex Message Examples](flex-message-examples.md) สำหรับ customization
4. 🔧 ตั้งค่า monitoring และ alerting ตาม environment ของคุณ
5. 📊 วิเคราะห์ performance และปรับแต่งตามต้องการ

---

<div align="center">

**🎉 ขอแสดงความยินดี! การติดตั้งเสร็จสมบูรณ์แล้ว 🎉**

ระบบ Wazuh ของคุณพร้อมส่ง Security Alerts ไปยัง LINE OA หมอพร้อมแล้ว!

</div>
# 🔧 คู่มือการแก้ไขปัญหา - Wazuh MOPH Notify Integration


## 🚀 ปัญหาการติดตั้ง

### ❌ **Wazuh Manager ไม่พบ**

**อาการ**: `❌ Wazuh not found at /var/ossec`

**สาเหตุ**: Wazuh ไม่ได้ติดตั้งหรือติดตั้งใน path อื่น

**วิธีแก้**:
```bash
# ตรวจสอบ Wazuh installation
which wazuh-control
find / -name "wazuh-control" 2>/dev/null

# ถ้าติดตั้งใน path อื่น ให้แก้ไข path ในสคริปต์
# หรือสร้าง symlink
sudo ln -s /path/to/actual/wazuh /var/ossec
```

### ❌ **File Permission Denied**

**อาการ**: `Permission denied` เมื่อรันสคริปต์

**สาเหตุ**: File permissions ไม่ถูกต้อง

**วิธีแก้**:
```bash
# ตรวจสอบ permissions ปัจจุบัน
ls -la /var/ossec/integrations/custom-moph-notify*

# แก้ไข permissions
sudo chmod 750 /var/ossec/integrations/custom-moph-notify
sudo chmod 750 /var/ossec/integrations/custom-moph-notify.py
sudo chown root:wazuh /var/ossec/integrations/custom-moph-notify*

# ตรวจสอบผลลัพธ์
ls -la /var/ossec/integrations/custom-moph-notify*
# ควรได้: -rwxr-x--- 1 root wazuh
```

### ❌ **Wazuh Manager ไม่ Start หลัง Configuration**

**อาการ**: Wazuh Manager fail to start หลังเพิ่ม integration

**สาเหตุ**: XML syntax error ใน ossec.conf

**วิธีแก้**:
```bash
# ตรวจสอบ XML syntax
sudo xmllint --noout /var/ossec/etc/ossec.conf

# ถ้ามี error ให้แก้ไข หรือ restore backup
sudo cp /var/ossec/backup/[timestamp]/ossec.conf /var/ossec/etc/ossec.conf

# ลองแก้ไข error และทดสอบอีกครั้ง
sudo /var/ossec/bin/wazuh-control configcheck  # (ถ้ามี command นี้)
sudo /var/ossec/bin/wazuh-control restart
```

---

## ⚙️ ปัญหาการกำหนดค่า

### ❌ **CLIENT_KEY และ SECRET_KEY ยังไม่ได้ตั้งค่า**

**อาการ**: `❌ Error: CLIENT_KEY and SECRET_KEY must be configured`

**วิธีแก้**:
```bash
# แก้ไขไฟล์ Python script
sudo nano /var/ossec/integrations/custom-moph-notify.py

# ค้นหาและแก้ไขบรรทัดเหล่านี้:
CLIENT_KEY = "YOUR_CLIENT_KEY"  # แทนที่ด้วยค่าจริง
SECRET_KEY = "YOUR_SECRET_KEY"  # แทนที่ด้วยค่าจริง

# ตรวจสอบว่าแก้ไขแล้ว
grep -E "CLIENT_KEY|SECRET_KEY" /var/ossec/integrations/custom-moph-notify.py
```

### ❌ **Integration ไม่ปรากฏใน Log**

**อาการ**: ไม่เห็น integration loading ใน ossec.log

**วิธีแก้**:
```bash
# ตรวจสอบ ossec.conf ว่ามี integration section หรือไม่
grep -A 5 -B 5 "custom-moph-notify" /var/ossec/etc/ossec.conf

# ตรวจสอบว่าอยู่ใน <global> section หรือไม่
sed -n '/<global>/,/<\/global>/p' /var/ossec/etc/ossec.conf | grep -A 5 -B 5 integration

# ถ้าไม่มี ให้เพิ่ม:
sudo nano /var/ossec/etc/ossec.conf
# เพิ่ม integration config ใน <global> section
```

### ❌ **Alert Level ไม่ตรงกับที่ตั้งค่า**

**อาการ**: Alert ที่ส่งไม่ตรงกับ level ที่กำหนด

**วิธีแก้**:
```bash
# ตรวจสอบ configuration
grep -A 5 "custom-moph-notify" /var/ossec/etc/ossec.conf

# ตรวจสอบ alert level ที่มาจริง
sudo tail -f /var/ossec/logs/alerts/alerts.log | grep level

# ปรับ level ใน ossec.conf ตามต้องการ
<level>7</level>  # แสดง alert level 7 ขึ้นไป
```

---

## 🌐 ปัญหาเครือข่าย

### ❌ **Connection Timeout**

**อาการ**: `❌ Timeout error: Request to MOPH Notify timed out after 30 seconds`

**วิธีแก้**:
```bash
# ทดสอบ connectivity
curl -I https://morpromt2f.moph.go.th/api/notify/send

# ตรวจสอบ DNS resolution
nslookup morpromt2f.moph.go.th
dig morpromt2f.moph.go.th

# ตรวจสอบ firewall
sudo ufw status
sudo iptables -L OUTPUT | grep -E "443|https"

# ทดสอบ routing
traceroute morpromt2f.moph.go.th
```

### ❌ **Unable to Connect to MOPH Notify API**

**อาการ**: `❌ Connection error: Unable to connect to MOPH Notify API`

**วิธีแก้**:
```bash
# ตรวจสอบ proxy settings (ถ้ามี)
echo $http_proxy
echo $https_proxy

# ทดสอบ connection
telnet morpromt2f.moph.go.th 443

# ตรวจสอบ network interface
ip route show
ping 8.8.8.8  # ทดสอบ internet connectivity
```

### ❌ **401 Unauthorized**

**อาการ**: `❌ Failed to send alert to MOPH Notify. Status code: 401`

**สาเหตุ**: API keys ไม่ถูกต้องหรือหมดอายุ

**วิธีแก้**:
```bash
# ตรวจสอบ API keys
grep -E "CLIENT_KEY|SECRET_KEY" /var/ossec/integrations/custom-moph-notify.py

# ตรวจสอบว่าไม่ใช่ค่า default
if grep -q "YOUR_CLIENT_KEY\|YOUR_SECRET_KEY" /var/ossec/integrations/custom-moph-notify.py; then
    echo "❌ API Keys ยังไม่ได้ตั้งค่า"
else
    echo "✅ API Keys ถูกตั้งค่าแล้ว"
fi

# ทดสอบ API keys ด้วย curl
curl -X POST https://morpromt2f.moph.go.th/api/notify/send \
  -H "Content-Type: application/json" \
  -H "client-key: YOUR_ACTUAL_CLIENT_KEY" \
  -H "secret-key: YOUR_ACTUAL_SECRET_KEY" \
  -d '{"messages":[{"type":"text","text":"test"}]}'
```

---

## 🔐 ปัญหา Permission

### ❌ **Script ไม่สามารถเขียน Log ได้**

**อาการ**: Permission denied เมื่อเขียน log files

**วิธีแก้**:
```bash
# ตรวจสอบ log directory permissions
ls -la /var/ossec/logs/
ls -la /var/log/

# แก้ไข permissions
sudo chown -R wazuh:wazuh /var/ossec/logs/
sudo chmod 755 /var/ossec/logs/

# สร้าง log file สำหรับ integration
sudo touch /var/ossec/logs/integrations.log
sudo chown wazuh:wazuh /var/ossec/logs/integrations.log
sudo chmod 644 /var/ossec/logs/integrations.log
```

### ❌ **SELinux หรือ AppArmor Block**

**อาการ**: Script ไม่ทำงานเนื่องจาก security policies

**วิธีแก้**:
```bash
# ตรวจสอบ SELinux status
sestatus
getenforce

# ถ้า SELinux enabled ให้ดู audit log
sudo tail -f /var/log/audit/audit.log | grep denied

# Temporary disable (สำหรับ testing)
sudo setenforce 0

# หรือสร้าง policy สำหรับ Wazuh
# ขอคำปรึกษาจาก SELinux admin

# สำหรับ AppArmor
sudo aa-status
sudo tail -f /var/log/syslog | grep apparmor
```

---

## 🐍 ปัญหา Python และ Dependencies

### ❌ **ModuleNotFoundError: No module named 'requests'**

**อาการ**: Python ไม่พบ requests module

**วิธีแก้**:
```bash
# ติดตั้ง requests module
sudo /var/ossec/framework/python/bin/python3 -m pip install requests

# ตรวจสอบการติดตั้ง
sudo /var/ossec/framework/python/bin/python3 -c "import requests; print('✅ requests OK')"

# ตรวจสอบ pip version
sudo /var/ossec/framework/python/bin/python3 -m pip --version

# ถ้า pip ไม่มี ให้ติดตั้ง
curl https://bootstrap.pypa.io/get-pip.py | sudo /var/ossec/framework/python/bin/python3
```

### ❌ **Python Syntax Error**

**อาการ**: SyntaxError เมื่อรัน Python script

**วิธีแก้**:
```bash
# ตรวจสอบ Python syntax
sudo /var/ossec/framework/python/bin/python3 -m py_compile /var/ossec/integrations/custom-moph-notify.py

# ตรวจสอบ Python version compatibility
sudo /var/ossec/framework/python/bin/python3 --version

# ถ้า version เก่าเกินไป (< 3.6) ให้อัปเกรด Python หรือแก้ไข syntax
```

### ❌ **Unicode/Encoding Issues**

**อาการ**: UnicodeDecodeError เมื่อประมวลผล Thai text

**วิธีแก้**:
```bash
# ตรวจสอบ locale settings
locale
echo $LANG

# ตั้งค่า locale สำหรับ Thai
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# หรือแก้ไขใน script โดยเพิ่ม encoding parameter
# ในส่วนการอ่านไฟล์:
# with open(file_path, 'r', encoding='utf-8') as f:
```

---

## 📱 ปัญหาการส่งข้อความ

### ❌ **Flex Message ไม่แสดงใน LINE**

**อาการ**: ข้อความส่งสำเร็จแต่ไม่เห็นใน LINE

**วิธีแก้**:
```bash
# ตรวจสอบ response จาก API
# ดูใน debug output ของ script

# ตรวจสอบ Flex Message format
# อาจมี syntax error ใน JSON structure

# ทดสอบส่งข้อความธรรมดาก่อน
# แก้ไข script ให้ส่ง text message แทน Flex Message ชั่วคราว
```

### ❌ **ข้อความซ้ำกัน**

**อาการ**: ได้รับข้อความซ้ำหลายครั้ง

**วิธีแก้**:
```bash
# ตรวจสอบว่ามี integration ซ้ำใน ossec.conf หรือไม่
grep -n "custom-moph-notify" /var/ossec/etc/ossec.conf

# เพิ่ม max_log=1 ใน integration config
<options>max_log=1</options>

# ตรวจสอบว่า Wazuh ไม่ส่ง alert ซ้ำ
sudo grep "duplicate" /var/ossec/logs/ossec.log
```

### ❌ **ข้อความตัดไม่เหมาะสม**

**อาการ**: ข้อความถูกตัดกลางคำหรือไม่มีข้อมูลสำคัญ

**วิธีแก้**:
```bash
# ปรับค่า max_length ในฟังก์ชัน get_max_length_by_priority()
# แก้ไขในไฟล์ custom-moph-notify.py:

def get_max_length_by_priority(priority):
    length_map = {
        "CRITICAL": 500,    # เพิ่มจาก 400
        "HIGH": 400,        # เพิ่มจาก 300
        "MEDIUM": 300,      # เพิ่มจาก 200
        "LOW": 200,         # เพิ่มจาก 150
        "INFO": 150         # เพิ่มจาก 100
    }
    return length_map.get(priority, 200)
```

---

## 🔍 การ Debug และ Monitoring

### การเปิด Debug Mode

```bash
# รัน script ด้วย debug mode
sudo bash -x /var/ossec/integrations/custom-moph-notify /tmp/test_alert.json dummy https://morpromt2f.moph.go.th/api/notify/send

# หรือเพิ่ม debug output ใน Python script
# เพิ่มบรรทัดนี้ในส่วนต้นของ main():
import logging
logging.basicConfig(level=logging.DEBUG)
```

### ตรวจสอบ Log Files

```bash
# Integration logs
sudo tail -f /var/ossec/logs/integrations.log

# Manager logs
sudo tail -f /var/ossec/logs/ossec.log

# Alert logs
sudo tail -f /var/ossec/logs/alerts/alerts.log

# System logs
sudo tail -f /var/log/syslog | grep wazuh

# ค้นหา error เฉพาะ
sudo grep -i "error\|fail\|timeout" /var/ossec/logs/ossec.log | tail -20
```

### การทดสอบแบบ Manual

```bash
# สร้าง test alert file
cat > /tmp/debug_alert.json << 'EOF'
{
    "timestamp": "2025-07-18T10:30:00.000+0000",
    "rule": {
        "level": 8,
        "description": "Debug test alert",
        "id": "99999"
    },
    "agent": {
        "name": "debug-agent"
    },
    "data": {
        "srcip": "127.0.0.1"
    }
}
EOF

# ทดสอบการรัน script
sudo /var/ossec/integrations/custom-moph-notify /tmp/debug_alert.json dummy https://morpromt2f.moph.go.th/api/notify/send

# ทดสอบด้วย curl โดยตรง
curl -v -X POST https://morpromt2f.moph.go.th/api/notify/send \
  -H "Content-Type: application/json" \
  -H "client-key: YOUR_CLIENT_KEY" \
  -H "secret-key: YOUR_SECRET_KEY" \
  -d @- << 'EOF'
{
  "messages": [
    {
      "type": "text",
      "text": "Test message from curl"
    }
  ]
}
EOF
```

---

## ❓ FAQ

### Q: สามารถใช้กับ Wazuh version เก่าได้หรือไม่?

**A**: Script ถูกออกแบบสำหรับ Wazuh 4.0+ แต่สามารถปรับใช้กับเวอร์ชันเก่าได้โดย:
- ตรวจสอบ path ของ Python interpreter
- ปรับ integration configuration format
- อาจต้องแก้ไข alert JSON structure

### Q: สามารถส่งไปหลาย LINE Groups ได้หรือไม่?

**A**: ได้ โดยสร้าง integration หลายตัวใน ossec.conf:
```xml
<integration>
    <n>custom-moph-notify</n>
    <level>12</level>
    <hook_url>https://morpromt2f.moph.go.th/api/notify/send?group=critical</hook_url>
    <alert_format>json</alert_format>
</integration>

<integration>
    <n>custom-moph-notify</n>
    <level>7</level>
    <hook_url>https://morpromt2f.moph.go.th/api/notify/send?group=normal</hook_url>
    <alert_format>json</alert_format>
</integration>
```

### Q: การใช้ memory และ CPU เป็นอย่างไร?

**A**: Script ใช้ทรัพยากรน้อย:
- Memory: ~10-20MB ต่อการรัน
- CPU: minimal (รันแค่ตอนมี alert)
- Network: ~1-5KB ต่อข้อความ

### Q: มี rate limiting หรือไม่?

**A**: MOPH Notify API อาจมี rate limiting ตรวจสอบได้จาก:
- HTTP response headers
- Error messages ที่ได้รับ
- ปรับ `max_log=1` ใน configuration

### Q: สามารถ customize Flex Message ได้หรือไม่?

**A**: ได้ โดยแก้ไขฟังก์ชัน `create_flex_message()` ใน script:
- เปลี่ยนสี, emoji, layout
- เพิ่มปุ่ม action buttons
- ปรับ content ตาม requirements

### Q: ถ้า MOPH API เปลี่ยน URL ต้องทำอย่างไร?

**A**: แก้ไขใน script:
```python
MOPH_BASE_URL = "https://new-api-url.moph.go.th"
```
และอัปเดต hook_url ใน ossec.conf

---

## 🆘 ขอความช่วยเหลือ

หากยังแก้ไขปัญหาไม่ได้:

1. **รวบรวมข้อมูล Debug**:
   ```bash
   # รัน health check
   sudo bash tools/healthcheck.sh > debug_info.txt 2>&1
   
   # รวบรวม logs
   sudo tar czf debug_logs.tar.gz /var/ossec/logs/ossec.log /var/ossec/logs/integrations.log /var/log/syslog
   ```

2. **สร้าง GitHub Issue**:
   - แนบไฟล์ debug_info.txt
   - แนบ log excerpts (ปิด sensitive data)
   - ระบุ OS version, Wazuh version
   - อธิบายขั้นตอนที่ทำมา

3. **ติดต่อทีมสนับสนุน**:
   - Email: sak.janenii@gmail.com
   - GitHub: https://github.com/sakmobile/Wazuh-MOPH-Notify-Integration/issues

---

<div align="center">

**💡 หากคู่มือนี้ช่วยแก้ปัญหาของคุณได้ กรุณา Star repository ด้วยนะครับ! ⭐**

**🤝 พบปัญหาใหม่? มาช่วยกันปรับปรุงคู่มือนี้!**

</div>
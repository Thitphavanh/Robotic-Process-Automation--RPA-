# 🔑 วิธีการตั้งค่า Anthropic API Key

## ⚠️ ปัญหา: API Key ไม่ถูกต้อง

หากคุณเจอ error นี้:
```
Error code: 401 - authentication_error: invalid x-api-key
```

แสดงว่า API Key ที่คุณใช้ไม่ถูกต้อง หรือหมดอายุ

---

## 📋 ขั้นตอนการแก้ไข

### 1. สร้าง API Key ใหม่

1. ไปที่: https://console.anthropic.com/
2. ลงชื่อเข้าใช้ (หรือสมัครใหม่)
3. ไปที่ **Settings** > **API Keys**
4. คลิก **Create Key**
5. ตั้งชื่อ API Key (เช่น "Stock Bot")
6. **คัดลอก API Key ทันที** (จะไม่สามารถดูอีกครั้งได้)

### 2. ตรวจสอบ API Key

API Key ที่ถูกต้องจะมีรูปแบบ:
```
sk-ant-api03-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**ความยาว:** ประมาณ 100+ ตัวอักษร

---

## 🛠️ วิธีตั้งค่า API Key (3 วิธี)

### วิธีที่ 1: Environment Variable (แนะนำ) ⭐

```bash
# macOS/Linux
export ANTHROPIC_API_KEY='sk-ant-api03-your-actual-key-here'

# ตรวจสอบ
echo $ANTHROPIC_API_KEY

# รันโปรแกรม
python stock_bot_macos_agent.py
```

**ข้อดี:** ปลอดภัย, ไม่ต้องแก้ไขโค้ด

### วิธีที่ 2: แก้ไขในไฟล์ Python

เปิดไฟล์ `stock_bot_macos_agent.py` และแก้ไขบรรทัดที่ 23:

```python
# เปลี่ยนจาก
ANTHROPIC_API_KEY = "sk-ant-api03-AzH72bYctbptTXYOjU8h0n_..."

# เป็น API Key ของคุณ
ANTHROPIC_API_KEY = "sk-ant-api03-YOUR-NEW-KEY-HERE"
```

**ข้อเสีย:** API Key อยู่ในโค้ด (ไม่ปลอดภัย)

### วิธีที่ 3: ใช้ไฟล์ .env

1. สร้างไฟล์ `.env`:
```bash
echo 'ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here' > .env
```

2. ติดตั้ง python-dotenv:
```bash
pip install python-dotenv
```

3. แก้ไขโค้ดเพิ่ม:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🔍 ตรวจสอบว่า API Key ใช้งานได้

รันคำสั่งนี้เพื่อทดสอบ:

```bash
python -c "
import anthropic
import os

api_key = os.environ.get('ANTHROPIC_API_KEY', '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')

try:
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model='claude-3-5-sonnet-20241022',
        max_tokens=10,
        messages=[{'role': 'user', 'content': 'hi'}]
    )
    print('✅ API Key ใช้งานได้!')
except anthropic.AuthenticationError:
    print('❌ API Key ไม่ถูกต้อง!')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

---

## 💰 ค่าใช้จ่าย

- **Free Tier:** $5 credit เมื่อสมัครใหม่
- **Claude Sonnet 4.5 (Latest):**
  - Input: $3 per million tokens
  - Output: $15 per million tokens
- การใช้งาน Stock Bot: ประมาณ $0.10-0.50 ต่อครั้ง

## 🆕 Model Update

โปรแกรมได้อัปเดตเป็น **Claude Sonnet 4.5 (claude-sonnet-4-20250514)** แล้ว
- Model เก่า: `claude-3-5-sonnet-20241022` (หมดอายุ October 22, 2025)
- Model ปัจจุบัน: `claude-sonnet-4-20250514` (Latest, Most Capable)

**ข้อดีของ Claude Sonnet 4.5:**
- ✅ ความสามารถด้าน Vision ดีกว่า
- ✅ ความแม่นยำในการวิเคราะห์สูงกว่า
- ✅ เข้าใจบริบทภาษาไทยดีขึ้น
- ✅ ประมวลผลภาพซับซ้อนได้ดีกว่า

---

## 🔒 ความปลอดภัย

1. **อย่า commit API Key** ลง Git
2. **อย่าแชร์ API Key** ให้คนอื่น
3. **ใช้ environment variable** แทนการเก็บในโค้ด
4. **Rotate API Key** เป็นประจำ
5. เพิ่ม `.env` ใน `.gitignore`:
   ```bash
   echo '.env' >> .gitignore
   ```

---

## 🆘 ยังไม่ได้?

### ลองเวอร์ชันที่ไม่ต้องใช้ API:

รันโปรแกรมเวอร์ชันพื้นฐานแทน:
```bash
python stock_bot_direct_visit_macos.py
```

เวอร์ชันนี้จะ:
- เข้าชมเว็บไซต์
- ถ่ายภาพหน้าจอ
- แต่ไม่มี AI analysis

---

## 📞 ติดต่อสอบถาม

- Anthropic Support: https://support.anthropic.com/
- Discord Community: https://discord.gg/anthropic

---

## 📝 สรุป

1. ✅ สร้าง API Key ใหม่จาก console.anthropic.com
2. ✅ คัดลอก API Key ทันที
3. ✅ ตั้งค่าผ่าน environment variable
4. ✅ ทดสอบด้วยคำสั่ง python ข้างบน
5. ✅ รันโปรแกรม

**API Key ที่ใช้อยู่ในโค้ดตอนนี้ไม่ใช่ของคุณ หรือหมดอายุแล้ว!**

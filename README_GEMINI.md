# 🌟 Stock Bot with Google Gemini AI

## 🎉 ใหม่! เวอร์ชัน Google Gemini - ฟรี 100%!

---

## 🚀 ทำไมต้อง Gemini?

### ✅ **ฟรี 100%!**
- ไม่มีค่าใช้จ่าย (ภายใน free tier)
- Gemini 2.0 Flash ฟรีตลอดการใช้งาน
- ไม่ต้องใส่บัตรเครดิต

### ✅ **ความสามารถเทียบเท่า Claude**
- Vision API ที่ทรงพลัง
- รองรับภาษาไทยได้ดีมาก
- วิเคราะห์ภาพได้แม่นยำ

### ✅ **ใช้งานง่าย**
- API Key ฟรี จาก Google
- ไม่ต้องกรอกข้อมูลบัตร
- Setup ง่าย 3 ขั้นตอน

---

## 📋 การเปรียบเทียบ

| Feature | Claude Sonnet | Gemini 2.0 Flash |
|---------|--------------|------------------|
| **ค่าใช้จ่าย** | $0.10-0.50/run | ฟรี! |
| **Vision Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Thai Support** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | เร็ว | เร็วมาก |
| **Rate Limit** | Varies | 15 req/min |
| **Setup** | ยาก (ต้องบัตร) | ง่าย (ไม่ต้องบัตร) |
| **Free Tier** | $5 credit | ฟรีตลอด |

---

## 🔑 ขั้นตอนที่ 1: รับ API Key (ฟรี!)

### 1. ไปที่ Google AI Studio
```
https://makersuite.google.com/app/apikey
```

### 2. คลิก "Get API Key" หรือ "Create API Key"

### 3. เลือก Project
- ถ้ายังไม่มี Project จะสร้างให้อัตโนมัติ
- หรือเลือก "Create API key in new project"

### 4. คัดลอก API Key
- รูปแบบ: `AIzaSy...` (ประมาณ 39 ตัวอักษร)
- **คัดลอกทันที!** เก็บไว้ที่ปลอดภัย

### 5. ไม่ต้องใส่บัตรเครดิต!
- Gemini 2.0 Flash ฟรีตลอด
- ไม่มีค่าใช้จ่ายแอบแฝง

---

## ⚙️ ขั้นตอนที่ 2: ติดตั้ง

### ติดตั้ง Dependencies:

```bash
# ติดตั้ง Google Generative AI SDK
pip install google-generativeai

# ติดตั้ง dependencies อื่นๆ
pip install pyautogui pillow python-dotenv
```

---

## 🔧 ขั้นตอนที่ 3: ตั้งค่า API Key

### วิธีที่ 1: ใช้ Environment Variable (แนะนำ)

```bash
# macOS/Linux
export GEMINI_API_KEY='AIzaSy-your-actual-key-here'

# ตรวจสอบ
echo $GEMINI_API_KEY

# เพื่อให้ใช้ได้ตลอด เพิ่มใน ~/.zshrc
echo "export GEMINI_API_KEY='AIzaSy-your-key'" >> ~/.zshrc
source ~/.zshrc
```

### วิธีที่ 2: ใส่ตอนรันโปรแกรม

```bash
# รันโปรแกรม - จะถามเอง
python stock_bot_macos_gemini.py

# จะมี prompt ให้ใส่:
🔑 API Key: [ใส่ API key ตรงนี้]
```

---

## 🚀 วิธีใช้งาน

### 1. ทดสอบ API ก่อน (แนะนำ):

```bash
python test_gemini_api.py
```

**ผลลัพธ์ที่คาดหวัง:**
```
✅ ทดสอบสำเร็จ! API Key ใช้งานได้
🤖 คำตอบจาก Gemini: [response]
✅ Vision API ทำงานได้
```

### 2. รัน Stock Bot:

```bash
python stock_bot_macos_gemini.py
```

### 3. เลือกโหมด:

```
📋 เลือกโหมดการทำงาน:
   1. ค้นหาข้อมูลทั่วไป (Dynamic Search)
   2. ค้นหาข้อมูลหุ้นไทย (Stock Focus)
   3. กำหนดเอง (Custom Query)

🔢 เลือกโหมด (1-3): 2
🌐 จำนวนเว็บไซต์ (1-10): 3
```

---

## 📊 Output Files

หลังรันเสร็จจะได้ไฟล์:

```
gemini_search_results.png          # ภาพหน้าค้นหา
gemini_website_01_main.png         # ภาพเว็บที่ 1
gemini_website_01_scrolled.png     # ภาพเว็บที่ 1 (หลัง scroll)
gemini_website_02_main.png         # ภาพเว็บที่ 2
...
gemini_analysis_report.txt         # รายงานสรุป Gemini AI
```

---

## 💰 ข้อมูลค่าใช้จ่าย

### Gemini 2.0 Flash (ฟรี!)

**Free Tier:**
- ✅ **ฟรี!** ไม่มีค่าใช้จ่าย
- ✅ 15 requests per minute
- ✅ 1,500 requests per day
- ✅ Vision API included
- ✅ ไม่ต้องใส่บัตรเครดิต

**Paid Tier (ถ้าต้องการ):**
- Input: $0.075 per million tokens
- Output: $0.30 per million tokens
- **ถูกกว่า Claude มาก!**

---

## 🆚 Gemini vs Claude

### Gemini 2.0 Flash ดีกว่าตรงไหน?

#### ✅ ข้อดี:
1. **ฟรี 100%!** (ใน free tier)
2. **Setup ง่ายกว่า** - ไม่ต้องใส่บัตรเครดิต
3. **ถูกกว่า** - ถ้าเกิน free tier
4. **Vision quality ดีมาก** - เทียบเท่า Claude
5. **รองรับไทย** - ดีมาก แม้จะน้อยกว่า Claude นิดหน่อย
6. **Rate limit สูง** - 15 req/min ฟรี
7. **Google ecosystem** - เชื่อมกับ Google services

#### ⚠️ ข้อจำกัด:
1. **Thai understanding** - น้อยกว่า Claude Sonnet 4.5 นิดหน่อย
2. **Rate limit** - 15 req/min (Claude ไม่มีใน paid tier)
3. **Context window** - เล็กกว่า Claude เล็กน้อย

---

## 🎯 Use Cases

### เหมาะสำหรับ:
- ✅ ผู้ใช้ทั่วไป ที่ต้องการฟรี
- ✅ Testing และ Development
- ✅ งานประจำวัน (ไม่เกิน 15 req/min)
- ✅ Small to Medium projects
- ✅ การเรียนรู้ RPA และ AI

### ไม่เหมาะสำหรับ:
- ❌ งานที่ต้องการ Thai native-level
- ❌ งานที่ต้อง > 15 requests/minute
- ❌ งานที่ต้องการ context window ใหญ่มาก
- ❌ Enterprise-level applications

---

## 🔧 Troubleshooting

### ปัญหา: "API Key ไม่ถูกต้อง"
```bash
# ตรวจสอบว่า API Key ขึ้นต้นด้วย AIzaSy
echo $GEMINI_API_KEY

# สร้าง API Key ใหม่
# https://makersuite.google.com/app/apikey
```

### ปัญหา: "No module named 'google.generativeai'"
```bash
pip install google-generativeai
```

### ปัญหา: "Rate limit exceeded"
```
⏰ รอ 1 นาที แล้วลองใหม่
💡 Free tier: 15 requests/minute
```

### ปัญหา: "Safety filters blocked"
```
⚠️  Gemini มี safety filters เข้มงวด
💡 ลองเปลี่ยนคำถาม หรือ prompt
```

---

## 📚 ตัวอย่างการใช้งาน

### ตัวอย่างที่ 1: เช็คหุ้นไทยประจำวัน (ฟรี!)

```bash
python stock_bot_macos_gemini.py

# เลือก:
🔢 เลือกโหมด (1-3): 2
🌐 จำนวนเว็บไซต์: 3
```

**ค่าใช้จ่าย:** $0 (ฟรี!)

### ตัวอย่างที่ 2: วิจัยบริษัท

```bash
python stock_bot_macos_gemini.py

# เลือก:
🔢 เลือกโหมด (1-3): 1
🔍 ใส่คำค้นหา: PTT stock analysis
🌐 จำนวนเว็บไซต์: 5
```

**ค่าใช้จ่าย:** $0 (ฟรี!)

### ตัวอย่างที่ 3: การวิเคราะห์ขั้นสูง

```bash
python stock_bot_macos_gemini.py

# เลือก:
🔢 เลือกโหมด (1-3): 3
🔍 ใส่คำค้นหา: Thailand stock market 2025
📝 ใส่คำสั่งวิเคราะห์: วิเคราะห์แนวโน้มตลาด พร้อมแนะนำหุ้นน่าสนใจ
🌐 จำนวนเว็บไซต์: 5
```

**ค่าใช้จ่าย:** $0 (ฟรี!)

---

## 🎓 เปรียบเทียบกับเวอร์ชันอื่น

### 1. stock_bot_macos_gemini.py (ใหม่!)
- 💰 **ฟรี!**
- 🤖 Google Gemini 2.0 Flash
- ✅ Vision + Text Analysis
- ✅ Thai support (ดีมาก)
- ⭐ **แนะนำสำหรับทุกคน!**

### 2. stock_bot_macos_agent.py (Claude)
- 💰 $0.10-0.50 per run
- 🤖 Claude Sonnet 4.5
- ✅ Vision + Text Analysis
- ✅ Thai support (ดีที่สุด)
- ⭐ แนะนำสำหรับงานที่ต้องการ native Thai

### 3. stock_bot_macos_no_api.py (OCR)
- 💰 ฟรี!
- 🤖 Tesseract OCR
- ⚠️ Text extraction only
- ⚠️ ไม่มี AI analysis
- ⭐ แนะนำถ้าไม่มี internet

---

## 🚀 Quick Start (3 ขั้นตอน)

### ขั้นตอนที่ 1: รับ API Key (2 นาที)
```
1. ไปที่ https://makersuite.google.com/app/apikey
2. คลิก "Get API Key"
3. คัดลอก API Key (AIzaSy...)
```

### ขั้นตอนที่ 2: ติดตั้ง (1 นาที)
```bash
pip install google-generativeai pyautogui pillow python-dotenv
```

### ขั้นตอนที่ 3: รัน! (ทันที)
```bash
export GEMINI_API_KEY='AIzaSy-your-key'
python test_gemini_api.py
python stock_bot_macos_gemini.py
```

**ใช้เวลาทั้งหมด: 3 นาที**
**ค่าใช้จ่าย: $0 (ฟรี!)**

---

## 💡 Pro Tips

### 1. Rate Limit Management
```python
# Free tier: 15 requests/minute
# ถ้าใช้เยอะ ให้เว้นระยะ:
num_websites = 3  # แทนที่จะใช้ 10
```

### 2. Prompt Engineering
```python
# Gemini เข้าใจภาษาไทยดี
analysis_prompt = "วิเคราะห์ราคาหุ้น แนวโน้ม และแนะนำ"
```

### 3. Error Handling
```python
# Gemini มี safety filters
# ถ้า response blocked ลอง rephrasing
```

### 4. Cost Optimization
```
✅ ฟรีตลอด (ใน free tier)
✅ ไม่ต้องกังวลเรื่องค่าใช้จ่าย
✅ 15 req/min เพียงพอสำหรับงานทั่วไป
```

---

## 📞 Support & Resources

### Official Resources:
- **API Keys:** https://makersuite.google.com/app/apikey
- **Documentation:** https://ai.google.dev/docs
- **Pricing:** https://ai.google.dev/pricing
- **Community:** https://discuss.ai.google.dev/

### Limits & Quotas:
- **Free tier:** 15 RPM (requests per minute)
- **Free tier:** 1,500 RPD (requests per day)
- **Free tier:** 1 million TPM (tokens per minute)

---

## 🎉 สรุป

### ทำไมต้อง Gemini?

1. **ฟรี 100%!** 🎁
   - ไม่มีค่าใช้จ่าย
   - ไม่ต้องใส่บัตรเครดิต

2. **ง่ายมาก** ⚡
   - Setup 3 นาที
   - ใช้งานได้ทันที

3. **คุณภาพสูง** ⭐
   - Vision API ดีมาก
   - รองรับภาษาไทย
   - วิเคราะห์แม่นยำ

4. **เหมาะสำหรับทุกคน** 👥
   - ผู้เริ่มต้น
   - นักพัฒนา
   - นักวิเคราะห์

---

## 🔄 Migration from Claude

### ถ้าคุณใช้ Claude อยู่:

```bash
# เปลี่ยนจาก Claude
python stock_bot_macos_agent.py

# เป็น Gemini
python stock_bot_macos_gemini.py
```

### ความแตกต่าง:
- ✅ Output เหมือนกัน
- ✅ Features เหมือนกัน
- ✅ แต่ Gemini **ฟรี!**

---

**🌟 เริ่มใช้ Gemini วันนี้ - ฟรี 100%!**

**📞 มีปัญหา? ดูที่ README.md หรือ test_gemini_api.py**

---

**Last Updated:** 2025-10-23
**Version:** Gemini 2.0 Flash
**Cost:** FREE! 🎉

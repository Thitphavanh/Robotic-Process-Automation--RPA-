#!/usr/bin/env python3
"""
Test script for Google Gemini API Key
ตรวจสอบว่า API Key ใช้งานได้หรือไม่
"""

import os
import sys

print("=" * 80)
print("🧪 ทดสอบ Google Gemini API Key")
print("=" * 80)

# ตรวจสอบว่าติดตั้ง google-generativeai หรือยัง
try:
    import google.generativeai as genai
    print("✅ พบ google-generativeai module")
except ImportError:
    print("❌ ไม่พบ google-generativeai module")
    print("\n💡 กรุณาติดตั้งก่อน:")
    print("   pip install google-generativeai")
    sys.exit(1)

# ตรวจสอบ API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    print(f"✅ พบ API Key จาก environment: {GEMINI_API_KEY[:20]}...")
else:
    print("⚠️  ไม่พบ API Key จาก environment variable")
    print("\n📝 กรุณาใส่ Google Gemini API Key:")
    GEMINI_API_KEY = input("🔑 API Key: ").strip()

if not GEMINI_API_KEY:
    print("\n❌ ไม่มี API Key! ออกจากโปรแกรม")
    sys.exit(1)

# ตรวจสอบรูปแบบ
if not GEMINI_API_KEY.startswith("AIzaSy"):
    print("\n⚠️  API Key ไม่ถูกต้อง! ควรขึ้นต้นด้วย 'AIzaSy'")
    print("💡 ตรวจสอบที่: https://makersuite.google.com/app/apikey")
    sys.exit(1)

print("\n" + "=" * 80)
print("🔍 กำลังทดสอบการเชื่อมต่อ...")
print("=" * 80)

try:
    # ตั้งค่า API
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ ตั้งค่า API Key สำเร็จ")

    # สร้าง model
    model = genai.GenerativeModel('gemini-2.5-pro')
    print("✅ สร้าง model สำเร็จ (gemini-2.5-pro)")

    # ทดสอบส่งคำของ่ายๆ
    print("\n📨 กำลังส่งคำขอทดสอบ...")
    response = model.generate_content("สวัสดีครับ ตอบกลับสั้นๆ ว่าคุณเป็นใคร")

    print("\n" + "=" * 80)
    print("✅ ทดสอบสำเร็จ! API Key ใช้งานได้")
    print("=" * 80)
    print(f"\n🤖 คำตอบจาก Gemini:\n{response.text}")

    # ทดสอบ vision capability
    print("\n" + "=" * 80)
    print("📸 ทดสอบความสามารถด้าน Vision...")
    print("=" * 80)

    try:
        from PIL import Image
        import io

        # สร้างภาพทดสอบ (ภาพสีเขียว 100x100)
        test_img = Image.new('RGB', (100, 100), color='green')
        print("✅ สร้างภาพทดสอบสำเร็จ")

        # ทดสอบวิเคราะห์ภาพ
        vision_response = model.generate_content([
            "อธิบายภาพนี้สั้นๆ",
            test_img
        ])

        print(f"✅ Vision API ทำงานได้")
        print(f"🤖 การวิเคราะห์ภาพ: {vision_response.text}")

    except Exception as e:
        print(f"⚠️  Vision test ล้มเหลว: {e}")
        print("แต่ text generation ทำงานได้ ยังใช้งานได้ปกติ")

    print("\n" + "=" * 80)
    print("📊 ข้อมูลการใช้งาน:")
    print("=" * 80)
    print("   Model: gemini-2.5-pro")
    print("   Free tier: ✅ ฟรี!")
    print("   Rate limit: 15 requests/minute")
    print("   Features: Text + Vision")

    print("\n" + "=" * 80)
    print("🎉 พร้อมใช้งาน Stock Bot Gemini แล้ว!")
    print("=" * 80)
    print("\n💡 รันโปรแกรมหลักด้วยคำสั่ง:")
    print("   python stock_bot_macos_gemini.py")

    print("\n💰 ข้อดีของ Gemini:")
    print("   ✅ ฟรี 100%! (ภายใน free tier)")
    print("   ✅ ความสามารถด้าน Vision ดีมาก")
    print("   ✅ รองรับภาษาไทยได้ดี")
    print("   ✅ ไม่มีค่าใช้จ่าย")
    print("   ✅ ใช้งานง่าย")

except Exception as e:
    print("\n" + "=" * 80)
    print("❌ เกิดข้อผิดพลาด!")
    print("=" * 80)
    print(f"\nError: {e}")
    print("\n💡 แก้ไข:")
    print("   1. ตรวจสอบว่า API Key ถูกต้อง")
    print("   2. สร้าง API Key ใหม่จาก https://makersuite.google.com/app/apikey")
    print("   3. ตรวจสอบว่ามี internet connection")
    print("   4. ตรวจสอบว่าไม่เกิน rate limit")
    print("\n   หรือตั้งค่าผ่าน environment variable:")
    print("   export GEMINI_API_KEY='AIzaSy-your-key-here'")
    sys.exit(1)

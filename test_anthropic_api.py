#!/usr/bin/env python3
"""
Test script for Anthropic API Key
ตรวจสอบว่า API Key ใช้งานได้หรือไม่
"""

import os
import sys

print("=" * 80)
print("🧪 ทดสอบ Anthropic API Key")
print("=" * 80)

# ตรวจสอบว่าติดตั้ง anthropic หรือยัง
try:
    import anthropic
    print("✅ พบ anthropic module")
except ImportError:
    print("❌ ไม่พบ anthropic module")
    print("\n💡 กรุณาติดตั้งก่อน:")
    print("   pip install anthropic")
    sys.exit(1)

# ตรวจสอบ API Key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if ANTHROPIC_API_KEY:
    print(f"✅ พบ API Key จาก environment: {ANTHROPIC_API_KEY[:20]}...")
else:
    print("⚠️  ไม่พบ API Key จาก environment variable")
    print("\n📝 กรุณาใส่ Anthropic API Key:")
    ANTHROPIC_API_KEY = input("🔑 API Key: ").strip()

if not ANTHROPIC_API_KEY:
    print("\n❌ ไม่มี API Key! ออกจากโปรแกรม")
    sys.exit(1)

# ตรวจสอบรูปแบบ
if not ANTHROPIC_API_KEY.startswith("sk-ant-"):
    print("\n⚠️  API Key ไม่ถูกต้อง! ควรขึ้นต้นด้วย 'sk-ant-'")
    sys.exit(1)

print("\n" + "=" * 80)
print("🔍 กำลังทดสอบการเชื่อมต่อ...")
print("=" * 80)

try:
    # สร้าง client
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    print("✅ สร้าง client สำเร็จ")

    # ทดสอบส่งคำของ่ายๆ
    print("\n📨 กำลังส่งคำขอทดสอบ...")
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": "สวัสดีครับ ตอบกลับสั้นๆ ว่าคุณเป็นใคร"
            }
        ]
    )

    print("\n" + "=" * 80)
    print("✅ ทดสอบสำเร็จ! API Key ใช้งานได้")
    print("=" * 80)
    print(f"\n🤖 คำตอบจาก Claude:\n{response.content[0].text}")
    print("\n" + "=" * 80)
    print("📊 ข้อมูลการใช้งาน:")
    print("=" * 80)
    print(f"   Model: {response.model}")
    print(f"   Input tokens: {response.usage.input_tokens}")
    print(f"   Output tokens: {response.usage.output_tokens}")

    # คำนวณค่าใช้จ่ายประมาณ
    input_cost = (response.usage.input_tokens / 1_000_000) * 3
    output_cost = (response.usage.output_tokens / 1_000_000) * 15
    total_cost = input_cost + output_cost

    print(f"\n💰 ค่าใช้จ่ายประมาณ:")
    print(f"   Input: ${input_cost:.6f}")
    print(f"   Output: ${output_cost:.6f}")
    print(f"   Total: ${total_cost:.6f}")

    print("\n" + "=" * 80)
    print("🎉 พร้อมใช้งาน Stock Bot AI แล้ว!")
    print("=" * 80)
    print("\n💡 รันโปรแกรมหลักด้วยคำสั่ง:")
    print("   python stock_bot_macos_agent.py")

except anthropic.AuthenticationError as e:
    print("\n" + "=" * 80)
    print("❌ API Key ไม่ถูกต้อง!")
    print("=" * 80)
    print(f"\nError: {e}")
    print("\n💡 แก้ไข:")
    print("   1. ตรวจสอบว่า API Key ถูกต้อง")
    print("   2. สร้าง API Key ใหม่จาก https://console.anthropic.com/")
    print("   3. ตรวจสอบว่า API Key ยังไม่หมดอายุ")
    print("\n   หรือตั้งค่าผ่าน environment variable:")
    print("   export ANTHROPIC_API_KEY='sk-ant-api03-your-key-here'")
    sys.exit(1)

except anthropic.PermissionDeniedError as e:
    print("\n" + "=" * 80)
    print("❌ ไม่มีสิทธิ์ใช้งาน!")
    print("=" * 80)
    print(f"\nError: {e}")
    print("\n💡 แก้ไข:")
    print("   1. ตรวจสอบว่าบัญชีมี credit เหลืออยู่")
    print("   2. ตรวจสอบสิทธิ์การใช้งาน API Key")
    print("   3. เติม credit ที่ https://console.anthropic.com/")
    sys.exit(1)

except anthropic.RateLimitError as e:
    print("\n" + "=" * 80)
    print("❌ เกินจำนวนครั้งที่ใช้งาน!")
    print("=" * 80)
    print(f"\nError: {e}")
    print("\n💡 แก้ไข:")
    print("   1. รอสักครู่แล้วลองใหม่")
    print("   2. อัปเกรดแพลนของคุณ")
    sys.exit(1)

except Exception as e:
    print("\n" + "=" * 80)
    print("❌ เกิดข้อผิดพลาด!")
    print("=" * 80)
    print(f"\nError: {e}")
    print("\n💡 ติดต่อ Anthropic Support:")
    print("   https://support.anthropic.com/")
    sys.exit(1)

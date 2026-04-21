#!/usr/bin/env python3
"""
Case-Law Interactive - Start script
"""

import subprocess
import webbrowser
import time
import sys

def start_case_law_app():
    """Case-Law Interactive app ni ishga tushirish"""
    print("🎓 Case-Law Interactive ishga tushirilmoqda...")
    print("📱 Port: 5006")
    print("🌐 URL: http://localhost:5006")
    print("📚 Interaktiv yuridik o'quv tizimi")
    print("🔑 Demo hisoblar:")
    print("   👩‍🏫 O'qituvchi: teacher / teacher123")
    print("   👨‍🎓 O'quvchi: student / student123")
    print("-" * 50)
    
    try:
        # Flask app ni background da ishga tushirish
        process = subprocess.Popen([sys.executable, 'case_law_interactive.py'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
        
        # 2 soniya kutib, brauzerni ochish
        time.sleep(2)
        
        # Brauzerni ochish
        webbrowser.open('http://localhost:5006')
        
        print("✅ Case-Law Interactive muvaffaqiyatli ishga tushirildi!")
        print("🌐 http://localhost:5006 manzilda ochilmoqda...")
        
        # Proses tugaguncha kutish
        process.wait()
        
    except FileNotFoundError:
        print("❌ Xatolik: case_law_interactive.py fayli topilmadi!")
        print("📁 Iltimos, fayl mavjudligini tekshiring.")
    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")
        print("🔧 Iltimos, qayta urinib ko'ring.")

if __name__ == "__main__":
    start_case_law_app()

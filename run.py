#!/usr/bin/env python3
"""
Case-Law Interactive - Interaktiv yuridik o'quv platformasi
Ishga tushirish skripti
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, init_db

def main():
    """Asosiy ishga tushirish funktsiyasi"""
    print("=" * 60)
    print("Case-Law Interactive - Interaktiv Yuridik O'quv Platformasi")
    print("=" * 60)
    
    # Initialize database
    try:
        print("Ma'lumotlar bazasini tayyorlash...")
        init_db()
        print("Ma'lumotlar bazasi muvaffaqiyatli tayyorlandi!")
    except Exception as e:
        print(f"Ma'lumotlar bazasini tayyorlashda xatolik: {e}")
        return
    
    # Check if port 5001 is available
    port = 5001
    print(f"Server {port} portida ishga tushirilmoqda...")
    print("Brauzerni oching va manzilga o'ting:")
    print(f"http://localhost:{port}")
    print("\nDemo hisoblar:")
    print("Admin: admin / admin123")
    print("O'qituvchi: teacher / teacher123")
    print("O'quvchi: student / student123")
    print("\nTo'xtatish uchun: Ctrl+C")
    print("=" * 60)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\nServer to'xtatildi.")
    except Exception as e:
        print(f"Serverni ishga tushirishda xatolik: {e}")

if __name__ == '__main__':
    main()

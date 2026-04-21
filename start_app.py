#!/usr/bin/env python3
import subprocess
import sys
import time
import webbrowser

print("Web app ni ishga tushirish...")
try:
    # Flask app ni background da ishga tushirish
    process = subprocess.Popen([sys.executable, "professional_legal_app.py"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    
    # 5 soniya kutish
    time.sleep(5)
    
    # Browser ni ochish
    webbrowser.open("http://localhost:5002")
    
    print("App ishga tushdi va browser ochildi!")
    print("http://localhost:5002")
    
    # Process ni kutish
    stdout, stderr = process.communicate()
    
except Exception as e:
    print(f"Xatolik: {e}")

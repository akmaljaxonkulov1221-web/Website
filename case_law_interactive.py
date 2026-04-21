#!/usr/bin/env python3
"""
Case-Law Interactive - Interaktiv yuridik o'quv tizimi
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'case-law-interactive-2024'

# Foydalanuvchilar ma'lumotlari
USERS = {
    'teacher': {
        'password_hash': generate_password_hash('teacher123'),
        'first_name': 'Teacher',
        'last_name': 'User',
        'role': 'teacher'
    },
    'student': {
        'password_hash': generate_password_hash('student123'),
        'first_name': 'Student',
        'last_name': 'User',
        'role': 'student'
    }
}

# Huquqiy ma'lumotlar
LEGAL_CASES = {
    'jinoyat_tarkibi': {
        'obekt': 'Jismoniy shaxs',
        'subekt': 'Jamiyat',
        'subyektiv': 'Davlat',
        'title': 'Jinoyat tarkibi',
        'description': 'Jinoyat tarkibidagi uch unsurlar: obekt, subekt, subyektiv',
        'flow': [
            {'step': 1, 'title': 'Obektni aniqlash', 'description': 'Kim jinoyat sodir etgan?'},
            {'step': 2, 'title': 'Subektni aniqlash', 'description': 'Jinoyat qaysi huquqqa tegishli?'},
            {'step': 3, 'title': 'Subyektivni aniqlash', 'description': 'Jinoyat qaysi manfaatga yetkazgan?'},
            {'step': 4, 'title': 'Jazo turi', 'description': 'Qanday jazo qo\'llanilishi kerak?'}
        ]
    },
    'talonchilik': {
        'obekt': 'Jismoniy shaxs',
        'subekt': 'Jamiyat',
        'subyektiv': 'Davlat',
        'title': 'Talonchilik',
        'description': 'Talonchilik tarkibi: obekt, subekt, subyektiv',
        'flow': [
            {'step': 1, 'title': 'Talonchilik belgilari', 'description': 'Talonchilikning alomatlari'},
            {'step': 2, 'title': 'Javobgarlik turlari', 'description': 'Qanday javobgarlik turlari mavjud?'},
            {'step': 3, 'title': 'Jarima miqdori', 'description': 'Jarima miqdorini belgilash'}
        ]
    }
}

# Test ma'lumotlari
TEST_RESULTS = {}

def load_data():
    """Ma'lumotlarni yuklash"""
    try:
        if os.path.exists('complete_uzbekistan_legal_codes.json'):
            with open('complete_uzbekistan_legal_codes.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Loaded {len(data.get('kodekslar', {}))} legal codes")
                return data.get('kodekslar', {})
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return {}

@app.route('/')
def index():
    """Asosiy sahifa"""
    return render_template('case_law_interactive.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login sahifasi"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and check_password_hash(USERS[username]['password_hash'], password):
            session['user_id'] = username
            session['role'] = USERS[username]['role']
            session['first_name'] = USERS[username]['first_name']
            flash(f"Xush kelibsiz, {USERS[username]['first_name']}!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login yoki parol noto\'g\'ri', 'danger')
    
    return render_template('case_law_login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_role = session.get('role')
    return render_template('case_law_dashboard.html', 
                         user_role=user_role,
                         first_name=session.get('first_name'))

@app.route('/fan/<fan_nomi>')
def fan_detail(fan_nomi):
    """Fan bo'yicha sahifa"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    case_data = LEGAL_CASES.get(fan_nomi, {})
    return render_template('case_law_subject_detail.html',
                         fan_nomi=fan_nomi,
                         case_data=case_data)

@app.route('/interactive/<case_type>')
def interactive_case(case_type):
    """Interaktiv holatlar"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    case_data = LEGAL_CASES.get(case_type, {})
    return render_template('case_law_interactive.html',
                         case_type=case_type,
                         case_data=case_data)

@app.route('/test')
def test():
    """Test sahifasi"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('case_law_test.html')

@app.route('/keys')
def keys():
    """Huquqiy kalitlar"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('case_law_keys.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('Siz tizimdan chiqdingiz', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5006)

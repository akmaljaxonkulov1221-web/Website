#!/usr/bin/env python3
"""
Professional Legal System with Login - Login tizimli to'liq yechim
3166 ta modda bilan
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
app.config['SECRET_KEY'] = 'professional-legal-system-2024'

# Global data storage
LEGAL_DATA = {}
ANALYZED_DATA = {}
ANALYSIS_REPORT = {}

# Simple user database (for demo)
USERS = {
    'admin': {
        'password_hash': generate_password_hash('admin123'),
        'first_name': 'Admin',
        'last_name': 'User',
        'is_admin': True
    },
    'teacher': {
        'password_hash': generate_password_hash('teacher123'),
        'first_name': 'Teacher',
        'last_name': 'User',
        'is_admin': False
    },
    'student': {
        'password_hash': generate_password_hash('student123'),
        'first_name': 'Student',
        'last_name': 'User',
        'is_admin': False
    }
}

def load_data():
    """Ma'lumotlarni yuklash"""
    global LEGAL_DATA, ANALYZED_DATA, ANALYSIS_REPORT
    
    try:
        # To'liq legal codes ma'lumotlarini yuklash
        if os.path.exists('complete_uzbekistan_legal_codes.json'):
            with open('complete_uzbekistan_legal_codes.json', 'r', encoding='utf-8') as f:
                complete_data = json.load(f)
                LEGAL_DATA = complete_data.get('kodekslar', {})
                logger.info(f"Loaded complete legal data: {complete_data.get('jami_kodekslar')} codes with {complete_data.get('jami_moddalar')} articles")
        elif os.path.exists('professional_legal_data.json'):
            # Agar to'liq ma'lumot bo'lmasa, professional ma'lumotlardan foydalanamiz
            with open('professional_legal_data.json', 'r', encoding='utf-8') as f:
                LEGAL_DATA = json.load(f)
                logger.info(f"Loaded professional legal data: {len(LEGAL_DATA)} codes")
        
        # AI tahlili ma'lumotlarini yuklash
        if os.path.exists('advanced_analyzed_legal_data.json'):
            with open('advanced_analyzed_legal_data.json', 'r', encoding='utf-8') as f:
                ANALYZED_DATA = json.load(f)
                logger.info(f"Loaded analyzed data for {len(ANALYZED_DATA)} codes")
        
        # Hisobotni yuklash
        if os.path.exists('analysis_report.json'):
            with open('analysis_report.json', 'r', encoding='utf-8') as f:
                ANALYSIS_REPORT = json.load(f)
                logger.info("Loaded analysis report")
                
    except Exception as e:
        logger.error(f"Error loading data: {e}")

# Login routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and check_password_hash(USERS[username]['password_hash'], password):
            session['user_id'] = username
            session['first_name'] = USERS[username]['first_name']
            session['last_name'] = USERS[username]['last_name']
            session['is_admin'] = USERS[username]['is_admin']
            flash(f'Xush kelibsiz, {USERS[username]["first_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login yoki parol noto\'g\'ri!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Siz tizimdan chiqdingiz!', 'info')
    return redirect(url_for('login'))

def login_required(f):
    """Login talab qiladigan decorator"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Main routes
@app.route('/')
@login_required
def dashboard():
    """Asosiy dashboard"""
    total_articles = sum(len(code_data.get('moddalar', [])) for code_data in LEGAL_DATA.values())
    
    return render_template('dashboard_with_login.html',
                         legal_data=LEGAL_DATA,
                         analyzed_data=ANALYZED_DATA,
                         analysis_report=ANALYSIS_REPORT,
                         total_articles=total_articles)

@app.route('/codes')
@login_required
def codes():
    """Kodekslar ro'yxati"""
    return render_template('codes.html', legal_data=LEGAL_DATA)

@app.route('/code/<code_name>')
@login_required
def code_detail(code_name):
    """Kodeks tafsilotlari"""
    if code_name in LEGAL_DATA:
        code_info = LEGAL_DATA[code_name]
        return render_template('code_detail.html', code_name=code_name, code_info=code_info)
    else:
        flash('Kodeks topilmadi!', 'error')
        return redirect(url_for('codes'))

@app.route('/search')
@login_required
def search():
    """Qidiruv"""
    query = request.args.get('q', '')
    results = []
    
    if query:
        query_lower = query.lower()
        for code_name, code_data in LEGAL_DATA.items():
            for article in code_data.get('moddalar', []):
                if (query_lower in article.get('nomi', '').lower() or 
                    query_lower in article.get('matn', '').lower() or
                    query_lower in article.get('modda', '').lower()):
                    results.append({
                        'code_name': code_name,
                        'article': article
                    })
    
    return render_template('search_results.html', query=query, results=results)

@app.route('/api/statistics')
@login_required
def api_statistics():
    """Statistika API"""
    if not LEGAL_DATA:
        return jsonify({'error': 'No data available'})
    
    stats = {
        'total_codes': len(LEGAL_DATA),
        'total_articles': sum(len(code_data.get('moddalar', [])) for code_data in LEGAL_DATA.values()),
        'codes': []
    }
    
    for code_name, code_data in LEGAL_DATA.items():
        stats['codes'].append({
            'name': code_name,
            'articles_count': len(code_data.get('moddalar', []))
        })
    
    return jsonify(stats)

@app.route('/api/articles/<code_name>')
@login_required
def api_articles(code_name):
    """Moddalar API"""
    if code_name in LEGAL_DATA:
        return jsonify(LEGAL_DATA[code_name].get('moddalar', []))
    else:
        return jsonify({'error': 'Code not found'}), 404

@app.route('/profile')
@login_required
def profile():
    """Profil"""
    return render_template('profile.html')

if __name__ == '__main__':
    # Ma'lumotlarni yuklash
    load_data()
    
    if not LEGAL_DATA:
        logger.error("No legal data found. Please run complete_uzbekistan_legal_codes.py first.")
        print("Please run complete_uzbekistan_legal_codes.py first to generate data.")
    else:
        logger.info("Starting Professional Legal System with Login...")
        total_articles = sum(len(code_data.get('moddalar', [])) for code_data in LEGAL_DATA.values())
        logger.info(f"Loaded {len(LEGAL_DATA)} codes with {total_articles} articles")
        logger.info(f"Analysis report available: {bool(ANALYSIS_REPORT)}")
        
        print(f"\n=== PROFESSIONAL LEGAL SYSTEM WITH LOGIN ===")
        print(f"Total codes: {len(LEGAL_DATA)}")
        print(f"Total articles: {total_articles}")
        print(f"Users: admin/admin123, teacher/teacher123, student/student123")
        print(f"URL: http://localhost:5003")
        
        app.run(debug=True, host='0.0.0.0', port=5003)

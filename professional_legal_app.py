#!/usr/bin/env python3
"""
Professional Legal Web Application - Mukammal web interfeysi
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
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

@app.route('/')
def index():
    """Asosiy sahifa"""
    # Force reload data to ensure latest version
    load_data()
    
    # Debug info
    print(f"DEBUG: Legal codes loaded: {len(LEGAL_DATA)}")
    print(f"DEBUG: Analysis report keys: {list(ANALYSIS_REPORT.keys()) if ANALYSIS_REPORT else 'None'}")
    print(f"DEBUG: Total codes: {ANALYSIS_REPORT.get('total_codes', 0)}")
    print(f"DEBUG: Total articles: {ANALYSIS_REPORT.get('total_articles', 0)}")
    
    return render_template('professional_index.html', 
                         legal_codes=list(LEGAL_DATA.keys()),
                         legal_data=LEGAL_DATA,
                         analysis_report=ANALYSIS_REPORT)

@app.route('/dashboard')
def dashboard():
    """Dashboard - barcha foydalanuvchilar uchun ochiq"""
    return render_template('student_dashboard.html',
                         legal_data=LEGAL_DATA,
                         analyzed_data=ANALYZED_DATA,
                         analysis_report=ANALYSIS_REPORT)

@app.route('/codes')
def codes():
    """Barcha kodekslar ro'yxati"""
    return render_template('codes.html', 
                         legal_data=LEGAL_DATA,
                         analysis_report=ANALYSIS_REPORT)

@app.route('/code/<code_name>')
def code_detail(code_name):
    """Kodeks tafsilotlari"""
    code_data = LEGAL_DATA.get(code_name, {})
    analyzed_code_data = ANALYZED_DATA.get(code_name, [])
    
    return render_template('code_detail.html',
                         code_name=code_name,
                         code_data=code_data,
                         analyzed_data=analyzed_code_data)

@app.route('/article/<code_name>/<article_id>')
def article_detail(code_name, article_id):
    """Modda tafsilotlari"""
    # Asosiy ma'lumot
    article = None
    code_data = LEGAL_DATA.get(code_name, {})
    for art in code_data.get('moddalar', []):
        if art.get('id') == article_id:
            article = art
            break
    
    # AI tahlili
    analyzed_article = None
    for art in ANALYZED_DATA.get(code_name, []):
        if art.get('id') == article_id:
            analyzed_article = art
            break
    
    return render_template('case_law_article_detail.html',
                         code_name=code_name,
                         article=article,
                         analyzed_article=analyzed_article)

@app.route('/search')
def search():
    """Qidiruv sahifasi"""
    query = request.args.get('q', '').lower()
    code_filter = request.args.get('code', 'all')
    results = []
    
    if query:
        for code_name, code_data in LEGAL_DATA.items():
            for article in code_data.get('moddalar', []):
                if query.lower() in article.get('nomi', '').lower() or query.lower() in article.get('matn', '').lower():
                    results.append({
                        'code_name': code_name,
                        'article': article
                    })
    
    return render_template('search.html', 
                         query=query,
                         results=results,
                         legal_data=LEGAL_DATA)

@app.route('/legal_map')
def legal_map():
    """Huquqiy xarita sahifasi"""
    return render_template('legal_map.html',
                         legal_data=LEGAL_DATA,
                         analysis_report=ANALYSIS_REPORT)

@app.route('/analysis')
def analysis():
    """AI tahlili sahifasi"""
    return render_template('analysis.html',
                         analysis_report=ANALYSIS_REPORT,
                         analyzed_data=ANALYZED_DATA)

@app.route('/visualization')
def visualization():
    """Vizualizatsiya sahifasi"""
    return render_template('visualization.html',
                         analyzed_data=ANALYZED_DATA,
                         analysis_report=ANALYSIS_REPORT)

@app.route('/api/statistics')
def api_statistics():
    """Statistika API"""
    return jsonify(ANALYSIS_REPORT)

@app.route('/api/codes')
def api_codes():
    """Kodekslar API"""
    return jsonify(LEGAL_DATA)

@app.route('/api/analyzed_data')
def api_analyzed_data():
    """Tahlil qilingan ma'lumotlar API"""
    return jsonify(ANALYZED_DATA)

@app.route('/api/article/<code_name>/<article_id>')
def api_article(code_name, article_id):
    """Modda API"""
    # Asosiy ma'lumot
    article = None
    for art in LEGAL_DATA.get(code_name, []):
        if art.get('id') == article_id:
            article = art
            break
    
    # AI tahlili
    analyzed_article = None
    for art in ANALYZED_DATA.get(code_name, []):
        if art.get('id') == article_id:
            analyzed_article = art
            break
    
    return jsonify({
        'article': article,
        'analyzed_article': analyzed_article
    })

@app.route('/debug')
def debug():
    """Debug endpoint to check loaded data"""
    debug_info = {
        'legal_data_loaded': len(LEGAL_DATA),
        'legal_codes': list(LEGAL_DATA.keys()),
        'total_articles': sum(len(code_data.get('moddalar', [])) for code_data in LEGAL_DATA.values()),
        'analysis_report_loaded': bool(ANALYSIS_REPORT)
    }
    
    # Add article counts per code
    for code_name, code_data in LEGAL_DATA.items():
        debug_info[f'{code_name}_articles'] = len(code_data.get('moddalar', []))
    
    return jsonify(debug_info)

@app.route('/export/json')
def export_json():
    """JSON formatida eksport"""
    export_data = {
        'legal_data': LEGAL_DATA,
        'analyzed_data': ANALYZED_DATA,
        'analysis_report': ANALYSIS_REPORT,
        'export_timestamp': datetime.now().isoformat()
    }
    
    # Vaqtinchalik fayl yaratish
    temp_file = 'legal_system_export.json'
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    return send_file(temp_file, 
                     as_attachment=True,
                     download_name=f'legal_system_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
                     mimetype='application/json')

if __name__ == '__main__':
    # Ma'lumotlarni yuklash
    load_data()
    
    if not LEGAL_DATA:
        logger.error("No legal data found. Please run complete_uzbekistan_legal_codes.py first.")
        print("Please run complete_uzbekistan_legal_codes.py first to generate data.")
    else:
        logger.info("Starting Professional Legal Web Application...")
        total_articles = sum(len(code_data.get('moddalar', [])) for code_data in LEGAL_DATA.values())
        logger.info(f"Loaded {len(LEGAL_DATA)} codes with {total_articles} articles")
        logger.info(f"Analysis report available: {bool(ANALYSIS_REPORT)}")
        
        # Production environment check
        import os
        debug_mode = os.getenv('FLASK_ENV') != 'production'
        port = int(os.getenv('PORT', 5005))
        
        app.run(debug=debug_mode, host='0.0.0.0', port=port)

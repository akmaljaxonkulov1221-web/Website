#!/usr/bin/env python3
"""
Case-Law Interactive - To'liq interaktiv yuridik o'quv tizimi
3166 ta modda bilan to'liq funksional tizim
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
app.config['SECRET_KEY'] = 'case-law-interactive-2024-ultimate'

# Global data storage
LEGAL_DATA = {}
ANALYZED_DATA = {}
ANALYSIS_REPORT = {}
USER_PROGRESS = {}
CLASS_DATA = {}
TEST_RESULTS = {}

# Enhanced user database
USERS = {
    'admin': {
        'password_hash': generate_password_hash('admin123'),
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@legal.uz',
        'role': 'Administrator',
        'is_admin': True,
        'is_teacher': True,
        'avatar': 'https://picsum.photos/seed/admin/100/100'
    },
    'teacher': {
        'password_hash': generate_password_hash('teacher123'),
        'first_name': 'Teacher',
        'last_name': 'Professional',
        'email': 'teacher@legal.uz',
        'role': 'Teacher',
        'is_admin': False,
        'is_teacher': True,
        'avatar': 'https://picsum.photos/seed/teacher/100/100'
    },
    'student': {
        'password_hash': generate_password_hash('student123'),
        'first_name': 'Student',
        'last_name': 'User',
        'email': 'student@legal.uz',
        'role': 'Student',
        'is_admin': False,
        'is_teacher': False,
        'avatar': 'https://picsum.photos/seed/student/100/100'
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
            session['email'] = USERS[username]['email']
            session['role'] = USERS[username]['role']
            session['avatar'] = USERS[username]['avatar']
            session['is_admin'] = USERS[username]['is_admin']
            session['is_teacher'] = USERS[username]['is_teacher']
            session['login_time'] = datetime.now().strftime('%H:%M')
            flash(f'Xush kelibsiz, {USERS[username]["first_name"]} {USERS[username]["last_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login yoki parol noto\'g\'ri!', 'error')
    
    return render_template('case_law_login.html')

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
    total_codes = len(LEGAL_DATA)
    
    # User progress
    user_progress = USER_PROGRESS.get(session['user_id'], {
        'completed_articles': 0,
        'completed_tests': 0,
        'total_score': 0
    })
    
    return render_template('case_law_dashboard.html',
                         legal_data=LEGAL_DATA,
                         analyzed_data=ANALYZED_DATA,
                         analysis_report=ANALYSIS_REPORT,
                         total_articles=total_articles,
                         total_codes=total_codes,
                         user_progress=user_progress)

@app.route('/subjects')
@login_required
def subjects():
    """Fanlar ro'yxati"""
    subjects = [
        {'id': 1, 'name': 'Jinoyat huquqi', 'icon': 'fa-gavel', 'color': 'red', 'description': 'Jinoyat kodeksi va amaliyoti'},
        {'id': 2, 'name': 'Fuqarolik huquqi', 'icon': 'fa-handshake', 'color': 'blue', 'description': 'Fuqarolik kodeksi va huquqiy munosabatlar'},
        {'id': 3, 'name': 'Mehnat huquqi', 'icon': 'fa-briefcase', 'color': 'green', 'description': 'Mehnat kodeksi va mehnat munosabatlari'},
        {'id': 4, 'name': 'Oila huquqi', 'icon': 'fa-home', 'color': 'yellow', 'description': 'Oila kodeksi va oilaviy munosabatlar'},
        {'id': 5, 'name': 'Ma\'muriy huquq', 'icon': 'fa-shield-alt', 'color': 'purple', 'description': 'Ma\'muriy javobgarlik kodeksi'},
        {'id': 6, 'name': 'Yer huquqi', 'icon': 'fa-mountain', 'color': 'brown', 'description': 'Yer kodeksi va yer munosabatlari'}
    ]
    
    return render_template('case_law_subjects.html', subjects=subjects)

@app.route('/subject/<int:subject_id>')
@login_required
def subject_detail(subject_id):
    """Fan tafsilotlari"""
    subjects = {
        1: {'name': 'Jinoyat huquqi', 'code': 'Jinoyat kodeksi'},
        2: {'name': 'Fuqarolik huquqi', 'code': 'Fuqarolik kodeksi'},
        3: {'name': 'Mehnat huquqi', 'code': 'Mehnat kodeksi'},
        4: {'name': 'Oila huquqi', 'code': 'Oila kodeksi'},
        5: {'name': 'Ma\'muriy huquq', 'code': 'Ma\'muriy javobgarlik kodeksi'},
        6: {'name': 'Yer huquqi', 'code': 'Yer kodeksi'}
    }
    
    subject = subjects.get(subject_id)
    if not subject:
        flash('Fan topilmadi!', 'error')
        return redirect(url_for('subjects'))
    
    # Get articles for this subject
    code_data = LEGAL_DATA.get(subject['code'], {})
    articles = code_data.get('moddalar', [])
    
    return render_template('case_law_subject_detail.html', 
                         subject=subject, 
                         articles=articles[:20],  # Show first 20 articles
                         subject_id=subject_id)

@app.route('/article/<code_name>/<article_id>')
@login_required
def article_detail(code_name, article_id):
    """Modda tafsilotlari - interaktiv"""
    if code_name in LEGAL_DATA:
        code_data = LEGAL_DATA[code_name]
        articles = code_data.get('moddalar', [])
        
        # Find the specific article
        article = None
        for art in articles:
            if art.get('id') == article_id or art.get('modda') == article_id:
                article = art
                break
        
        if not article:
            flash('Modda topilmadi!', 'error')
            return redirect(url_for('subjects'))
        
        # Generate visual data for this article
        visual_data = generate_visual_data(article, code_name)
        
        return render_template('case_law_article_detail.html', 
                             article=article, 
                             code_name=code_name,
                             visual_data=visual_data)
    else:
        flash('Kodeks topilmadi!', 'error')
        return redirect(url_for('subjects'))

def generate_visual_data(article, code_name):
    """Modda uchun vizual ma'lumotlar generatsiya qilish"""
    visual_data = {
        'diagram': generate_diagram(article, code_name),
        'flowchart': generate_flowchart(article, code_name),
        'timeline': generate_timeline(article, code_name),
        'keys': generate_keys(article, code_name),
        'animation': generate_animation_data(article, code_name)
    }
    return visual_data

def generate_diagram(article, code_name):
    """Diagramma generatsiya qilish"""
    if 'Jinoyat' in code_name:
        return {
            'type': 'crime_composition',
            'elements': [
                {'name': 'Ob\'ekt', 'description': 'Jinoyat ta\'siri etuvchi jamiyat manfaatlari', 'position': {'x': 200, 'y': 50}},
                {'name': 'Sub\'ekt', 'description': 'Jinoyatni sodir etgan shaxs (16 yoshdan)', 'position': {'x': 50, 'y': 150}},
                {'name': 'Subyektiv tomon', 'description': 'Qasddorlik yoki ehtiyotsizlik', 'position': {'x': 350, 'y': 150}},
                {'name': 'Obyektiv tomon', 'description': 'Xavfli harakat va oqibat', 'position': {'x': 200, 'y': 250}}
            ],
            'connections': [
                {'from': 'Sub\'ekt', 'to': 'Obyektiv tomon', 'label': 'Sodir etadi'},
                {'from': 'Obyektiv tomon', 'to': 'Ob\'ekt', 'label': 'Ta\'sir qiladi'},
                {'from': 'Subyektiv tomon', 'to': 'Sub\'ekt', 'label': 'Belgilaydi'}
            ]
        }
    else:
        return {
            'type': 'legal_relation',
            'elements': [
                {'name': 'Tomonlar', 'description': 'Huquqiy munosabat ishtirokchilari', 'position': {'x': 200, 'y': 50}},
                {'name': 'Huquq', 'description': 'Tomonlarning huquqlari', 'position': {'x': 50, 'y': 150}},
                {'name': 'Majburiyat', 'description': 'Tomonlarning majburiyatlari', 'position': {'x': 350, 'y': 150}},
                {'name': 'Javobgarlik', 'description': 'Buzilishning oqibatlari', 'position': {'x': 200, 'y': 250}}
            ]
        }

def generate_flowchart(article, code_name):
    """Flowchart generatsiya qilish"""
    return {
        'type': 'process_flow',
        'steps': [
            {'id': 1, 'title': 'Holat yuzaga keladi', 'description': 'Huquqiy munosabatlar vujudga keladi', 'type': 'start'},
            {'id': 2, 'title': 'Huquq buziladi', 'description': 'Norma buzilishi sodir bo\'ladi', 'type': 'process'},
            {'id': 3, 'title': 'Javobgarlik kelib chiqadi', 'description': 'Yuridik javobgarlik paydo bo\'ladi', 'type': 'decision'},
            {'id': 4, 'title': 'Jazo qo\'llaniladi', 'description': 'Belgilangan choralar ko\'llaniladi', 'type': 'end'}
        ],
        'connections': [
            {'from': 1, 'to': 2},
            {'from': 2, 'to': 3},
            {'from': 3, 'to': 4, 'condition': 'ha'},
            {'from': 3, 'to': 1, 'condition': 'yo\'q'}
        ]
    }

def generate_timeline(article, code_name):
    """Timeline generatsiya qilish"""
    return {
        'type': 'event_sequence',
        'events': [
            {'time': 'T-1', 'title': 'Tayyorgarlik', 'description': 'Jinoyatga tayyorgarlik ko\'riladi'},
            {'time': 'T', 'title': 'Sodir etish', 'description': 'Jinoyat sodir etiladi'},
            {'time': 'T+1', 'title': 'Aniqlash', 'description': 'Jinoyat aniqlanadi'},
            {'time': 'T+7', 'title': 'Tergov', 'description': 'Tergov boshlanadi'},
            {'time': 'T+30', 'title': 'Sud', 'description': 'Sud jarayoni boshlanadi'}
        ]
    }

def generate_keys(article, code_name):
    """Interaktiv keyslar generatsiya qilish"""
    return {
        'type': 'decision_tree',
        'scenarios': [
            {
                'id': 1,
                'title': 'Vaziyat 1: Shaxs do\'konidan narsa olib qochadi',
                'description': 'Bir kishi do\'kondan mahsulot olib, to\'lamasdan qochib ketmoqda',
                'question': 'Bu vaziyatda jinoyat bormi?',
                'options': [
                    {'text': 'Ha, o\'g\'rilik', 'correct': True, 'explanation': 'O\'g\'rilik - o\'zganing mulkini qonunga zid ravishda olish'},
                    {'text': 'Yo\'q, jinoyat emas', 'correct': False, 'explanation': 'Bu holatda o\'g\'rilik jinoyati sodir bo\'lmoqda'}
                ]
            },
            {
                'id': 2,
                'title': 'Vaziyat 2: Shaxs pulni topib oladi',
                'description': 'Ko\'chada topilgan pul sumkasini olib ketayotgan shaxs',
                'question': 'Bu qilmish jinoyat hisoblanadimi?',
                'options': [
                    {'text': 'Ha, o\'g\'rilik', 'correct': False, 'explanation': 'Topilgan mulkni olish o\'g\'rilik emas, agar egasi topilmasa'},
                    {'text': 'Yo\'q, jinoyat emas', 'correct': True, 'explanation': 'Topilgan mulkni olish qonunga zid emas (agar egasi ma\'lum bo\'lsa)'}
                ]
            }
        ]
    }

def generate_animation_data(article, code_name):
    """Animatsiya ma'lumotlari generatsiya qilish"""
    return {
        'type': 'scene_animation',
        'scenes': [
            {
                'id': 1,
                'title': 'Jinoyat sodir etish',
                'duration': 30,
                'description': 'Jinoyat qanday sodir bo\'lishi ko\'rsatiladi',
                'steps': [
                    {'time': 0, 'action': 'Shaxs ob\'ektni ko\'radi', 'description': 'Ehtiyotliqlik shakllanadi'},
                    {'time': 10, 'action': 'Tayyorgarlik ko\'riladi', 'description': 'Jinoyatga tayyorgarlik'},
                    {'time': 20, 'action': 'Harakat amalga oshiriladi', 'description': 'Jinoyat sodir etiladi'},
                    {'time': 30, 'action': 'Oqibat', 'description': 'Jinoyat natijasi'}
                ]
            }
        ]
    }

@app.route('/test/<article_id>')
@login_required
def article_test(article_id):
    """Modda bo'yicha test"""
    # Generate test questions for this article
    test_data = generate_test_questions(article_id)
    
    return render_template('case_law_article_test.html', 
                         test_data=test_data, 
                         article_id=article_id)

def generate_test_questions(article_id):
    """Test savollari generatsiya qilish"""
    return {
        'title': f'Modda {article_id} bo\'yicha test',
        'questions': [
            {
                'id': 1,
                'question': 'Ushbu modda qaysi huquq sohasiga tegishli?',
                'type': 'multiple_choice',
                'options': [
                    'Jinoyat huquqi',
                    'Fuqarolik huquqi',
                    'Mehnat huquqi',
                    'Oila huquqi'
                ],
                'correct': 0
            },
            {
                'id': 2,
                'question': 'Modda asosiy xususiyatini belgilang',
                'type': 'true_false',
                'correct': True
            },
            {
                'id': 3,
                'question': 'Modda qo\'llanilish shartlarini sanang',
                'type': 'multiple_answer',
                'options': [
                    'Shaxs 16 yoshga to\'lgan bo\'lishi',
                    'Aqli raso bo\'lishi',
                    'Qasddorlik borligi',
                    'Jazo belgilangan bo\'lishi'
                ],
                'correct': [0, 1, 2, 3]
            }
        ]
    }

@app.route('/submit_test', methods=['POST'])
@login_required
def submit_test():
    """Test natijalarini saqlash"""
    test_data = request.json
    article_id = test_data.get('article_id')
    answers = test_data.get('answers')
    
    # Calculate score
    score = calculate_test_score(article_id, answers)
    
    # Save user progress
    user_id = session['user_id']
    if user_id not in TEST_RESULTS:
        TEST_RESULTS[user_id] = []
    
    TEST_RESULTS[user_id].append({
        'article_id': article_id,
        'score': score,
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({'score': score, 'message': 'Test muvaffaqiyatli yakunlandi!'})

def calculate_test_score(article_id, answers):
    """Test ballarini hisoblash"""
    # Simple scoring logic - can be enhanced
    total_questions = len(answers)
    correct_answers = sum(1 for answer in answers if answer.get('correct', False))
    return int((correct_answers / total_questions) * 100) if total_questions > 0 else 0

@app.route('/legal_map')
@login_required
def legal_map():
    """Huquqiy xarita"""
    # Build legal map data
    map_data = build_legal_map()
    
    return render_template('case_law_legal_map.html', map_data=map_data)

def build_legal_map():
    """Huquqiy xarita ma'lumotlarini qurish"""
    return {
        'nodes': [],
        'connections': []
    }

@app.route('/teacher_panel')
@login_required
def teacher_panel():
    """O'qituvchi paneli"""
    if not session.get('is_teacher'):
        flash('Siz o\'qituvchi emassiz!', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('case_law_teacher_panel.html')

@app.route('/create_class', methods=['POST'])
@login_required
def create_class():
    """Sinf yaratish"""
    if not session.get('is_teacher'):
        return jsonify({'error': 'Ruxsat berilmagan'}), 403
    
    class_data = request.json
    class_id = f"class_{len(CLASS_DATA) + 1}"
    
    CLASS_DATA[class_id] = {
        'id': class_id,
        'name': class_data.get('name'),
        'teacher_id': session['user_id'],
        'students': [],
        'created_at': datetime.now().isoformat()
    }
    
    return jsonify({'class_id': class_id, 'message': 'Sinf muvaffaqiyatli yaratildi!'})

@app.route('/join_class', methods=['POST'])
@login_required
def join_class():
    """Sinfqa qo'shilish"""
    class_id = request.json.get('class_id')
    
    if class_id in CLASS_DATA:
        if session['user_id'] not in CLASS_DATA[class_id]['students']:
            CLASS_DATA[class_id]['students'].append(session['user_id'])
            return jsonify({'message': 'Sinfqa muvaffaqiyatli qo\'shildingiz!'})
        else:
            return jsonify({'error': 'Siz allaqachon ushbu sinfga qo\'shilgansiz!'}), 400
    else:
        return jsonify({'error': 'Sinf topilmadi!'}), 404

@app.route('/profile')
@login_required
def profile():
    """Profil"""
    user_id = session['user_id']
    user_progress = USER_PROGRESS.get(user_id, {})
    user_tests = TEST_RESULTS.get(user_id, [])
    
    return render_template('case_law_profile.html', 
                         user_progress=user_progress,
                         user_tests=user_tests)

# API routes
@app.route('/api/article_visual/<article_id>')
@login_required
def api_article_visual(article_id):
    """Modda vizuallari API"""
    # Find article
    article = None
    code_name = None
    for code, data in LEGAL_DATA.items():
        for art in data.get('moddalar', []):
            if art.get('id') == article_id or art.get('modda') == article_id:
                article = art
                code_name = code
                break
        if article:
            break
    
    if article:
        visual_data = generate_visual_data(article, code_name)
        return jsonify(visual_data)
    else:
        return jsonify({'error': 'Article not found'}), 404

@app.route('/api/check_answer', methods=['POST'])
@login_required
def api_check_answer():
    """Javobni tekshirish API"""
    data = request.json
    scenario_id = data.get('scenario_id')
    selected_option = data.get('selected_option')
    
    # Simple logic - can be enhanced
    is_correct = selected_option == 0  # First option is correct for demo
    
    return jsonify({
        'correct': is_correct,
        'explanation': 'To\'g\'ri javob. Bu holatda...' if is_correct else 'Noto\'g\'ri javob. To\'g\'ri javob...'
    })

if __name__ == '__main__':
    # Ma'lumotlarni yuklash
    load_data()
    
    if not LEGAL_DATA:
        logger.error("No legal data found. Please run complete_uzbekistan_legal_codes.py first.")
        print("Please run complete_uzbekistan_legal_codes.py first to generate data.")
    else:
        logger.info("Starting Case-Law Interactive System...")
        total_articles = sum(len(code_data.get('moddalar', [])) for code_data in LEGAL_DATA.values())
        logger.info(f"Loaded {len(LEGAL_DATA)} codes with {total_articles} articles")
        
        print(f"\n=== CASE-LAW INTERACTIVE SYSTEM ===")
        print(f"Total codes: {len(LEGAL_DATA)}")
        print(f"Total articles: {total_articles}")
        print(f"Users: admin/admin123, teacher/teacher123, student/student123")
        print(f"URL: http://localhost:5005")
        print(f"Features: Interaktiv o\'quv, 3166 ta modda, Testlar, Animatsiyalar")
        
        app.run(debug=True, host='0.0.0.0', port=5005)

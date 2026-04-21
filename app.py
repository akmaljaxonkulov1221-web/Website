from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'case-law-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///case_law_interactive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    is_teacher = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    test_results = db.relationship('TestResult', backref='student', lazy=True)
    case_progress = db.relationship('CaseProgress', backref='student', lazy=True)
    classes_taught = db.relationship('Class', backref='teacher', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # emoji or icon name
    color = db.Column(db.String(20))  # hex color
    
    # Relationships
    articles = db.relationship('Article', backref='subject', lazy=True, cascade='all, delete-orphan')
    tests = db.relationship('Test', backref='subject', lazy=True, cascade='all, delete-orphan')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)  # modda raqami
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    
    # Visual elements
    diagram_data = db.Column(db.Text)  # JSON for diagrams
    flowchart_data = db.Column(db.Text)  # JSON for flowcharts
    timeline_data = db.Column(db.Text)  # JSON for timelines
    
    # Relationships
    cases = db.relationship('Case', backref='article', lazy=True, cascade='all, delete-orphan')
    related_articles = db.relationship('RelatedArticle', foreign_keys='RelatedArticle.article_id', backref='article', lazy=True, cascade='all, delete-orphan')

class RelatedArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    related_article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    relationship_type = db.Column(db.String(50))  # 'similar', 'opposite', 'consequence'

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    scenario = db.Column(db.Text, nullable=False)  # vaziyat tavsifi
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    
    # Interactive elements
    decision_question = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(10), nullable=False)  # 'yes' or 'no'
    explanation = db.Column(db.Text, nullable=False)
    
    # Animation data
    animation_steps = db.Column(db.Text)  # JSON for animation
    
    # Relationships
    user_progress = db.relationship('CaseProgress', backref='case', lazy=True)

class CaseProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    user_answer = db.Column(db.String(10))
    is_correct = db.Column(db.Boolean)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    attempts = db.Column(db.Integer, default=1)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    test_type = db.Column(db.String(20), default='kahoot')  # kahoot, traditional
    time_limit = db.Column(db.Integer, default=300)  # seconds
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    questions = db.relationship('Question', backref='test', lazy=True, cascade='all, delete-orphan')
    results = db.relationship('TestResult', backref='test', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)
    points = db.Column(db.Integer, default=10)
    time_seconds = db.Column(db.Integer, default=30)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_points = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    time_taken = db.Column(db.Integer)  # seconds

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    join_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    students = db.relationship('ClassStudent', backref='class_obj', lazy=True)
    assignments = db.relationship('Assignment', backref='class_obj', lazy=True)

class ClassStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=True)
    due_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='User',
                is_admin=True,
                is_teacher=True
            )
            db.session.add(admin)
        
        # Create sample subject
        subject = Subject.query.filter_by(name='Jinoyat huquqi').first()
        if not subject:
            subject = Subject(
                name='Jinoyat huquqi',
                description='Jinoyat huquqi asoslari va moddalari',
                icon='gavel',
                color='#FF6B6B'
            )
            db.session.add(subject)
            db.session.flush()
            
            # Create sample article
            article = Article(
                number='169-modda',
                title='O\'g\'rilik',
                content='O\'g\'rilik - bu boshqa kishining mol-mulkini noqonuniy olib qochish...',
                subject_id=subject.id,
                diagram_data=json.dumps({
                    'type': 'crime_structure',
                    'elements': [
                        {'name': 'Ob\'ekt', 'value': 'Boshqa kishining mol-mulki'},
                        {'name': 'Sub\'ekt', 'value': '16 yoshga to\'lgan, aqli raso shaxs'},
                        {'name': 'Obyektiv tomon', 'value': 'Noqonuniy olib qochish harakati'},
                        {'name': 'Subyektiv tomon', 'value': 'Bexosorlik, o\'z manfaati uchun'}
                    ]
                }),
                flowchart_data=json.dumps({
                    'type': 'crime_process',
                    'steps': [
                        'Shaxs mol-mulkni ko\'radi',
                        'Olib qochishga qaror qiladi',
                        'Mol-mulkni olib qochadi',
                        'Mol-mulkni o\'zlashtiradi'
                    ]
                })
            )
            db.session.add(article)
            db.session.flush()
            
            # Create sample case
            case = Case(
                title='Telefon o\'g\'irlash holati',
                description='Odamlar orasida turgan holda telefon o\'g\'irlash',
                scenario='Ali bozorda turib, sotuvchining stol ustida qo\'yilgan telefonni ko\'radi. Hech kim ko\'rmayotgan paytda telefonni olib, yashirinadi. Bu vaziyatda jinoyat bormi?',
                article_id=article.id,
                decision_question='Bu vaziyatda jinoyat sodir bo\'lganmi?',
                correct_answer='yes',
                explanation='Ha, bu o\'g\'rilik jinoyatining to\'liq tarkibi mavjud. Ali boshqa kishining mol-mulkini (telefon) noqonuniy olib qochdi.',
                animation_steps=json.dumps([
                    {'step': 1, 'description': 'Ali telefonni ko\'radi', 'duration': 2000},
                    {'step': 2, 'description': 'Atrofga qaraydi', 'duration': 1000},
                    {'step': 3, 'description': 'Telefonni oladi', 'duration': 1500},
                    {'step': 4, 'description': 'Yashirinadi', 'duration': 1500}
                ])
            )
            db.session.add(case)
            
            # Create sample test
            test = Test(
                title='O\'g\'rilik moddasi bo\'yicha test',
                subject_id=subject.id,
                test_type='kahoot',
                time_limit=300
            )
            db.session.add(test)
            db.session.flush()
            
            # Create sample questions
            questions = [
                {
                    'question': 'O\'g\'rilik jinoyatining ob\'ektini aniqlang?',
                    'options': ['Boshqa kishining mol-mulki', 'Davlat mulki', 'Shaxsiy narsalar', 'Hamma to\'g\'ri'],
                    'correct': 'a'
                },
                {
                    'question': 'O\'g\'rilik uchun javobgarlik necha yoshdan boshlanadi?',
                    'options': ['14 yosh', '16 yosh', '18 yosh', '21 yosh'],
                    'correct': 'b'
                }
            ]
            
            for q_data in questions:
                question = Question(
                    test_id=test.id,
                    question_text=q_data['question'],
                    option_a=q_data['options'][0],
                    option_b=q_data['options'][1],
                    option_c=q_data['options'][2],
                    option_d=q_data['options'][3],
                    correct_answer=q_data['correct']
                )
                db.session.add(question)
        
        db.session.commit()

# Authentication
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_teacher'] = user.is_teacher
            session['is_admin'] = user.is_admin
            flash(f'Xush kelibsiz, {user.first_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login yoki parol noto\'g\'ri!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        is_teacher = request.form.get('is_teacher') == 'on'
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Bu login allaqachon mavjud!', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_teacher=is_teacher
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Ro\'yxatdan o\'tish muvaffaqiyatli yakunlandi!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Tizimdan chiqdingiz!', 'info')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    subjects = Subject.query.all()
    
    if user.is_teacher:
        # Teacher dashboard
        classes = Class.query.filter_by(teacher_id=user.id).all()
        return render_template('teacher_dashboard.html', user=user, subjects=subjects, classes=classes)
    else:
        # Student dashboard
        recent_results = TestResult.query.filter_by(user_id=user.id).order_by(TestResult.completed_at.desc()).limit(5).all()
        completed_cases = CaseProgress.query.filter_by(user_id=user.id, is_correct=True).count()
        return render_template('student_dashboard.html', user=user, subjects=subjects, recent_results=recent_results, completed_cases=completed_cases)

# Subjects and Articles
@app.route('/subjects')
def subjects():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    subjects = Subject.query.all()
    return render_template('subjects.html', subjects=subjects)

@app.route('/subject/<int:subject_id>')
def subject_detail(subject_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    subject = Subject.query.get_or_404(subject_id)
    articles = Article.query.filter_by(subject_id=subject_id).all()
    return render_template('subject_detail.html', subject=subject, articles=articles)

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    article = Article.query.get_or_404(article_id)
    diagram_data = json.loads(article.diagram_data) if article.diagram_data else None
    flowchart_data = json.loads(article.flowchart_data) if article.flowchart_data else None
    timeline_data = json.loads(article.timeline_data) if article.timeline_data else None
    
    return render_template('article_detail.html', article=article, 
                         diagram_data=diagram_data, flowchart_data=flowchart_data, 
                         timeline_data=timeline_data)

# Interactive Cases
@app.route('/case/<int:case_id>')
def case_detail(case_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    case = Case.query.get_or_404(case_id)
    animation_steps = json.loads(case.animation_steps) if case.animation_steps else []
    
    # Check if user already completed this case
    progress = CaseProgress.query.filter_by(user_id=session['user_id'], case_id=case_id).first()
    
    return render_template('case_detail.html', case=case, animation_steps=animation_steps, progress=progress)

@app.route('/case/<int:case_id>/solve', methods=['POST'])
def solve_case(case_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    case = Case.query.get_or_404(case_id)
    user_answer = request.form.get('answer')
    
    is_correct = user_answer == case.correct_answer
    
    # Save progress
    progress = CaseProgress.query.filter_by(user_id=session['user_id'], case_id=case_id).first()
    if progress:
        progress.user_answer = user_answer
        progress.is_correct = is_correct
        progress.attempts += 1
        progress.completed_at = datetime.utcnow()
    else:
        progress = CaseProgress(
            user_id=session['user_id'],
            case_id=case_id,
            user_answer=user_answer,
            is_correct=is_correct
        )
        db.session.add(progress)
    
    db.session.commit()
    
    return render_template('case_result.html', case=case, user_answer=user_answer, is_correct=is_correct)

# Tests
@app.route('/tests')
def tests():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if user.is_teacher:
        tests = Test.query.all()
        return render_template('teacher_tests.html', tests=tests)
    else:
        tests = Test.query.filter_by(is_active=True).all()
        return render_template('student_tests.html', tests=tests)

@app.route('/test/<int:test_id>')
def test_detail(test_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    test = Test.query.get_or_404(test_id)
    questions = Question.query.filter_by(test_id=test_id).all()
    
    return render_template('test_detail.html', test=test, questions=questions)

@app.route('/test/<int:test_id>/take', methods=['GET', 'POST'])
def take_test(test_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    test = Test.query.get_or_404(test_id)
    questions = Question.query.filter_by(test_id=test_id).all()
    
    if request.method == 'POST':
        score = 0
        total_points = sum(q.points for q in questions)
        
        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer == question.correct_answer:
                score += question.points
        
        percentage = (score / total_points) * 100 if total_points > 0 else 0
        
        # Save result
        result = TestResult(
            user_id=session['user_id'],
            test_id=test_id,
            score=score,
            total_points=total_points,
            percentage=percentage
        )
        db.session.add(result)
        db.session.commit()
        
        flash(f'Test yakunlandi! Natijangiz: {score}/{total_points} ({percentage:.1f}%)', 'success')
        return redirect(url_for('test_result', test_id=test_id, result_id=result.id))
    
    return render_template('take_test.html', test=test, questions=questions)

@app.route('/test/<int:test_id>/result/<int:result_id>')
def test_result(test_id, result_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    test = Test.query.get_or_404(test_id)
    result = TestResult.query.get_or_404(result_id)
    
    return render_template('test_result.html', test=test, result=result)

# Teacher Panel
@app.route('/teacher/classes')
def teacher_classes():
    if 'user_id' not in session or not session.get('is_teacher'):
        return redirect(url_for('login'))
    
    classes = Class.query.filter_by(teacher_id=session['user_id']).all()
    return render_template('teacher_classes.html', classes=classes)

@app.route('/teacher/create_class', methods=['GET', 'POST'])
def create_class():
    if 'user_id' not in session or not session.get('is_teacher'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # Generate unique join code
        import random
        import string
        join_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        while Class.query.filter_by(join_code=join_code).first():
            join_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        new_class = Class(
            name=name,
            description=description,
            teacher_id=session['user_id'],
            join_code=join_code
        )
        db.session.add(new_class)
        db.session.commit()
        
        flash(f'Sinf muvaffaqiyatli yaratildi! Qo\'shilish kodi: {join_code}', 'success')
        return redirect(url_for('teacher_classes'))
    
    return render_template('create_class.html')

@app.route('/join_class', methods=['GET', 'POST'])
def join_class():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        join_code = request.form.get('join_code')
        
        class_obj = Class.query.filter_by(join_code=join_code).first()
        if not class_obj:
            flash('Noto\'g\'ri qo\'shilish kodi!', 'error')
            return render_template('join_class.html')
        
        # Check if already joined
        existing = ClassStudent.query.filter_by(class_id=class_obj.id, student_id=session['user_id']).first()
        if existing:
            flash('Siz allaqachon ushbu sinfga qo\'shilgansiz!', 'info')
            return redirect(url_for('dashboard'))
        
        # Join class
        class_student = ClassStudent(
            class_id=class_obj.id,
            student_id=session['user_id']
        )
        db.session.add(class_student)
        db.session.commit()
        
        flash(f'"{class_obj.name}" sinfiga muvaffaqiyatli qo\'shildingiz!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('join_class.html')

# Legal Map
@app.route('/legal-map')
def legal_map():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    subjects = Subject.query.all()
    articles = Article.query.all()
    related_articles = RelatedArticle.query.all()
    
    # Build map data
    map_data = {
        'subjects': [{'id': s.id, 'name': s.name, 'color': s.color} for s in subjects],
        'articles': [{'id': a.id, 'number': a.number, 'title': a.title, 'subject_id': a.subject_id} for a in articles],
        'connections': [{'from': ra.article_id, 'to': ra.related_article_id, 'type': ra.relationship_type} for ra in related_articles]
    }
    
    return render_template('legal_map.html', map_data=map_data)

# API endpoints for AJAX
@app.route('/api/case/<int:case_id>/animation')
def get_case_animation(case_id):
    case = Case.query.get_or_404(case_id)
    animation_steps = json.loads(case.animation_steps) if case.animation_steps else []
    return jsonify(animation_steps)

@app.route('/api/article/<int:article_id>/diagram')
def get_article_diagram(article_id):
    article = Article.query.get_or_404(article_id)
    diagram_data = json.loads(article.diagram_data) if article.diagram_data else {}
    return jsonify(diagram_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)

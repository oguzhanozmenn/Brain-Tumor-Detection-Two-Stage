import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# --- BİZİM YAZDIĞIMIZ YAPAY ZEKA VE PDF MODÜLLERİ ---
from utils.image_processor import analyze_image
from utils.pdf_generator import create_pdf

app = Flask(__name__)

# --- AYARLAR ---
app.config['SECRET_KEY'] = 'bu-cok-gizli-bir-anahtardir-kimseyle-paylasma'  # Güvenlik anahtarı
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasev3.db'  # Veritabanı dosyası
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Klasörlerin varlığını garantiye al
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/results', exist_ok=True)
os.makedirs('static/reports', exist_ok=True)

# --- VERİTABANI & LOGIN KURULUMU ---
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Giriş yapılmamışsa buraya atar


# --- VERİTABANI MODELLERİ (TABLOLAR) ---

# 1. Kullanıcı Tablosu
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Yönetici mi?
    reports = db.relationship('Report', backref='owner', lazy=True)  # Kullanıcının raporları


# 2. Rapor (Analiz) Tablosu
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    original_path = db.Column(db.String(300))
    processed_path = db.Column(db.String(300))
    pdf_path = db.Column(db.String(300))
    risk_score = db.Column(db.Float)
    risk_label = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Hangi kullanıcıya ait?


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- ROTALAR (SAYFALAR) ---

# Ana Sayfa (Login zorunlu)
@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)


# Kayıt Ol Sayfası
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Kullanıcı adı dolu mu?
        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten alınmış. Lütfen başka bir tane seçin.', 'danger')
            return redirect(url_for('register'))

        # Eğer kullanıcı adı "admin" ise otomatik yönetici yap
        is_admin_user = (username.lower() == 'admin')

        # Şifreyi şifrele ve kaydet
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, is_admin=is_admin_user)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('index'))

    return render_template('register.html')


# Giriş Yap Sayfası
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')

    return render_template('login.html')


# Çıkış Yap
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Kullanıcı Dashboard (Kendi Geçmişi)
@app.route('/dashboard')
@login_required
def dashboard():
    # Sadece giriş yapan kullanıcının raporlarını getir
    user_reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.date.desc()).all()
    return render_template('dashboard.html', reports=user_reports)


# --- YÖNETİCİ PANELİ (GÜNCELLENDİ) ---
@app.route('/admin')
@login_required
def admin_panel():
    # Güvenlik Kontrolü: Sadece adminler girebilir
    if not current_user.is_admin:
        return "<h1>⛔ Yetkisiz Giriş! Bu alana sadece yöneticiler girebilir.</h1><a href='/'>Geri Dön</a>", 403

    # 1. Tüm Kullanıcıları Çek
    all_users = User.query.all()

    # 2. Tüm Raporları Çek (En yeniden eskiye)
    all_reports = Report.query.order_by(Report.date.desc()).all()

    # İstatistikler için sayıları hesapla (HTML içinde len() ile de yapılabilir ama burası daha temiz)
    total_users = len(all_users)
    total_scans = len(all_reports)

    return render_template('admin_dashboard.html', users=all_users, reports=all_reports, total_users=total_users,
                           total_scans=total_scans)


# --- ANALİZ FONKSİYONU ---
@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    if 'file' not in request.files: return redirect(request.url)
    file = request.files['file']
    if file.filename == '': return redirect(request.url)

    if file:
        # Dosya ismini güvenli hale getir
        unique_filename = str(uuid.uuid4()) + "_" + file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # 1. AI Modeli Çalıştır
        result = analyze_image(filepath)

        if result['success']:
            # 2. PDF Raporu Oluştur
            pdf_filename = f"report_{unique_filename}.pdf"
            pdf_path = create_pdf(result, output_filename=pdf_filename)
            result['pdf_path'] = pdf_path

            # 3. Veritabanına Kaydet
            new_report = Report(
                original_path=filepath,
                processed_path=result['processed_path'],
                pdf_path=pdf_path,
                risk_score=result['risk_score'],
                risk_label=result['risk_label'],
                user_id=current_user.id  # Şu anki kullanıcıya bağla
            )
            db.session.add(new_report)
            db.session.commit()

            return render_template('result.html', result=result)
        else:
            # Hata varsa (Örn: MR değilse)
            return f"""
            <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
                <h1 style="color:red;">⚠️ Analiz Reddedildi</h1>
                <h3>{result['message']}</h3>
                <br>
                <a href="/" style="padding:10px 20px; background:#007bff; color:white; text-decoration:none; border-radius:5px;">Geri Dön</a>
            </div>
            """


if __name__ == '__main__':
    # Veritabanı tablolarını oluştur (Yoksa)
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5002)
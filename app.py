from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import db, User, get_user_by_username, Participant

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DBとLoginManagerの初期化
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ユーザー読み込み関数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ログインルート
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        return 'ログイン失敗'
    return render_template('login.html')

# ログイン後のトップページ
@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.username)

# ✅ 修正済み：ログアウトルート
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 出席管理ページ
@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    if request.method == 'POST':
        position = request.form.get('position')
        name = request.form.get('name')
        status = request.form.get('status')

        participant = Participant.query.filter_by(name=name).first()
        if participant:
            participant.position = position
            participant.status = status
        else:
            participant = Participant(position=position, name=name, status=status)
            db.session.add(participant)

        db.session.commit()
        return redirect(url_for('attendance'))

    participants = Participant.query.all()
    return render_template('attendance.html', username=current_user.username, participants=participants)

# 管理者用ダッシュボード（未使用モデル Attendance に注意）
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    # attendances = Attendance.query.all()  # モデルが未定義のためコメントアウト
    # return render_template('admin_dashboard.html', attendances=attendances)
    return "管理者ページ（未実装）"

# アプリ起動時にDB作成（ローカル開発用）
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

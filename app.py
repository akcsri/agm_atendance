from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ユーザーモデル
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# 出欠モデル
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    investor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100))
    name = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        return 'ログイン失敗'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    if current_user.is_admin:
        records = Attendance.query.all()
    else:
        records = Attendance.query.filter_by(investor_id=current_user.id).all()
    return render_template('index.html', data=records)

@app.route('/register', methods=['POST'])
@login_required
def register():
    status = request.form['status']
    title = request.form.get('title', '')
    name = request.form.get('name', '')
    attendance = Attendance(
        investor_id=current_user.id,
        status=status,
        title=title if status == '出席' else '',
        name=name if status == '出席' else ''
    )
    db.session.add(attendance)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    attendance = Attendance.query.get_or_404(id)
    if not current_user.is_admin and attendance.investor_id != current_user.id:
        return "アクセス拒否", 403
    if request.method == 'POST':
        attendance.status = request.form['status']
        attendance.title = request.form.get('title', '')
        attendance.name = request.form.get('name', '')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', attendance=attendance)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

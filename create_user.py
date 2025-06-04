
from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        user = User(username='admin', password_hash=generate_password_hash('admin123'))
        db.session.add(user)
        db.session.commit()
        print("初期ユーザー admin を作成しました")
    else:
        print("admin ユーザーはすでに存在します")

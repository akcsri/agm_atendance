from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    # 参加者とのリレーション
    participants = db.relationship('Participant', backref='user', lazy=True)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100))
    name = db.Column(db.String(100))
    status = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所有者ユーザー

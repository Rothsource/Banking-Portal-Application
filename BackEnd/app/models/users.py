# app/models/user.py
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)        
    email = db.Column(db.String(255), nullable=False)           
    password_hash = db.Column(db.String(255), nullable=False)   
    otp = db.Column(db.String(255), nullable=True)              # varchar, nullable
    gov_id = db.Column(db.String(255), nullable=True)
    bank_id = db.Column(db.String(255), nullable=True)
    user_type = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    digits = db.Column(db.String(50), nullable=False)

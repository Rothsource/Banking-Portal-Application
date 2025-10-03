# app/services/user_service.py
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime
import secrets

def generate_otp():
    return str(secrets.randbelow(10**8)).zfill(8)


def create_otp(id):
    user = User.query.get(id)
    if not user:
        return None, "User not found"

    otp = generate_otp()
    user.otp = otp

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}"

    return otp, None

def verify_otp(id, entered_otp):
    user = User.query.get(id)
    if not user:
        return False, "User not found"

    if user.otp != entered_otp:
        return False, "Invalid OTP"

    user.otp = None 

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"

    return True, None



def create_user(username, email, password, user_type, digits, gov_id):

    existing_user = User.query.filter(
        (User.email == email) | (User.gov_id == gov_id)
    ).first()
    
    if not user_type:
        user_type = "customer"
        

    if existing_user:
        if existing_user.username == username:
            return None, "User already exists"

    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password), 
        gov_id=gov_id,
        user_type=user_type,
        digits=digits,
        created_at=datetime.utcnow(),
        is_active=True
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}"

    return new_user, None

def user_login(gov_id, gmail, password):
    user = User.query.filter(
        (User.gov_id == gov_id) & (User.email == gmail)
    ).first()
    
    if not user:
        return None, "User not found", None, None

    if not user.is_active:
        return None, "User is inactive", None, None

    if not check_password_hash(user.password_hash, password):
        return None, "Invalid password", None, None

    otp = None
    if user.user_type != 'customer':
        otp, err = create_otp(user.id)
        if err:
            return None, err, None, None
        db.session.refresh(user)

    try:
        user.last_login = datetime.utcnow()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}", None, None

    return user, None, user.user_type, otp
# app/routers/user.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.controller import create_user, user_login
import random

def generate_otp():
    otp = random.randint(10000000, 99999999)
    return otp

bp = Blueprint("user", __name__, template_folder="../../Fronend/templetes")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        digits = request.form.get("digits")
        gov_id = request.form.get("gov_id")
        user_type = request.form.get("user_type")  # optional

        user, error = create_user(username, email, password, user_type, digits, gov_id)
        if error:
            return f"Error: {error}"  
        return "User created successfully!"

    return render_template("register.html")

@bp.route("/registerothers", methods=["GET", "POST"])
def register_others():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        digits = request.form.get("digits")
        gov_id = request.form.get("gov_id")
        user_type = request.form.get("user_type")  # optional

        user, error = create_user(username, email, password, user_type, digits, gov_id)
        if error:
            return f"Error: {error}"  
        return "User created successfully!"

    return render_template("othersRegister.html")

@bp.route("/otp", methods=["GET", "POST"])
def otp():
    if request.method == "POST":
        entered_otp = request.form.get("otp")
        # Here you would verify the OTP with the one stored/sent
        # For simplicity, let's assume it's always correct
        return "OTP verified successfully!"
    return render_template("otp.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        gov_id = request.form.get("gov_id")
        gmail = request.form.get("email")   
        password = request.form.get("password")
        
        user, error,role = user_login(gov_id, gmail, password)
        if role != "customer":
            return redirect(url_for("user.otp"))
        
        if error:
            return f"Error: {error}"
        return "Login successful!"
    return render_template("login.html")

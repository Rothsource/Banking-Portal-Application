# app/routers/user.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.controller import create_user, user_login, verify_otp

bp = Blueprint("user", __name__, template_folder="../../Fronend/templetes")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        digits = request.form.get("digits")
        gov_id = request.form.get("gov_id")
        user_type = request.form.get("user_type")

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
        user_type = request.form.get("user_type")

        user, error = create_user(username, email, password, user_type, digits, gov_id)
        if error:
            return f"Error: {error}"  
        return "User created successfully!"

    return render_template("othersRegister.html")

@bp.route("/otp/<int:user_id>", methods=["GET", "POST"]) 
def otp(user_id):
    if request.method == "POST":
        entered_otp = request.form.get("otp")
        valid, error = verify_otp(user_id, entered_otp)
        if not valid:
            return f"Error: {error}"
        
        return "OTP verified successfully! You are now logged in."
    
    return render_template("otp.html", user_id=user_id)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        gov_id = request.form.get("gov_id")
        email = request.form.get("gmail")   
        password = request.form.get("password")
        
        # Fixed: unpack all 4 return values
        user, error, role, otp = user_login(gov_id, email, password)
        if error:
            return f"Error: {error}"
        
        if role != "customer":
            print(f"OTP for user {user.id}: {otp}")  
            
            return redirect(url_for("user.otp", user_id=user.id))
        
        return "Login successful!"
    
    return render_template("login.html")
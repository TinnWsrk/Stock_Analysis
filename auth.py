from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    success_message = None
    if session.pop('register_success', None):
        success_message = "Account created successfully. You can now log in."

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        #1. Look up user by email
        user = User.query.filter_by(email=email).first()

        #2. Check if user exists and password correct
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['user_email'] = user.email  
            return redirect(url_for('main'))
        else:
            return render_template("login.html", error="Invalid email or password.")

    return render_template("login.html", success=success_message)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            return render_template("register.html", error="Passwords do not match.")

        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("register.html", error="Email already registered.")

        # Hash password before saving
        hashed_password = generate_password_hash(password)

        # Create new user and add to database
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session['register_success'] = True
        return redirect(url_for('auth.login'))

        return redirect(url_for('auth.login'))

    return render_template("register.html")


#@auth.route('/logout')
#def logout():
    #session.pop('logged_in', None)
    #return redirect(url_for('auth.login'))

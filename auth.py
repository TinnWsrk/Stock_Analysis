from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Dummy-Login (with real DB later)
        if email == "admin" and password == "1234":
            session['logged_in'] = True
            return redirect(url_for('main'))
        else:
            return render_template("login.html", error = "user name or password is incorrect!")
    return render_template("login.html")

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

        return redirect(url_for('auth.login'))

    return render_template("register.html")


#@auth.route('/logout')
#def logout():
    #session.pop('logged_in', None)
    #return redirect(url_for('auth.login'))

from flask import Blueprint, render_template, request, redirect, url_for, session

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Dummy-Login (with real DB later)
        if email == "admin" and password == "1234":
            session['logged_in'] = True
            return redirect(url_for('main'))
        else:
            return render_template("login.html", error = "login failed!")
    return render_template("login.html")

#@auth.route('/logout')
#def logout():
    #session.pop('logged_in', None)
    #return redirect(url_for('auth.login'))

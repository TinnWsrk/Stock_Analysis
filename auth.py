from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email == "admin@test.de" and password == "pass123":
            return "Login erfolgreich!"
        return "Login fehlgeschlagen!"
    return render_template("login.html")

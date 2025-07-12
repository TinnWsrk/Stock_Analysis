from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User

from auth import auth                         # Login-Blueprint
from csv_logic import process_csv             # CSV-Verarbeitung
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supergeheimespasswort123"   # Für Sessions nötig
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)
with app.app_context():
    db.create_all()

# Blueprint registrieren
app.register_blueprint(auth)

# Standard-Route: Weiterleitung zu /login
@app.route("/")
def home():
    return redirect(url_for('auth.login'))

# Geschützte Hauptseite für Upload und Graph
@app.route("/main", methods=["GET", "POST"])
def main():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    user_email = session.get('user_email') #get email
    graph_html = None

    if request.method == "POST":
        file = request.files["csvfile"]
        if file:
            graph_html = process_csv(file, app.config['UPLOAD_FOLDER'])
    return render_template("index.html", graph_html=graph_html, user_email=user_email)

#Add temporarily for debug
@app.route("/debug-users")
def debug_users():
   users = User.query.all()
   return "<br>".join([f"{u.id}: {u.email} | {u.password}" for u in users])


# Projekt starten
if __name__ == "__main__":
    # Sicherstellen, dass Upload-Ordner existiert
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from auth import auth                         # Login-Blueprint
from csv_logic import process_csv             # CSV-Verarbeitung
import os

app = Flask(__name__)
app.secret_key = "supergeheimespasswort123"   # Für Sessions nötig
app.config['UPLOAD_FOLDER'] = 'uploads'

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

    graph_html = None
    if request.method == "POST":
        file = request.files["csvfile"]
        if file:
            graph_html = process_csv(file, app.config['UPLOAD_FOLDER'])
    return render_template("index.html", graph_html=graph_html)

# Projekt starten
if __name__ == "__main__":
    # Sicherstellen, dass Upload-Ordner existiert
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)



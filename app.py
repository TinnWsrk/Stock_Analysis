from flask import Flask, render_template, request
from auth import auth
from csv_logic import process_csv    # 👈 Importiere CSV-Logik
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Blueprint registrieren
app.register_blueprint(auth)

@app.route("/", methods=["GET", "POST"])
def index():
    graph_html = None
    if request.method == "POST":
        file = request.files["csvfile"]
        if file:
            graph_html = process_csv(file, app.config['UPLOAD_FOLDER'])
    return render_template("index.html", graph_html=graph_html)

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)


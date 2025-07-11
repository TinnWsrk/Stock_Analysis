from flask import Flask, render_template, request, redirect, url_for, session
from auth import auth
from yahoo_logic import fetch_stock_plot   # <-- NEU: Import der Logik
import os

app = Flask(__name__)
app.secret_key = "supergeheimespasswort123"
app.register_blueprint(auth)

@app.route("/")
def home():
    return redirect(url_for('auth.login'))

@app.route("/main", methods=["GET", "POST"])
def main():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    graph_html = None
    if request.method == "POST":
        ticker = request.form.get("ticker")
        if ticker:
            graph_html = fetch_stock_plot(ticker)

    return render_template("index.html", graph_html=graph_html)


if __name__ == "__main__":
    app.run(debug=True)
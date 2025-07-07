from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/", methods=["GET", "POST"])
def index():
    graph_html = None
    if request.method == "POST":
        file = request.files["csvfile"]
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            df = pd.read_csv(filepath, parse_dates=["Date"])
            df.sort_values("Date", inplace=True)

            fig = px.line(df, x="Date", y="Close", title="Kursentwicklung")
            graph_html = fig.to_html(full_html=False)

    return render_template("index.html", graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)

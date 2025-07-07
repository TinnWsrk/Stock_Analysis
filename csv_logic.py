import pandas as pd
import plotly.express as px
import os

def process_csv(file, upload_folder):
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath, parse_dates=["Date"])
    df.sort_values("Date", inplace=True)

    fig = px.line(df, x="Date", y="Close", title="Kursentwicklung (Close)")
    return fig.to_html(full_html=False)

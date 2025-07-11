# yahoo_logic.py
import yfinance as yf
import plotly.express as px

def fetch_stock_plot(ticker: str, period="6mo", interval="1d"):
    """
    Holt historische Kursdaten von Yahoo Finance und gibt ein HTML-Plot zurück.
    """
    df = yf.download(ticker, period=period, interval=interval)

    if df.empty:
        return "<p>Keine Daten gefunden. Bitte überprüfe das Ticker-Symbol.</p>"

    fig = px.line(df, x=df.index, y="Close", title=f"{ticker.upper()} Kursentwicklung")
    return fig.to_html(full_html=False)

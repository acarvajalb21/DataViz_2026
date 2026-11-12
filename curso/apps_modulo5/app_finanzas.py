"""Finance Explorer: velas y bandas de Bollinger del módulo 5."""

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, dcc, html

from comun import crear_app, ejecutar, leer_datos

df = leer_datos("dash-stock-ticker-demo.csv", ["Stock", "Date", "Open", "High", "Low", "Close"])
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(["Stock", "Date"])
TICKERS = sorted(df.Stock.unique())
app = crear_app(__name__, "Finance Explorer")
server = app.server
app.layout = html.Main(
    [
        html.P("MÓDULO 5 · PRECIOS DE ACCIONES Y BANDAS DE BOLLINGER", className="eyebrow"),
        html.H1("Finance Explorer"),
        html.Section(
            [
                html.Label("Selecciona una o varias acciones", htmlFor="stock-ticker-input"),
                dcc.Dropdown(id="stock-ticker-input", options=TICKERS, value=["YHOO", "GOOGL"], multi=True),
                html.Div(id="graphs"),
            ],
            className="panel",
        ),
    ],
    className="container",
)


def bbands(precios, window_size=10, num_of_std=5):
    # Parámetros del profesor: 10 observaciones y 5 desviaciones estándar.
    media = precios.rolling(window=window_size).mean()
    desviacion = precios.rolling(window=window_size).std()
    return media, media + num_of_std * desviacion, media - num_of_std * desviacion


@app.callback(Output("graphs", "children"), Input("stock-ticker-input", "value"))
def update_graph(tickers):
    if not tickers:
        return html.P("Selecciona una acción para ver su gráfico.")
    graficos = []
    for ticker in tickers:
        datos = df[df.Stock == ticker]
        if datos.empty:
            continue
        figura = go.Figure(
            go.Candlestick(
                x=datos.Date, open=datos.Open, high=datos.High, low=datos.Low,
                close=datos.Close, name=ticker,
                increasing_line_color="#1f78b4", decreasing_line_color="#a6cee3",
            )
        )
        for valores, nombre, color in zip(
            bbands(datos.Close),
            ["Media móvil", "Banda superior", "Banda inferior"],
            ["#2563eb", "#ea580c", "#16a34a"],
        ):
            figura.add_trace(go.Scatter(x=datos.Date, y=valores, mode="lines", name=nombre, line=dict(width=1, color=color)))
        figura.update_layout(title=ticker, template="plotly_white", height=440, margin=dict(l=50, r=20, t=50, b=20))
        graficos.append(dcc.Graph(id=f"accion-{ticker}", figure=figura))
    return graficos


if __name__ == "__main__":
    ejecutar(app)

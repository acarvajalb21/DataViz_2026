"""Dashboard de predicción de crédito del módulo 5."""

from pathlib import Path
import math

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html


APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "data_banco_creditos.csv"
MODEL_PATH = APP_DIR / "modelo_credito.pkl"

df = pd.read_csv(DATA_PATH)
modelo = joblib.load(MODEL_PATH)

# El modelo usa exactamente esta columna, con el mismo nombre que en el entrenamiento.
tiempos = np.linspace(
    df["tiempo_analisis_min"].min(),
    df["tiempo_analisis_min"].max(),
    100,
)
tiempos_df = pd.DataFrame({"tiempo_analisis_min": tiempos})
predicciones_linea = modelo.predict(tiempos_df)

fig = px.scatter(
    df,
    x="tiempo_analisis_min",
    y="monto_credito_millones",
    labels={
        "tiempo_analisis_min": "Tiempo de análisis (min)",
        "monto_credito_millones": "Monto de crédito (millones)",
    },
    template="plotly_white",
)
fig.update_traces(
    name="Créditos observados",
    showlegend=True,
    marker={"size": 10, "color": "#2563eb", "opacity": 0.78},
)
fig.add_trace(
    go.Scatter(
        x=tiempos,
        y=predicciones_linea,
        mode="lines",
        name="Regresión lineal",
        line={"color": "#f97316", "width": 3},
    )
)
fig.update_layout(
    margin={"l": 25, "r": 25, "t": 35, "b": 25},
    legend={"orientation": "h", "y": 1.12, "x": 0},
    hovermode="closest",
)

app = Dash(__name__, title="Predicción de crédito")
app.layout = html.Main(
    className="page",
    children=[
        html.Header(
            className="page-header",
            children=[
                html.P("MÓDULO 5 · DASH", className="eyebrow"),
                html.H1("Predicción de monto de crédito"),
                html.P(
                    "Modelo de regresión lineal basado en el tiempo de análisis.",
                    className="subtitle",
                ),
            ],
        ),
        html.Div(
            className="dashboard-grid",
            children=[
                html.Section(
                    className="card chart-card",
                    children=[
                        html.H2("Datos y recta de regresión"),
                        html.P(
                            "Cada punto representa un crédito observado.",
                            className="muted",
                        ),
                        dcc.Graph(id="grafico-regresion", figure=fig, config={"displaylogo": False}),
                    ],
                ),
                html.Section(
                    className="card prediction-card",
                    children=[
                        html.H2("Haz una predicción"),
                        html.Label(
                            "Tiempo de análisis (minutos)",
                            htmlFor="input-tiempo-analisis",
                        ),
                        dcc.Input(
                            id="input-tiempo-analisis",
                            type="number",
                            min=0,
                            step="any",
                            placeholder="Por ejemplo: 45",
                        ),
                        html.Div(
                            id="output-prediccion",
                            className="prediction-result",
                            role="status",
                        ),
                        html.P(
                            "La estimación es una demostración académica del modelo.",
                            className="muted note",
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("output-prediccion", "children"),
    Input("input-tiempo-analisis", "value"),
)
def predecir_credito(tiempo_analisis):
    if tiempo_analisis is None:
        return "Ingresa un tiempo para obtener la predicción."
    if not isinstance(tiempo_analisis, (int, float)) or not math.isfinite(tiempo_analisis):
        return "Ingresa un número válido."
    if tiempo_analisis < 0:
        return "El tiempo no puede ser negativo."

    entrada = pd.DataFrame({"tiempo_analisis_min": [tiempo_analisis]})
    prediccion = modelo.predict(entrada)[0]
    return f"Monto estimado: {prediccion:.2f} millones"


if __name__ == "__main__":
    app.run(debug=True)

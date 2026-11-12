"""Aplicación principal: último dashboard del módulo, predicción de créditos."""

import math

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, dcc, html

from comun import crear_app, ejecutar, leer_datos
from entrenar_modelo import cargar_modelo

df = leer_datos(
    "data_banco_creditos.csv", ["tiempo_analisis_min", "monto_credito_millones"]
)
modelo = cargar_modelo()
x_linea = np.linspace(df.tiempo_analisis_min.min(), df.tiempo_analisis_min.max(), 100)
y_linea = modelo.predict(pd.DataFrame({"tiempo_analisis_min": x_linea}))

fig = px.scatter(
    df,
    x="tiempo_analisis_min",
    y="monto_credito_millones",
    title="Relación entre tiempo de análisis y monto del crédito",
    labels={
        "tiempo_analisis_min": "Tiempo de análisis (min)",
        "monto_credito_millones": "Monto de crédito (millones)",
    },
    template="plotly_white",
    color_discrete_sequence=["#2563eb"],
)
fig.add_trace(
    go.Scatter(x=x_linea, y=y_linea, mode="lines", name="Regresión lineal", line_color="#ea580c")
)
fig.update_layout(margin=dict(l=30, r=25, t=65, b=30), height=510)

app = crear_app(__name__, "Predicción de monto de crédito")
server = app.server
app.layout = html.Main(
    [
        html.Header(
            [
                html.P("MÓDULO 5 · DASH CON MODELO DE PREDICCIÓN", className="eyebrow"),
                html.H1("Predicción de monto de crédito con regresión lineal"),
            ]
        ),
        html.Div(
            [
                html.Section(dcc.Graph(id="grafico-regresion", figure=fig), className="panel"),
                html.Section(
                    [
                        html.H2("Haz una predicción"),
                        html.Label("Tiempo de análisis (minutos)", htmlFor="input-tiempo-analisis"),
                        dcc.Input(
                            id="input-tiempo-analisis",
                            type="number",
                            min=0,
                            step="any",
                            placeholder="Por ejemplo, 45",
                            debounce=False,
                            className="number-input",
                        ),
                        html.Div(id="output-prediccion", className="prediction", **{"aria-live": "polite"}),
                        html.P("Ejemplo académico con los datos y el modelo del módulo.", className="muted"),
                    ],
                    className="panel prediction-panel",
                ),
            ],
            className="two-columns",
        ),
    ],
    className="container",
)


@app.callback(Output("output-prediccion", "children"), Input("input-tiempo-analisis", "value"))
def predecir_credito(tiempo_analisis):
    if tiempo_analisis is None:
        return "Ingresa un tiempo para obtener la predicción."
    if not isinstance(tiempo_analisis, (int, float)) or not math.isfinite(tiempo_analisis) or tiempo_analisis < 0:
        return "Ingresa un número válido mayor o igual a cero."
    entrada = pd.DataFrame({"tiempo_analisis_min": [tiempo_analisis]})
    prediccion = float(modelo.predict(entrada)[0])
    return f"Predicción del monto de crédito: {prediccion:.2f} millones"


if __name__ == "__main__":
    ejecutar(app)

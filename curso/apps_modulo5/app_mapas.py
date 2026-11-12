"""Aplicación independiente de mapas de abejas del módulo 5."""

import plotly.express as px
from dash import Input, Output, dcc, html

from comun import crear_app, ejecutar, leer_datos

agrupacion = ["State", "ANSI", "Affected by", "Year", "state_code"]
df = leer_datos("intro_bees.csv", agrupacion + ["Pct of Colonies Impacted"])
df = df.groupby(agrupacion, as_index=False)[["Pct of Colonies Impacted"]].mean()
# Se mantienen los cuatro años y el filtro Varroa_mites del ejemplo final.
ANIOS = [2015, 2016, 2017, 2018]
app = crear_app(__name__, "Mapa de colonias de abejas")
server = app.server
app.layout = html.Main(
    [
        html.P("MÓDULO 5 · DASH APP PARA MAPAS", className="eyebrow"),
        html.H1("Desarrollo de Dashboards Web con Dash"),
        html.Section(
            [
                html.Label("Año", htmlFor="slct_year"),
                dcc.Dropdown(id="slct_year", options=ANIOS, value=2015, clearable=False),
                html.P(id="output_container"),
                dcc.Graph(id="my_bee_map"),
            ],
            className="panel",
        ),
    ],
    className="container",
)


@app.callback(Output("output_container", "children"), Output("my_bee_map", "figure"), Input("slct_year", "value"))
def update_graph(anio):
    datos = df[(df.Year == anio) & (df["Affected by"] == "Varroa_mites")]
    figura = px.choropleth(
        datos,
        locations="state_code",
        locationmode="USA-states",
        scope="usa",
        color="Pct of Colonies Impacted",
        hover_name="State",
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={"Pct of Colonies Impacted": "% de colonias afectadas"},
        template="plotly_dark",
    )
    figura.update_layout(height=580, margin=dict(l=0, r=0, t=30, b=0))
    return f"El año seleccionado por el usuario fue: {anio}", figura


if __name__ == "__main__":
    ejecutar(app)

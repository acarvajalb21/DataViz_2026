# --------------------------------------------------
# IMPORTAR LIBRERÍAS
# --------------------------------------------------

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# CARGAR Y PREPARAR LOS DATOS
# --------------------------------------------------

url = (
    "https://raw.githubusercontent.com/cdeoroaguado/Datos/"
    "refs/heads/main/dataviz/country_indicators.csv"
)

df = pd.read_csv(url)

# Convertir columnas
df["Year"] = df["Year"].astype(int)
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

# Eliminar registros incompletos
df = df.dropna(
    subset=[
        "Country Name",
        "Indicator Name",
        "Year",
        "Value",
    ]
)

# Indicadores y años disponibles
available_indicators = sorted(
    df["Indicator Name"].unique().tolist()
)

available_years = sorted(
    df["Year"].unique().tolist()
)


# --------------------------------------------------
# CREAR LA APLICACIÓN
# --------------------------------------------------

app = dash.Dash(__name__)
app.title = "Explorador de indicadores"


# --------------------------------------------------
# ESTILOS
# --------------------------------------------------

PAGE_STYLE = {
    "backgroundColor": "#F5F7FA",
    "minHeight": "100vh",
    "fontFamily": "Inter, Segoe UI, Arial, sans-serif",
    "color": "#17202D",
}

CARD_STYLE = {
    "backgroundColor": "#FFFFFF",
    "border": "1px solid #E4E8EE",
    "borderRadius": "16px",
    "boxShadow": "0 6px 22px rgba(15, 23, 42, 0.05)",
}

CONTROL_STYLE = {
    **CARD_STYLE,
    "padding": "20px",
}

LABEL_STYLE = {
    "display": "block",
    "marginBottom": "9px",
    "fontSize": "11px",
    "fontWeight": "700",
    "letterSpacing": "1px",
    "color": "#8993A1",
}


# --------------------------------------------------
# FUNCIÓN PARA CREAR CONTROL DE INDICADOR
# --------------------------------------------------

def create_indicator_control(
    axis_letter,
    axis_description,
    dropdown_id,
    radio_id,
    default_indicator,
    background_color,
    text_color,
):

    return html.Div(

        style=CONTROL_STYLE,

        children=[

            html.Div(

                style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "10px",
                    "marginBottom": "17px",
                },

                children=[

                    html.Div(
                        axis_letter,
                        style={
                            "width": "31px",
                            "height": "31px",
                            "borderRadius": "8px",
                            "backgroundColor": background_color,
                            "color": text_color,
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "fontSize": "13px",
                            "fontWeight": "700",
                        },
                    ),

                    html.Div([

                        html.P(
                            f"EJE {axis_description.upper()}",
                            style={
                                "margin": "0",
                                "fontSize": "10px",
                                "fontWeight": "700",
                                "letterSpacing": "1px",
                                "color": "#8993A1",
                            },
                        ),

                        html.H3(
                            f"Indicador del eje {axis_letter}",
                            style={
                                "margin": "3px 0 0 0",
                                "fontSize": "15px",
                                "fontWeight": "600",
                            },
                        ),
                    ]),
                ],
            ),

            html.Label(
                "SELECCIONAR INDICADOR",
                style=LABEL_STYLE,
            ),

            dcc.Dropdown(
                id=dropdown_id,

                options=[
                    {
                        "label": indicator,
                        "value": indicator,
                    }
                    for indicator in available_indicators
                ],

                value=default_indicator,
                clearable=False,
                searchable=True,

                style={
                    "fontSize": "13px",
                    "marginBottom": "17px",
                },
            ),

            dcc.RadioItems(
                id=radio_id,

                options=[
                    {
                        "label": " Lineal",
                        "value": "Linear",
                    },
                    {
                        "label": " Logarítmica",
                        "value": "Log",
                    },
                ],

                value="Linear",
                inline=True,

                labelStyle={
                    "marginRight": "24px",
                    "fontSize": "13px",
                    "color": "#586474",
                    "cursor": "pointer",
                },

                inputStyle={
                    "marginRight": "6px",
                    "accentColor": text_color,
                },
            ),
        ],
    )


# --------------------------------------------------
# DISEÑO DE LA APLICACIÓN
# --------------------------------------------------

app.layout = html.Div(

    style=PAGE_STYLE,

    children=[

        # Encabezado
        html.Header(

            style={
                "backgroundColor": "#FFFFFF",
                "borderBottom": "1px solid #E4E8EE",
                "padding": "24px 5%",
            },

            children=[

                html.Div(

                    style={
                        "maxWidth": "1300px",
                        "margin": "0 auto",
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "gap": "20px",
                        "flexWrap": "wrap",
                    },

                    children=[

                        html.Div([

                            html.P(
                                "GLOBAL DATA EXPLORER",
                                style={
                                    "margin": "0 0 6px",
                                    "fontSize": "12px",
                                    "fontWeight": "700",
                                    "letterSpacing": "2px",
                                    "color": "#526A7E",
                                },
                            ),

                            html.H1(
                                "Indicadores mundiales",
                                style={
                                    "margin": "0",
                                    "fontSize": "30px",
                                    "fontWeight": "650",
                                    "letterSpacing": "-0.7px",
                                },
                            ),
                        ]),

                        html.Div(
                            id="year-badge",
                            style={
                                "backgroundColor": "#17202D",
                                "color": "#FFFFFF",
                                "padding": "10px 18px",
                                "borderRadius": "30px",
                                "fontSize": "14px",
                                "fontWeight": "600",
                            },
                        ),
                    ],
                )
            ],
        ),

        # Contenido
        html.Main(

            style={
                "maxWidth": "1300px",
                "margin": "0 auto",
                "padding": "34px 5% 50px",
            },

            children=[

                # Introducción
                html.Div(

                    style={
                        "marginBottom": "26px",
                    },

                    children=[

                        html.H2(
                            "Explora las relaciones entre indicadores",
                            style={
                                "margin": "0 0 8px",
                                "fontSize": "21px",
                                "fontWeight": "600",
                            },
                        ),

                        html.P(
                            "Selecciona un año y pasa el cursor sobre un país "
                            "para analizar su evolución hasta ese periodo.",
                            style={
                                "margin": "0",
                                "fontSize": "15px",
                                "lineHeight": "1.6",
                                "color": "#687486",
                            },
                        ),
                    ],
                ),

                # Controles de los ejes
                html.Div(

                    style={
                        "display": "grid",
                        "gridTemplateColumns": (
                            "repeat(auto-fit, minmax(320px, 1fr))"
                        ),
                        "gap": "18px",
                        "marginBottom": "20px",
                    },

                    children=[

                        create_indicator_control(
                            axis_letter="X",
                            axis_description="horizontal",
                            dropdown_id="crossfilter-xaxis-column",
                            radio_id="crossfilter-xaxis-type",
                            default_indicator=(
                                "Fertility rate, total "
                                "(births per woman)"
                            ),
                            background_color="#EAF1F7",
                            text_color="#315D7A",
                        ),

                        create_indicator_control(
                            axis_letter="Y",
                            axis_description="vertical",
                            dropdown_id="crossfilter-yaxis-column",
                            radio_id="crossfilter-yaxis-type",
                            default_indicator=(
                                "Life expectancy at birth, "
                                "total (years)"
                            ),
                            background_color="#F1ECE5",
                            text_color="#846746",
                        ),
                    ],
                ),

                # Tarjetas informativas
                html.Div(

                    style={
                        "display": "grid",
                        "gridTemplateColumns": (
                            "repeat(auto-fit, minmax(190px, 1fr))"
                        ),
                        "gap": "16px",
                        "marginBottom": "20px",
                    },

                    children=[

                        html.Div(

                            style={
                                **CONTROL_STYLE,
                                "padding": "17px 20px",
                            },

                            children=[

                                html.P(
                                    "PAÍSES CON INFORMACIÓN",
                                    style={
                                        "margin": "0 0 9px",
                                        "fontSize": "11px",
                                        "fontWeight": "700",
                                        "letterSpacing": "1px",
                                        "color": "#8993A1",
                                    },
                                ),

                                html.H3(
                                    id="countries-count",
                                    style={
                                        "margin": "0",
                                        "fontSize": "25px",
                                        "fontWeight": "650",
                                    },
                                ),
                            ],
                        ),

                        html.Div(

                            style={
                                **CONTROL_STYLE,
                                "padding": "17px 20px",
                            },

                            children=[

                                html.P(
                                    "PAÍS EN DETALLE",
                                    style={
                                        "margin": "0 0 9px",
                                        "fontSize": "11px",
                                        "fontWeight": "700",
                                        "letterSpacing": "1px",
                                        "color": "#8993A1",
                                    },
                                ),

                                html.H3(
                                    id="selected-country",
                                    style={
                                        "margin": "0",
                                        "fontSize": "25px",
                                        "fontWeight": "650",
                                    },
                                ),
                            ],
                        ),
                    ],
                ),

                # Visualizaciones
                html.Div(

                    style={
                        "display": "grid",
                        "gridTemplateColumns": (
                            "minmax(0, 1.25fr) "
                            "minmax(340px, 0.75fr)"
                        ),
                        "gap": "20px",
                        "alignItems": "stretch",
                    },

                    children=[

                        # Gráfico principal
                        html.Div(

                            style={
                                **CARD_STYLE,
                                "padding": "18px 20px 24px",
                            },

                            children=[

                                html.Div(

                                    style={
                                        "display": "flex",
                                        "justifyContent": "space-between",
                                        "alignItems": "center",
                                        "gap": "15px",
                                        "marginBottom": "5px",
                                    },

                                    children=[

                                        html.Div([

                                            html.H3(
                                                "Comparación entre países",
                                                style={
                                                    "margin": "0 0 5px",
                                                    "fontSize": "16px",
                                                    "fontWeight": "600",
                                                },
                                            ),

                                            html.P(
                                                "Pasa el cursor sobre un punto "
                                                "para analizar el país.",
                                                style={
                                                    "margin": "0",
                                                    "fontSize": "12px",
                                                    "color": "#8993A1",
                                                },
                                            ),
                                        ]),

                                        html.Div(
                                            "● Datos por país",
                                            style={
                                                "fontSize": "11px",
                                                "color": "#315D7A",
                                                "fontWeight": "600",
                                            },
                                        ),
                                    ],
                                ),

                                dcc.Graph(
                                    id="crossfilter-indicator-scatter",

                                    hoverData={
                                        "points": [
                                            {
                                                "customdata": ["Japan"]
                                            }
                                        ]
                                    },

                                    clear_on_unhover=False,

                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },

                                    style={
                                        "height": "525px",
                                    },
                                ),

                                # Slider
                                html.Div(

                                    style={
                                        "borderTop": "1px solid #EEF0F3",
                                        "padding": "22px 10px 3px",
                                    },

                                    children=[

                                        html.Div(

                                            style={
                                                "display": "flex",
                                                "justifyContent": (
                                                    "space-between"
                                                ),
                                                "alignItems": "center",
                                                "marginBottom": "22px",
                                            },

                                            children=[

                                                html.P(
                                                    "Periodo de análisis",
                                                    style={
                                                        "margin": "0",
                                                        "fontSize": "14px",
                                                        "fontWeight": "600",
                                                        "color": "#354052",
                                                    },
                                                ),

                                                html.Span(
                                                    id="slider-year-text",
                                                    style={
                                                        "fontSize": "12px",
                                                        "color": "#8993A1",
                                                    },
                                                ),
                                            ],
                                        ),

                                        dcc.Slider(
                                            id="crossfilter-year--slider",
                                            min=available_years[0],
                                            max=available_years[-1],
                                            value=available_years[-1],

                                            marks={
                                                int(year): {
                                                    "label": str(year),
                                                    "style": {
                                                        "fontSize": "11px",
                                                        "color": "#788394",
                                                    },
                                                }
                                                for year in available_years
                                            },

                                            step=None,

                                            tooltip={
                                                "placement": "bottom",
                                                "always_visible": False,
                                            },
                                        ),
                                    ],
                                ),
                            ],
                        ),

                        # Gráficas de la derecha
                        html.Div(

                            style={
                                "display": "grid",
                                "gridTemplateRows": "1fr 1fr",
                                "gap": "20px",
                            },

                            children=[

                                # Serie X
                                html.Div(

                                    style={
                                        **CARD_STYLE,
                                        "padding": "18px",
                                    },

                                    children=[

                                        html.H3(
                                            "Evolución del indicador X",
                                            style={
                                                "margin": "0 0 4px",
                                                "fontSize": "15px",
                                                "fontWeight": "600",
                                            },
                                        ),

                                        html.P(
                                            id="x-series-description",
                                            style={
                                                "margin": "0",
                                                "fontSize": "12px",
                                                "color": "#8993A1",
                                            },
                                        ),

                                        dcc.Graph(
                                            id="x-time-series",

                                            config={
                                                "displayModeBar": False,
                                                "responsive": True,
                                            },

                                            style={
                                                "height": "275px",
                                            },
                                        ),
                                    ],
                                ),

                                # Serie Y
                                html.Div(

                                    style={
                                        **CARD_STYLE,
                                        "padding": "18px",
                                    },

                                    children=[

                                        html.H3(
                                            "Evolución del indicador Y",
                                            style={
                                                "margin": "0 0 4px",
                                                "fontSize": "15px",
                                                "fontWeight": "600",
                                            },
                                        ),

                                        html.P(
                                            id="y-series-description",
                                            style={
                                                "margin": "0",
                                                "fontSize": "12px",
                                                "color": "#8993A1",
                                            },
                                        ),

                                        dcc.Graph(
                                            id="y-time-series",

                                            config={
                                                "displayModeBar": False,
                                                "responsive": True,
                                            },

                                            style={
                                                "height": "275px",
                                            },
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# --------------------------------------------------
# OBTENER PAÍS DESDE EL HOVER
# --------------------------------------------------

def get_country_from_hover(hover_data):

    if hover_data and hover_data.get("points"):

        custom_data = hover_data["points"][0].get(
            "customdata"
        )

        if isinstance(custom_data, list):
            return custom_data[0]

        if custom_data:
            return custom_data

    return "Japan"


# --------------------------------------------------
# CALLBACK DEL GRÁFICO PRINCIPAL
# --------------------------------------------------

@app.callback(
    Output("crossfilter-indicator-scatter", "figure"),
    Output("year-badge", "children"),
    Output("countries-count", "children"),
    Output("slider-year-text", "children"),

    Input("crossfilter-xaxis-column", "value"),
    Input("crossfilter-yaxis-column", "value"),
    Input("crossfilter-xaxis-type", "value"),
    Input("crossfilter-yaxis-type", "value"),
    Input("crossfilter-year--slider", "value"),
)
def update_scatter(
    x_indicator,
    y_indicator,
    x_scale,
    y_scale,
    selected_year,
):

    # Filtrar los datos del año
    filtered_df = df[
        (df["Year"] == selected_year)
        & (
            df["Indicator Name"].isin(
                [x_indicator, y_indicator]
            )
        )
    ]

    # Organizar indicadores por país
    comparison_df = filtered_df.pivot_table(
        index="Country Name",
        columns="Indicator Name",
        values="Value",
        aggfunc="first",
    ).reset_index()

    # Caso en que se selecciona el mismo indicador
    if x_indicator == y_indicator:
        comparison_df[y_indicator] = (
            comparison_df[x_indicator]
        )

    # Eliminar países sin ambos valores
    comparison_df = comparison_df.dropna(
        subset=[
            x_indicator,
            y_indicator,
        ]
    )

    # Eliminar valores inválidos para escala logarítmica
    if x_scale == "Log":
        comparison_df = comparison_df[
            comparison_df[x_indicator] > 0
        ]

    if y_scale == "Log":
        comparison_df = comparison_df[
            comparison_df[y_indicator] > 0
        ]

    # Crear gráfico
    figure = px.scatter(
        comparison_df,
        x=x_indicator,
        y=y_indicator,
        custom_data=["Country Name"],
    )

    figure.update_traces(
        marker={
            "size": 10,
            "color": "#315D7A",
            "opacity": 0.76,
            "line": {
                "width": 1.2,
                "color": "#FFFFFF",
            },
        },

        hovertemplate=(
            "<b>%{customdata[0]}</b><br><br>"
            + x_indicator
            + ": %{x:,.2f}<br>"
            + y_indicator
            + ": %{y:,.2f}"
            + "<extra></extra>"
        ),
    )

    figure.update_layout(
        template="plotly_white",
        transition_duration=350,
        hovermode="closest",
        showlegend=False,

        margin={
            "l": 30,
            "r": 20,
            "t": 30,
            "b": 30,
        },

        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        font={
            "family": "Inter, Segoe UI, Arial, sans-serif",
            "color": "#4B5667",
        },

        hoverlabel={
            "bgcolor": "#17202D",
            "bordercolor": "#17202D",
            "font": {
                "color": "#FFFFFF",
                "size": 12,
            },
        },
    )

    figure.update_xaxes(
        title=x_indicator,
        type="linear" if x_scale == "Linear" else "log",
        showgrid=True,
        gridcolor="#EEF0F3",
        zeroline=False,

        tickfont={
            "size": 10,
            "color": "#7A8493",
        },

        title_font={
            "size": 11,
            "color": "#536071",
        },
    )

    figure.update_yaxes(
        title=y_indicator,
        type="linear" if y_scale == "Linear" else "log",
        showgrid=True,
        gridcolor="#EEF0F3",
        zeroline=False,

        tickfont={
            "size": 10,
            "color": "#7A8493",
        },

        title_font={
            "size": 11,
            "color": "#536071",
        },
    )

    return (
        figure,
        f"Año {selected_year}",
        str(len(comparison_df)),
        f"Mostrando información de {selected_year}",
    )


# --------------------------------------------------
# CREAR GRÁFICA TEMPORAL
# --------------------------------------------------

def create_time_series(
    data,
    axis_type,
    indicator_name,
    selected_year,
    line_color,
):

    # Mostrar únicamente la historia hasta el año escogido
    data = data[
        data["Year"] <= selected_year
    ].sort_values("Year").copy()

    # Evitar valores inválidos en escalas logarítmicas
    if axis_type == "Log":
        data = data[data["Value"] > 0]

    # Crear gráfica
    figure = px.line(
        data,
        x="Year",
        y="Value",
        markers=True,
    )

    figure.update_traces(
        line={
            "color": line_color,
            "width": 2.5,
        },

        marker={
            "size": 6,
            "color": "#FFFFFF",
            "line": {
                "width": 2,
                "color": line_color,
            },
        },

        hovertemplate=(
            "<b>Año %{x}</b><br>"
            "Valor: %{y:,.2f}"
            "<extra></extra>"
        ),
    )

    # Resaltar el último dato disponible
    if not data.empty:

        latest_row = data.iloc[-1]

        figure.add_scatter(
            x=[latest_row["Year"]],
            y=[latest_row["Value"]],
            mode="markers",
            marker={
                "size": 12,
                "color": line_color,
                "line": {
                    "width": 3,
                    "color": "#FFFFFF",
                },
            },
            hovertemplate=(
                "<b>Dato seleccionado</b><br>"
                f"Año: {int(latest_row['Year'])}<br>"
                f"Valor: {latest_row['Value']:,.2f}"
                "<extra></extra>"
            ),
            showlegend=False,
        )

        # Línea vertical del año elegido
        figure.add_vline(
            x=selected_year,
            line_width=1,
            line_dash="dot",
            line_color="#B8C0CC",
        )

    figure.update_layout(
        template="plotly_white",
        showlegend=False,
        hovermode="x unified",
        transition_duration=350,

        margin={
            "l": 20,
            "r": 10,
            "t": 34,
            "b": 25,
        },

        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        font={
            "family": "Inter, Segoe UI, Arial, sans-serif",
            "color": "#586474",
        },
    )

    figure.update_xaxes(
        title=None,
        showgrid=False,
        zeroline=False,
        nticks=6,

        tickfont={
            "size": 10,
            "color": "#7A8493",
        },
    )

    figure.update_yaxes(
        title=None,
        type="linear" if axis_type == "Linear" else "log",
        showgrid=True,
        gridcolor="#EEF0F3",
        zeroline=False,

        tickfont={
            "size": 10,
            "color": "#7A8493",
        },
    )

    figure.add_annotation(
        x=0,
        y=1.13,
        xref="paper",
        yref="paper",
        text=indicator_name,
        showarrow=False,
        xanchor="left",

        font={
            "size": 10,
            "color": "#7A8493",
        },
    )

    return figure


# --------------------------------------------------
# CALLBACK DE LAS GRÁFICAS DE LA DERECHA
# --------------------------------------------------

@app.callback(
    Output("x-time-series", "figure"),
    Output("y-time-series", "figure"),
    Output("selected-country", "children"),
    Output("x-series-description", "children"),
    Output("y-series-description", "children"),

    Input("crossfilter-indicator-scatter", "hoverData"),
    Input("crossfilter-xaxis-column", "value"),
    Input("crossfilter-yaxis-column", "value"),
    Input("crossfilter-xaxis-type", "value"),
    Input("crossfilter-yaxis-type", "value"),

    # Esta entrada hace que las dos gráficas cambien con el slider
    Input("crossfilter-year--slider", "value"),
)
def update_time_series(
    hover_data,
    x_indicator,
    y_indicator,
    x_scale,
    y_scale,
    selected_year,
):

    # País seleccionado
    country_name = get_country_from_hover(hover_data)

    # Datos del indicador X
    x_data = df[
        (df["Country Name"] == country_name)
        & (df["Indicator Name"] == x_indicator)
    ]

    # Datos del indicador Y
    y_data = df[
        (df["Country Name"] == country_name)
        & (df["Indicator Name"] == y_indicator)
    ]

    # Crear serie X hasta el año seleccionado
    x_figure = create_time_series(
        data=x_data,
        axis_type=x_scale,
        indicator_name=x_indicator,
        selected_year=selected_year,
        line_color="#315D7A",
    )

    # Crear serie Y hasta el año seleccionado
    y_figure = create_time_series(
        data=y_data,
        axis_type=y_scale,
        indicator_name=y_indicator,
        selected_year=selected_year,
        line_color="#846746",
    )

    return (
        x_figure,
        y_figure,
        country_name,
        f"Historia de {country_name} hasta {selected_year}",
        f"Historia de {country_name} hasta {selected_year}",
    )


# --------------------------------------------------
# EJECUTAR LA APLICACIÓN
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
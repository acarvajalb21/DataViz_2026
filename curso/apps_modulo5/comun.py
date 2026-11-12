"""Rutas y arranque compartidos por los tres ejemplos del módulo 5."""

import os
from pathlib import Path

import pandas as pd
from dash import Dash

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"


def leer_datos(nombre, columnas):
    archivo = DATA / nombre
    if not archivo.exists():
        raise FileNotFoundError(
            f"Falta {archivo}. Ejecuta: python descargar_datos.py"
        )
    datos = pd.read_csv(archivo)
    faltantes = set(columnas) - set(datos.columns)
    if faltantes:
        raise ValueError(f"Columnas ausentes en {nombre}: {sorted(faltantes)}")
    return datos


def crear_app(nombre, titulo):
    app = Dash(nombre, title=titulo, assets_folder=str(BASE / "assets"))

    @app.server.get("/healthz")
    def healthz():
        return {"status": "ok"}

    return app


def ejecutar(app):
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "8080")),
        debug=os.environ.get("DASH_DEBUG", "0") == "1",
    )

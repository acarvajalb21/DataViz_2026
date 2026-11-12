"""Configuración del servidor utilizado dentro de Docker y Cloud Run."""
import os

bind = "0.0.0.0:" + os.environ.get("PORT", "8080")
workers = 1
threads = 4
timeout = 120
accesslog = "-"
errorlog = "-"

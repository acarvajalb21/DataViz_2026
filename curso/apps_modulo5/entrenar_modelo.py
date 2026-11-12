"""Reproduce el entrenamiento y la serialización del profesor."""

import hashlib
import json

import joblib
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from comun import BASE, DATA, leer_datos

MODELOS = BASE / "models"
MODELO = MODELOS / "modelo_credito.pkl"
METADATOS = MODELOS / "modelo_credito.json"


def firma_datos():
    return hashlib.sha256((DATA / "data_banco_creditos.csv").read_bytes()).hexdigest()


def entrenar():
    datos = leer_datos(
        "data_banco_creditos.csv", ["tiempo_analisis_min", "monto_credito_millones"]
    )
    x_train, _, y_train, _ = train_test_split(
        datos[["tiempo_analisis_min"]],
        datos["monto_credito_millones"],
        test_size=0.2,
        random_state=42,
    )
    modelo = LinearRegression().fit(x_train, y_train)
    MODELOS.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, MODELO)
    METADATOS.write_text(
        json.dumps(
            {"scikit_learn": sklearn.__version__, "datos_sha256": firma_datos()},
            indent=2,
        ),
        encoding="utf-8",
    )
    return modelo


def cargar_modelo():
    # Se regenera si cambian los datos o la versión de scikit-learn.
    if MODELO.exists() and METADATOS.exists():
        registro = json.loads(METADATOS.read_text(encoding="utf-8"))
        if registro == {
            "scikit_learn": sklearn.__version__,
            "datos_sha256": firma_datos(),
        }:
            return joblib.load(MODELO)
    return entrenar()


if __name__ == "__main__":
    entrenar()
    print(f"Modelo entrenado y guardado en {MODELO}")

"""Comprobaciones funcionales de las tres apps, sin servicios externos."""

import unittest

import joblib
import pandas as pd

import app
import app_finanzas
import app_mapas
from entrenar_modelo import MODELO


class DashboardsDelModulo(unittest.TestCase):
    def test_prediccion_del_profesor_y_modelo_serializado(self):
        # El módulo publica 36.53 millones para 45 minutos.
        self.assertIn("36.53 millones", app.predecir_credito(45))
        modelo = joblib.load(MODELO)
        valor = modelo.predict(pd.DataFrame({"tiempo_analisis_min": [45]}))[0]
        self.assertAlmostEqual(valor, 36.53, places=2)

    def test_entrada_vacia_e_invalida(self):
        self.assertIn("Ingresa un tiempo", app.predecir_credito(None))
        for valor in [-1, float("inf"), float("nan"), "texto"]:
            with self.subTest(valor=valor):
                self.assertIn("número válido", app.predecir_credito(valor))
        self.assertIn("millones", app.predecir_credito(0))

    def test_grafico_de_creditos(self):
        self.assertEqual(len(app.fig.data[0].x), len(app.df))
        self.assertEqual(len(app.fig.data[1].x), 100)
        self.assertGreater(app.modelo.coef_[0], 0)

    def test_mapa_para_todos_los_anios(self):
        for anio in app_mapas.ANIOS:
            with self.subTest(anio=anio):
                texto, figura = app_mapas.update_graph(anio)
                self.assertIn(str(anio), texto)
                self.assertGreater(len(figura.data[0].locations), 0)
                self.assertTrue(all(0 <= v <= 100 for v in figura.data[0].z))
        self.assertNotEqual(
            list(app_mapas.update_graph(2015)[1].data[0].z),
            list(app_mapas.update_graph(2018)[1].data[0].z),
        )

    def test_finanzas_multiples_acciones_y_seleccion_vacia(self):
        graficos = app_finanzas.update_graph(["YHOO", "GOOGL"])
        self.assertEqual(len(graficos), 2)
        for grafico in graficos:
            self.assertEqual(grafico.figure.data[0].type, "candlestick")
            self.assertEqual(len(grafico.figure.data), 4)
            self.assertGreater(len(grafico.figure.data[0].x), 10)
            self.assertEqual(list(grafico.figure.data[0].x), sorted(grafico.figure.data[0].x))
        self.assertIn("Selecciona", app_finanzas.update_graph([]).children)

    def test_rutas_de_las_tres_apps(self):
        for modulo in [app, app_mapas, app_finanzas]:
            cliente = modulo.server.test_client()
            for ruta in ["/", "/healthz", "/_dash-layout", "/_dash-dependencies", "/assets/style.css"]:
                with self.subTest(app=modulo.__name__, ruta=ruta):
                    with cliente.get(ruta) as respuesta:
                        self.assertEqual(respuesta.status_code, 200)
            self.assertEqual(cliente.get("/healthz").json, {"status": "ok"})

    def test_callback_creditos_por_http(self):
        respuesta = app.server.test_client().post(
            "/_dash-update-component",
            json={
                "output": "output-prediccion.children",
                "outputs": {"id": "output-prediccion", "property": "children"},
                "inputs": [{"id": "input-tiempo-analisis", "property": "value", "value": 45}],
                "state": [],
                "changedPropIds": ["input-tiempo-analisis.value"],
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("36.53 millones", respuesta.json["response"]["output-prediccion"]["children"])

    def test_callback_mapas_por_http(self):
        respuesta = app_mapas.server.test_client().post(
            "/_dash-update-component",
            json={
                "output": "..output_container.children...my_bee_map.figure..",
                "outputs": [
                    {"id": "output_container", "property": "children"},
                    {"id": "my_bee_map", "property": "figure"},
                ],
                "inputs": [{"id": "slct_year", "property": "value", "value": 2018}],
                "state": [],
                "changedPropIds": ["slct_year.value"],
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("2018", respuesta.json["response"]["output_container"]["children"])

    def test_callback_finanzas_por_http(self):
        respuesta = app_finanzas.server.test_client().post(
            "/_dash-update-component",
            json={
                "output": "graphs.children",
                "outputs": {"id": "graphs", "property": "children"},
                "inputs": [{"id": "stock-ticker-input", "property": "value", "value": ["YHOO", "GOOGL"]}],
                "state": [],
                "changedPropIds": ["stock-ticker-input.value"],
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json["response"]["graphs"]["children"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

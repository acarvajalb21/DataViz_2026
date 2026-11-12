# Jupyter · Salud en el Atlántico

Esta carpeta reúne los dos cuadernos de la entrega final de Mateo y el Jupyter Book compilado. Para leerlo sin ejecutar código, abra [`docs/index.html`](docs/index.html). Las gráficas del libro HTML son interactivas; los cuadernos también guardan imágenes de respaldo para visores que no ejecutan JavaScript.

- [`EDA_acceso_salud_Atlantico_CNPV2018.ipynb`](EDA_acceso_salud_Atlantico_CNPV2018.ipynb): exploración completa.
- [`Modelo_acceso_salud_Atlantico_CNPV2018.ipynb`](Modelo_acceso_salud_Atlantico_CNPV2018.ipynb): construcción y evaluación del modelo v2.
- `../ml_salud/`: única carpeta del pipeline y sus resultados, compartida por los entregables.
- `datos/`: instrucciones y mapa municipal. Los cuatro CSV individuales están en la carpeta compartida `../datos/`.

Para reejecutar, instale las dependencias de `requirements.txt` y `../ml_salud/requirements.txt`, indique la carpeta de los cuatro CSV mediante la variable de entorno `CNPV_DATOS` y abra Jupyter **desde `jupyter_salud/`**. El cuaderno del modelo consulta los resultados guardados en `../ml_salud/resultados/` y comprueba las huellas de los CSV. `python validar_eda.py` comprueba la estructura del cuaderno exploratorio sin entrenar el modelo.

La procedencia de los archivos y el historial anterior están registrados en `../../gestion/migracion/` y `../../archivo/`. Los cuadernos buscan los CSV en `../datos/`; `CNPV_DATOS` permite indicar otra carpeta.

Los entornos ya están creados y registrados: el EDA usa **Libro Salud · Python 3.12 · pandas 2** y el modelo usa **Modelo Salud · Python 3.12 · pandas 3**. Los cuadernos tienen esos kernels seleccionados en sus metadatos. Abre Jupyter con el iniciador de la raíz. Las dependencias siguen separadas y se conservan sus versiones registradas en `../../gestion/entorno/`.

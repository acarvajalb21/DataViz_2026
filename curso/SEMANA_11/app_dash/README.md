# Dashboard de predicción de crédito

Esta carpeta contiene la aplicación Dash del módulo 5. Está separada de `modelo.ipynb` porque `app.py` es el programa que inicia el servidor web y necesita encontrar el CSV y el modelo serializado al ejecutarse.

## Ejecutar

Usa el entorno `dash_project` y, desde esta carpeta, ejecuta:

```powershell
conda activate dash_project
python app.py
```

Abre <http://127.0.0.1:8050/> en el navegador. El modelo se entrenó con `data_banco_creditos.csv` y se guardó como `modelo_credito.pkl` desde el cuaderno. Para volver a generarlo, ejecuta las celdas del cuaderno en orden.

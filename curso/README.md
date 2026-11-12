# Material del curso

| Carpeta | Contenido |
| --- | --- |
| `python/` | Cuadernos de los módulos, ejercicios y sus CSV. |
| `DASH/` | Explorador de indicadores mundiales; conserva su entorno existente. |
| `SEMANA_11/` | Cuaderno del modelo y app de crédito original; conserva su entorno Python 3.11. |
| `apps_modulo5/` | Apps recuperadas de crédito, mapas y finanzas; entorno propio preparado y 9 pruebas aprobadas. Se abren con `iniciar.bat`. |
| `R_Studio/` | Ejercicios y datos de R. |
| `jbook_dataviz_2026/` | Libro del curso y entorno Python 3.11. |

Invoca los intérpretes por su ruta actual y usa `python -m ...` para los comandos de Python. Los tres entornos trasladados fueron reconstruidos en sus rutas actuales. Sus ejecutables `pip.exe` y `jupyter-book.exe` funcionan; el cuaderno de crédito tiene su propio kernel Python 3.11.

Desde la raíz DataViz_2026:

```powershell
.\curso\DASH\.venv\Scripts\python.exe .\curso\DASH\app.py
.\curso\SEMANA_11\app_dash\.venv\Scripts\python.exe .\curso\SEMANA_11\app_dash\app.py
.\curso\jbook_dataviz_2026\.venv\Scripts\python.exe -c "from jupyter_book.cli.main import main; main()" build .\curso\jbook_dataviz_2026\docs
```

Las dos apps anteriores usan el puerto 8050: ejecútalas por separado del Dash de salud. Los cuadernos se abren con JupyterLab desde la guía general.

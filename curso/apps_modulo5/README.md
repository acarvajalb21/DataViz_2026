# Dashboards del módulo 5

La aplicación principal es **Predicción de monto de crédito con regresión lineal**, el último dashboard con código completo antes de Docker. Se incluyen las otras dos aplicaciones finales como programas independientes:

- `app.py`: créditos; gráfico de dispersión, recta de regresión y predicción al ingresar minutos.
- `app_mapas.py`: mapa de colonias de abejas; selector de 2015 a 2018 y filtro `Varroa_mites`.
- `app_finanzas.py`: Finance Explorer; selección múltiple de acciones, velas y bandas de Bollinger.

Los ejercicios anteriores enseñan componentes y callbacks. Estos tres proyectos tienen propósitos distintos; el último no reemplaza funcionalmente a los otros dos. La parte de Docker utiliza una app Dash genérica y hace referencia a mapas, sin proporcionar un nuevo dashboard completo.

Fuente: [módulo 5 del profesor Carlos de Oro Aguado](https://cdeoroaguado.github.io/pbook_dataviz/modulo_5.html).

## Inicio rápido en este computador

Abre esta carpeta y haz doble clic en **`iniciar.bat`**. Cuando aparezca el mensaje del servidor, entra en [http://127.0.0.1:8080](http://127.0.0.1:8080). Mantén la ventana abierta; para detenerlo, pulsa **Ctrl+C**.

Desde PowerShell también puedes ejecutar:

```powershell
.\iniciar.bat
```

Para abrir una de las otras aplicaciones, detén primero la que está usando el puerto 8080 y ejecuta:

```powershell
.\iniciar.bat mapas
```

```powershell
.\iniciar.bat finanzas
```

## Instalación en otro computador

En este computador el entorno está preparado con **Python 3.12.10** y las versiones fijadas en `requirements.txt`; sus 9 pruebas pasaron. La imagen Docker conserva Python 3.14. Abre una terminal dentro de `app_dash`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

No hace falta activar el entorno. Los tres CSV están incluidos en `data/`. La aplicación de créditos carga `models/modelo_credito.pkl`; si falta o cambia la versión de scikit-learn o el CSV, regenera el modelo automáticamente.

Para entrenarlo expresamente:

```powershell
.\.venv\Scripts\python.exe entrenar_modelo.py
```

Se reproduce el entrenamiento del módulo: regresión lineal, tiempo de análisis como entrada, monto en millones como salida, división 80/20 y `random_state=42`. **45 minutos deben producir 36.53 millones.**

Los datos se leen mediante rutas relativas al proyecto, por lo que no depende de la carpeta desde la que invoques Python. Para descargar nuevamente los CSV originales:

```powershell
.\.venv\Scripts\python.exe descargar_datos.py
```

Los datos proceden del [repositorio Datos del profesor](https://github.com/cdeoroaguado/Datos): `datadescrip/data_banco_creditos.csv`, `dataviz/intro_bees.csv` y `dataviz/dash-stock-ticker-demo.csv`.

## Docker

**Sí, el módulo incluye Docker**: contenedores, Dockerfile, imágenes, instalación, construcción, ejecución, exportación `.tar` y subida a Google Cloud. Consulta la [sección Docker](https://cdeoroaguado.github.io/pbook_dataviz/modulo_5.html#docker).

Con Docker Desktop instalado y su motor en ejecución, abre una terminal dentro de `app_dash`:

```powershell
docker build -t mi-dash .
docker run --rm --name modulo5-creditos -p 8080:8080 mi-dash
```

Entra en [http://localhost:8080](http://localhost:8080). El contenedor inicia el dashboard de créditos mediante Gunicorn. El servidor escucha en `0.0.0.0` y utiliza `PORT`, con 8080 como valor predeterminado. El modelo se entrena al construir la imagen con las mismas versiones de librerías que tendrá al ejecutarse.

Para desplegar una de las otras apps con la misma imagen:

```powershell
docker run --rm -p 8080:8080 mi-dash gunicorn --config gunicorn.conf.py app_mapas:server
```

```powershell
docker run --rm -p 8080:8080 mi-dash gunicorn --config gunicorn.conf.py app_finanzas:server
```

Para exportar la imagen como en clase:

```powershell
docker save -o mi-dash.tar mi-dash
```

## Despliegue posterior

El despliegue en Google Cloud queda a tu cargo. El proyecto entrega el objeto `server`, el Dockerfile y un servidor de producción que respeta la variable `PORT`.

## Verificación

```powershell
.\.venv\Scripts\python.exe pruebas.py
```

En este computador, si se reutiliza el entorno preparado junto a `app_dash`, usa `..\.venv\Scripts\python.exe pruebas.py`.

Las pruebas comprueban la predicción publicada, entradas vacías e inválidas, lectura del modelo guardado, los cuatro años del mapa, gráficos de múltiples acciones y peticiones a las rutas y callbacks de las tres aplicaciones.

## Ajustes respecto a los ejemplos

- Se mantiene el comportamiento de cada aplicación y se da formato adaptable a pantallas pequeñas.
- Se conservan los parámetros de Bollinger del profesor: ventana de 10 y 5 desviaciones estándar.
- Se incluyen datos locales y entrenamiento reproducible; los CSV no se descargan al abrir la aplicación.
- Se utiliza `app.run()` para compatibilidad con Dash actual y se exporta `server = app.server` en las tres apps.
- Gunicorn se utiliza en Linux/Docker; el arranque local también funciona en Windows.
- Los archivos `.env`, entornos locales y archivos de imagen se excluyen del contexto de despliegue.

El contenedor debe construirse y probarse con Docker; la comprobación local de Python no sustituye esa construcción. Docker no está disponible en el entorno de preparación, por lo que la imagen no se ha construido aquí.

# DataViz 2026

## Abrir y trabajar

Haz doble clic en **INICIAR_DATAVIZ.cmd** y elige Shiny, Dash, JupyterLab, Bookdown, Jupyter Book o RStudio. El menú utiliza los entornos de este computador.

Mantén abierta la terminal mientras uses un servidor local. Para detenerlo, pulsa `Ctrl+C` en esa terminal.

En PowerShell, desde esta carpeta, también puedes ejecutar:

```powershell
.\ABRIR_DATAVIZ.ps1 Shiny
.\ABRIR_DATAVIZ.ps1 Dash
.\ABRIR_DATAVIZ.ps1 Jupyter
.\ABRIR_DATAVIZ.ps1 Bookdown
.\ABRIR_DATAVIZ.ps1 JupyterBook
.\ABRIR_DATAVIZ.ps1 RStudio
```

| Herramienta local | Dirección |
| --- | --- |
| Shiny | http://127.0.0.1:3838 |
| Dash | http://127.0.0.1:8050 |
| JupyterLab | El iniciador abre la sesión autenticada del puerto 8888. |
| Bookdown | http://127.0.0.1:4321 |
| Jupyter Book | http://127.0.0.1:4322 |

JupyterLab sirve para editar y ejecutar los cuadernos. Jupyter Book es el libro HTML para leer. Los cuadernos de salud seleccionan automáticamente sus kernels separados: **Modelo Salud** usa pandas 3 y **Libro Salud** usa pandas 2. El cuaderno de crédito del curso tiene su kernel Python 3.11.

Para RStudio, abre `DataViz_2026.Rproj` o usa el menú. Para trabajar en el libro con el panel Build de RStudio, abre `proyecto_salud/bookdown_salud/Bookdown.Rproj`. Ambos proyectos cargan primero la biblioteca compartida `.dataviz-runtime/r-library/`.

## Carpetas

| Carpeta | Contenido |
| --- | --- |
| `proyecto_salud/` | Entrega final: Shiny, Dash, Bookdown, Jupyter y modelo. |
| `curso/` | Ejercicios y libros del curso. |
| `archivo/` | Respaldo original, versiones locales distintas e historias Git anteriores. |
| `gestion/` | Documentación, dependencias registradas y verificaciones. |

Los cuatro CSV originales están en `proyecto_salud/datos/`. El código compartido del modelo está únicamente en `proyecto_salud/ml_salud/`. Los recursos necesarios para los despliegues independientes permanecen junto a cada entregable.

## Compilar y comprobar

```powershell
.\ABRIR_DATAVIZ.ps1 CompilarBookdown
.\ABRIR_DATAVIZ.ps1 CompilarJupyterBook
.\ABRIR_DATAVIZ.ps1 CompilarLibroCurso
.\ABRIR_DATAVIZ.ps1 PruebasShiny
.\ABRIR_DATAVIZ.ps1 PruebasModelo
```

La compilación de Jupyter Book genera `jupyter_salud/_build/html/`; el lector local prefiere esa versión cuando existe. Bookdown compila en `bookdown_salud/docs/`. Los resultados existentes del modelo se conservaron sin reentrenarlo.

## Versiones publicadas

El menú también permite abrir [Shiny](https://shiny-salud-atlantico-409319239507.us-east1.run.app/), [Dash](https://dataviz-salud-atlantico-409319239507.us-east1.run.app/), [Bookdown](https://acarvajalb21.github.io/EDAR/) y [Jupyter Book](https://acarvajalb21.github.io/EDAPYTHON/).

Las cuatro publicaciones se actualizaron el 17 de noviembre de 2026 con leyendas en las gráficas, el asistente ampliado y la explicación del modelo. Consulta el [registro de publicación y verificación](gestion/publicacion/ESTADO.md).

Google Cloud CLI y GitHub quedaron autenticados para actualizar estas publicaciones. `GCLOUD.ps1` proporciona acceso a la CLI desde esta carpeta. Los proyectos locales funcionan con sus iniciadores habituales.

Consulta el [estado del entorno](gestion/entorno/ESTADO.md) y el [registro de organización](gestion/migracion/ORGANIZACION.md). Las versiones anteriores se pueden recuperar con `gestion/recuperar_archivo.py` y el índice de migración.

# Publicaciones verificadas

Fecha: 17 de noviembre de 2026. Las cuatro direcciones originales muestran la versión actual del proyecto.

| Entregable | Dirección | Versión publicada |
| --- | --- | --- |
| Shiny | https://shiny-salud-atlantico-409319239507.us-east1.run.app/ | Revisión `shiny-salud-atlantico-c-cb6d100f-20261117` |
| Dash | https://dataviz-salud-atlantico-409319239507.us-east1.run.app/ | Revisión `dataviz-salud-atlantico-c-cb6d100f-20261117` |
| Bookdown | https://acarvajalb21.github.io/EDAR/ | Repositorio EDAR, commit `ec63a3f685b7e8a313dcf49551304ef37df9393d` |
| Jupyter Book | https://acarvajalb21.github.io/EDAPYTHON/ | Repositorio EDAPYTHON, commit `ac629ab8298e9a7475c948f7769ca4fd24d2803a` |

## Cambios publicados

- Leyendas y significado de colores y series en las gráficas.
- Reconocimiento de preguntas de BQSI sobre el modelo, la partición y las métricas.
- Justificación de la elección del boosting y explicación del umbral y de los límites del modelo.
- Bookdown con texto ampliado, código plegable y capítulo de código del proyecto.
- Cuadernos y libros compilados con estos cambios.

## Verificación

Los dos servicios de Cloud Run terminaron sus despliegues y asignaron el 100 % del tráfico a las nuevas revisiones. GitHub Pages terminó correctamente sus publicaciones en ambos repositorios.

Se comprobaron 13 rutas públicas con HTTP 200. Los HTML revisados de ambos libros coinciden byte a byte con los archivos de sus commits publicados; el informe de Dash y el widget de Shiny coinciden con los recursos locales corregidos. `docs/publicacion.json` de cada libro registra las huellas SHA-256 del HTML.

Se comprobaron en la API publicada estas tres preguntas: por qué se escogió el modelo, cómo se dividieron los datos y por qué las métricas son bajas. Las tres respondieron con sus fuentes y con la cabecera CORS que permite usarlas desde Shiny. El modo observado fue `demostracion`, que utiliza las respuestas y fuentes del proyecto. La prueba local del asistente aprobó 110 de 110 preguntas antes de publicar.

La evidencia de HTTP, respuestas y ejecuciones de GitHub Actions está en `verificacion_2026-11-17.json`.

## Fuentes y organización

`proyecto_salud/` sigue siendo la carpeta de trabajo local. Los repositorios EDAR y EDAPYTHON mantienen su estructura histórica y la publicación desde `/docs`; se adaptaron las rutas de los dos archivos nuevos de Bookdown que leen el código y el experimento del modelo. Las copias temporales de publicación se retiraron después de verificar los enlaces.

Las credenciales permanecen en las configuraciones privadas de Google Cloud CLI y Git Credential Manager. Los microdatos originales y las predicciones individuales de validación quedaron fuera de estas publicaciones.

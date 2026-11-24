# Publicaciones verificadas

Fecha: 17 de noviembre de 2026, con actualizaciones el 19 y el 24 de noviembre. Las cuatro direcciones originales muestran la versión actual del proyecto.

| Entregable | Dirección | Versión publicada |
| --- | --- | --- |
| Shiny | https://shiny-salud-atlantico-409319239507.us-east1.run.app/ | Revisión `shiny-salud-atlantico-video-20261124` |
| Dash | https://dataviz-salud-atlantico-409319239507.us-east1.run.app/ | Revisión `dataviz-salud-atlantico-video-20261124` |
| Bookdown | https://acarvajalb21.github.io/EDAR/ | Repositorio EDAR, commit `63028d5018d5bd22580eb6138a4b4df7397a5218` |
| Jupyter Book | https://acarvajalb21.github.io/EDAPYTHON/ | Repositorio EDAPYTHON, commit `3b9178e16e53527b528411d0d20be728acf40696` |

## Cambios publicados

- Leyendas y significado de colores y series en las gráficas.
- Reconocimiento de preguntas de BQSI sobre el modelo, la partición y las métricas.
- Justificación de la elección del boosting y explicación del umbral y de los límites del modelo.
- Bookdown con texto ampliado, código plegable y capítulo de código del proyecto.
- Cuadernos y libros compilados con estos cambios.

## Actualización del 19 de noviembre

Se ajustó la redacción de la sección del experimento de mejora en el Bookdown, el cuaderno del modelo y el informe del Dash. Se volvieron a publicar el Dash en Cloud Run y los dos libros en GitHub Pages; las huellas de `docs/publicacion.json` corresponden a los HTML nuevos. En línea se comprobó la frase nueva en los tres sitios y las respuestas del asistente sobre el modelo.

## Actualización del 24 de noviembre

Shiny y Dash tienen una sección Video con la exposición (15:24) y nueve partes que se pueden pulsar. Se publicaron las dos aplicaciones en Cloud Run con sus ajustes anteriores; los libros no cambiaron. En línea, el video descargado completo coincide con el archivo local en ambos servicios (MD5 `84421f7600faf25ee7b91675c0afb62c`), la respuesta por rangos es 206 y el salto a Conclusiones reprodujo el video en el navegador. No se probó en Safari.

## Verificación del 17 de noviembre

Los dos servicios de Cloud Run terminaron sus despliegues y asignaron el 100 % del tráfico a las nuevas revisiones. GitHub Pages terminó correctamente sus publicaciones en ambos repositorios.

Se comprobaron 13 rutas públicas con HTTP 200. Los HTML revisados de ambos libros coinciden byte a byte con los archivos de sus commits publicados; el informe de Dash y el widget de Shiny coinciden con los recursos locales corregidos. `docs/publicacion.json` de cada libro registra las huellas SHA-256 del HTML.

Se comprobaron en la API publicada estas tres preguntas: por qué se escogió el modelo, cómo se dividieron los datos y por qué las métricas son bajas. Las tres respondieron con sus fuentes y con la cabecera CORS que permite usarlas desde Shiny. El modo observado fue `demostracion`, que utiliza las respuestas y fuentes del proyecto. La prueba local del asistente aprobó 110 de 110 preguntas antes de publicar.

La evidencia de HTTP, respuestas y ejecuciones de GitHub Actions está en `verificacion_2026-11-17.json`.

## Fuentes y organización

`proyecto_salud/` sigue siendo la carpeta de trabajo local. Los repositorios EDAR y EDAPYTHON mantienen su estructura histórica y la publicación desde `/docs`; se adaptaron las rutas de los dos archivos nuevos de Bookdown que leen el código y el experimento del modelo. Las copias temporales de publicación se retiraron después de verificar los enlaces.

Las credenciales permanecen en las configuraciones privadas de Google Cloud CLI y Git Credential Manager. Los microdatos originales y las predicciones individuales de validación quedaron fuera de estas publicaciones.

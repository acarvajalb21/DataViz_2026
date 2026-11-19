# Entorno de DataViz: configuración comprobada

Fecha: 12 de noviembre de 2026. El acceso cotidiano es `INICIAR_DATAVIZ.cmd`, en la raíz.

| Punto | Resultado |
| --- | --- |
| Shiny de prueba | Proceso anterior terminado. Los nuevos ensayos comprueban el dueño del puerto y lo liberan al finalizar. |
| Entornos del curso | Los tres fueron reconstruidos en sus rutas actuales. Funcionan `pip.exe`, las activaciones y `jupyter-book.exe`; el libro del curso compiló. |
| Modelo | Python 3.12.10, pandas 3.0.5 y scikit-learn 1.9.1 en `proyecto_salud/ml_salud/.venv`. Pasaron las 7 pruebas del modelo guardado. |
| Jupyter Book | Entorno separado en `proyecto_salud/jupyter_salud/.venv`, con pandas 2.3.3, Jupyter Book 1.x y Kaleido. El libro compiló con sus 15 figuras interactivas. |
| Pruebas de R | `testthat` instalado y las pruebas de Shiny aprobadas. |
| RStudio | `DataViz_2026.Rproj` y `Bookdown.Rproj` cargan primero `.dataviz-runtime/r-library/`. La biblioteca global se conserva para otros paquetes y proyectos. |
| Google Cloud CLI | Versión 593.0.0 instalada y proyecto/región configurados. Sesión vinculada el 17 de noviembre de 2026; Shiny y Dash actualizados en Cloud Run. Los libros también se publicaron en GitHub Pages. Registro en `../publicacion/ESTADO.md`. |
| Git | Código, organización y configuración se guardan localmente. Consulta `git log -1 --oneline` y `git status --short` para el estado exacto. |

## Kernels de los cuadernos

- `modelo-salud`: Python 3.12.10, pandas 3.0.5, modelo de salud.
- `libro-salud`: Python 3.12.10, pandas 2.3.3, EDA y libro de salud.
- `credito-curso`: Python 3.11.9, pandas 2.1.0, cuaderno de crédito original.

Los tres se comprobaron ejecutando código a través del canal WebSocket de JupyterLab. Los cuadernos ya tienen asignado su kernel correspondiente. El servidor Jupyter de trabajo se inició con el usuario de Windows y utiliza el puerto 8888.

## Comprobaciones realizadas

- Iniciadores de Shiny, Dash y los dos lectores HTML: HTTP 200 y puertos liberados después de cada prueba.
- Pruebas de Shiny: 9 grupos y 70 aserciones aprobadas.
- Módulo 5 del curso: entorno propio y 9 pruebas de crédito, mapas y finanzas aprobadas.
- Dash y datos agregados: pruebas aprobadas; asistente local: 89/89 preguntas correctas.
- Modelo: 7 pruebas de contrato e inferencia aprobadas; exportación PNG con Kaleido comprobada.
- EDA: todas sus celdas ejecutadas con 1.932 registros ficticios aislados; se generaron 9 figuras y el CSV esperado.
- Bookdown, Jupyter Book de salud y libro del curso: compilación completada.
- Inicio de R desde la raíz y desde el proyecto Bookdown: misma biblioteca principal del proyecto.

No se volvió a entrenar el modelo ni se reemplazaron sus resultados con las pruebas ficticias. Los cuatro CSV originales se conservaron.

## Reproducibilidad

`*.requirements.txt` y `*.freeze.txt` registran los paquetes de Python. `R-paquetes.csv` registra los paquetes de la biblioteca de R. `entornos_curso.json`, `entornos_salud.json`, `kernels.json`, `servidores.json` y `verificacion.json` guardan la evidencia actual. Los dos archivos del modelo cuya huella se verifica tienen atributos Git que preservan sus bytes.

Los scripts de esta carpeta permiten reconstruir los entornos y repetir las comprobaciones. Los paquetes instalados, datos originales, cachés y configuración privada de Google Cloud quedan fuera de Git.

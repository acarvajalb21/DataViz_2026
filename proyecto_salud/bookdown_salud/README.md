# Salud en el Atlántico — Bookdown

Este repositorio contiene el **informe Bookdown vigente** del proyecto de Alejandro Carvajal y Mateo Chang. El [libro publicado](https://acarvajalb21.github.io/EDAR/) se genera desde `index.Rmd` y los capítulos `01`–`08`; `docs/` conserva el HTML listo para GitHub Pages. Los antecedentes se conservan en el respaldo archivado.

La pregunta del informe es qué patrones se observaron entre las personas del Atlántico que declararon un problema de salud en los 30 días previos al CNPV 2018, sin hospitalización, y hasta dónde permite clasificarlas la regla operativa `ACCESO_FORMAL_SALUD`. La cohorte tiene **136.034 personas**. La categoría `ACCESO_FORMAL_SALUD = 0` reúne **28.650 (21,06 %)**: 1.907 acudieron a su EPS y no fueron atendidas; las demás reportaron otra acción principal o ninguna. **No equivale a una tasa general de atención denegada ni de necesidad médica insatisfecha.**

## Estructura vigente

- `index.Rmd`, `01`–`08-*.Rmd`, `_bookdown.yml`, `_output.yml`, `style.css`: fuentes y configuración del libro.
- `data/`: cuadros **agregados** para reproducir las tablas; no contiene registros individuales.
- `figures/`: gráficos del análisis y del modelo.
- `scripts/`: preparación de agregados y auditoría.
- `../ml_salud/`: carpeta compartida del pipeline y sus resultados.
- `docs/`: HTML compilado que publica GitHub Pages.
- [`../shiny_salud/`](../shiny_salud/README.md): aplicación Shiny en R, con sus pruebas y despliegue. Se publica en [Cloud Run](https://shiny-salud-atlantico-409319239507.us-east1.run.app/) y se documenta en el capítulo 8 del libro.

El [Dash actual](https://dataviz-salud-atlantico-409319239507.us-east1.run.app/) y el código del modelo están en [EDAPYTHON](https://github.com/acarvajalb21/EDAPYTHON), carpetas `dash_salud/` y `ml_salud/`. El informe técnico de la [auditoría de octubre de 2026](https://github.com/acarvajalb21/EDAPYTHON/blob/main/ml_salud/experimentos_2026_10/INFORME_AUDITORIA.md) documenta la revisión de la versión 1; el modelo vigente (versión 2) y su protocolo están en `ml_salud/experimento_contexto/`. Las versiones anteriores están archivadas fuera de la carpeta de trabajo.

## Reproducir el libro

Para leer el informe no hacen falta los microdatos: abra `docs/index.html` o el enlace publicado. Para volver a compilarlo, instale R, Pandoc y los paquetes `bookdown`, `rmarkdown`, `knitr` y `plotly`; luego, desde esta carpeta del libro:

```powershell
..\..\ABRIR_DATAVIZ.ps1 CompilarBookdown
```

`build_bookdown.R` escribe en `docs/` y copia la fuente desde `../shiny_salud/www/fonts/`. Para **regenerar** las tablas y figuras desde cero se necesitan además Python, las dependencias de `ml_salud` y los cuatro CSV departamentales del CNPV 2018 del DANE (`5PER`, `2HOG`, `1VIV`, `MGN`, departamento 08). Ejecute desde la raíz `python scripts/preparar_resumen.py --data-dir RUTA_CSV_DANE` y luego `python scripts/preparar_auditoria.py`. Los scripts verifican las huellas de los archivos. Los microdatos originales no se suben a GitHub.

**Estado metodológico:** el modelo es retrospectivo y su validación se limita al censo 2018. No se ha demostrado que sus patrones sirvan para decisiones sobre personas actuales. Antes de redefinir la pregunta o la etiqueta del proyecto hace falta comprobar la viabilidad de una fuente que observe barreras reales de atención.

Fuente: [DANE, CNPV 2018](https://microdatos.dane.gov.co/catalog/643).

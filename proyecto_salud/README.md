# Salud en el Atlántico

Entrega final de Alejandro Carvajal y Mateo Chang, recuperada del respaldo del computador anterior. Analiza el acceso formal a salud con datos del CNPV 2018 del DANE. El análisis es descriptivo y el modelo conserva sus resultados guardados; esta migración no lo volvió a entrenar.

| Componente | Entrada |
| --- | --- |
| Shiny | `shiny_salud/app.R` |
| Dash | `dash_salud/app.py`; módulo `dash_salud.app` desde esta carpeta |
| Bookdown | `bookdown_salud/index.Rmd`; libro compilado en `bookdown_salud/docs/index.html` |
| Jupyter | Dos cuadernos en `jupyter_salud/`; libro en `jupyter_salud/docs/index.html` |
| Modelo | `ml_salud/`; dependencias propias en `ml_salud/requirements.txt` |
| Microdatos originales | Los cuatro CSV están en `datos/` |

Usa el iniciador [ABRIR_DATAVIZ.ps1](../ABRIR_DATAVIZ.ps1) y la [guía general](../README.md). Shiny y Dash incluyen los agregados y recursos que necesitan para sus despliegues independientes. El código del modelo se comparte desde `ml_salud/`; los cuadernos y los scripts del libro fueron adaptados para usarlo desde ahí.

El respaldo original, las diferencias anteriores y los historiales Git están en `../archivo/`. La procedencia y los ajustes se documentan en `../gestion/migracion/`. Los enlaces de publicación están en la guía general. Los despliegues existentes no se modificaron.

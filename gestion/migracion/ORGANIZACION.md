# Organización del 12 de noviembre de 2026

La carpeta `proyecto_salud/` contiene la entrega integrada recuperada de `DATAVIZ/` en el ZIP de migración. Los proyectos `EDAR-*` y `EDAPYTHON-*` anteriores se compararon por contenido antes de retirarlos del espacio de trabajo.

## Distribución

- `proyecto_salud/shiny_salud/`: aplicación Shiny recuperada, con módulos, datos agregados y recursos.
- `proyecto_salud/dash_salud/`: Dash vigente, con su informe HTML y recursos para desplegarlo de forma independiente.
- `proyecto_salud/bookdown_salud/`: fuentes y HTML del libro de R.
- `proyecto_salud/jupyter_salud/`: dos cuadernos y Jupyter Book.
- `proyecto_salud/ml_salud/`: única carpeta de código y resultados del modelo.
- `proyecto_salud/datos/`: única copia de los cuatro CSV originales del CNPV 2018.
- `curso/python/`, `curso/DASH/`, `curso/SEMANA_11/`, `curso/apps_modulo5/`, `curso/R_Studio/` y `curso/jbook_dataviz_2026/`: material del curso.

## Conservación y trazabilidad

- El ZIP original queda intacto en `archivo/`.
- `archivos_importados.csv` registra las rutas de origen, destino y huellas originales antes de los ajustes de rutas.
- `recuperacion_versiones_anteriores.csv` permite reconstruir cada archivo anterior desde el ZIP original o desde `versiones_locales_unicas.zip`. Los contenidos idénticos se guardan una sola vez en este último.
- `archivo/historial_git/` contiene bundles verificados con la historia completa de los dos repositorios anteriores.
- `ajustes_rutas.json` registra los archivos adaptados a la organización actual.
- `resumen.json` contiene los recuentos de la integración y la huella del ZIP original.

Para recuperar un archivo sin sobrescribir la versión de trabajo, desde la raíz:

```powershell
.\.venv\Scripts\python.exe gestion\recuperar_archivo.py "EDAR-github/index.Rmd"
```

El archivo aparece en `archivo/recuperados/` y se verifica su SHA-256 antes de escribirlo. El índice CSV permite consultar las demás rutas anteriores.

No se extrajeron `.github_sync`, `.r-lib` ni las copias internas de Shiny y del modelo. Los recursos que forman parte de aplicaciones y libros independientes permanecen en sus carpetas: imágenes, fuentes, bibliotecas del HTML y JSON de despliegue pueden coincidir porque cada entregable los necesita.

## Comprobación

Las comprobaciones actuales se registran en `verificacion.json`. Las verificaciones descritas en los README originales corresponden al equipo anterior y no se consideran automáticamente ejecutadas aquí.

Los servidores publicados conservan sus direcciones. No se modificaron despliegues ni repositorios remotos. El modelo y sus resultados se conservaron sin volver a entrenarlos.

@echo off
setlocal
cd /d "%~dp0"
if not "%~1"=="" (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ABRIR_DATAVIZ.ps1" %*
  exit /b
)
echo.
echo   DATAVIZ 2026
echo.
echo   1. Shiny de salud
echo   2. Dash de salud
echo   3. JupyterLab - editar cuadernos
echo   4. Bookdown - libro de R
echo   5. Jupyter Book - libro de Python
echo   6. RStudio
echo   7. Versiones publicadas en internet
echo   8. Salir
echo.
choice /c 12345678 /n /m "Selecciona una opcion: "
if errorlevel 8 exit /b 0
if errorlevel 7 goto publicados
if errorlevel 6 goto rstudio
if errorlevel 5 goto jupyterbook
if errorlevel 4 goto bookdown
if errorlevel 3 goto jupyter
if errorlevel 2 goto dash
goto shiny
:publicados
set "datavizTool=Publicados"
goto abrir
:rstudio
set "datavizTool=RStudio"
goto abrir
:jupyterbook
set "datavizTool=JupyterBook"
goto abrir
:bookdown
set "datavizTool=Bookdown"
goto abrir
:jupyter
set "datavizTool=Jupyter"
goto abrir
:dash
set "datavizTool=Dash"
goto abrir
:shiny
set "datavizTool=Shiny"
:abrir
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ABRIR_DATAVIZ.ps1" %datavizTool%
if errorlevel 1 pause

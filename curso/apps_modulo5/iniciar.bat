@echo off
setlocal
cd /d "%~dp0"
set "DASH_APP=app.py"
if /I "%~1"=="mapas" set "DASH_APP=app_mapas.py"
if /I "%~1"=="finanzas" set "DASH_APP=app_finanzas.py"
set "DASH_PYTHON=.venv\Scripts\python.exe"
if exist "%DASH_PYTHON%" goto ejecutar
set "BASE_PYTHON=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not exist "%BASE_PYTHON%" set "BASE_PYTHON=python"
echo Preparando el entorno. Se requiere Python 3.12 o posterior.
"%BASE_PYTHON%" -m venv .venv
if errorlevel 1 goto error
"%DASH_PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 goto error
:ejecutar
echo Abre http://127.0.0.1:8080 en tu navegador.
echo Para detener el dashboard, pulsa Ctrl+C.
"%DASH_PYTHON%" "%DASH_APP%"
if errorlevel 1 goto error
exit /b 0
:error
echo No se pudo iniciar. Revisa el mensaje anterior y README.md.
pause
exit /b 1

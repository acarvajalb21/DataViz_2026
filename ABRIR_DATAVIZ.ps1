param(
    [ValidateSet('Jupyter','Shiny','Dash','Bookdown','JupyterBook','CompilarBookdown','CompilarJupyterBook','CompilarLibroCurso','PruebasShiny','PruebasModelo','RStudio','Publicados')]
    [string]$Herramienta = 'Publicados',
    [switch]$SinNavegador
)
$ErrorActionPreference = 'Stop'
$raiz = $PSScriptRoot
$runtime = Join-Path $raiz '.dataviz-runtime'
$proyecto = Join-Path $raiz 'proyecto_salud'
$python = Join-Path $raiz '.venv\Scripts\python.exe'
$rscript = 'C:\Program Files\R\R-4.6.2\bin\Rscript.exe'
$env:R_LIBS_USER = Join-Path $runtime 'r-library'
$env:RSTUDIO_PANDOC = Join-Path $env:LOCALAPPDATA 'Programs\RStudio\resources\app\bin\quarto\bin\tools'
$env:CNPV_DATOS = Join-Path $proyecto 'datos'
$env:JUPYTER_PATH = Join-Path $raiz '.venv\share\jupyter'
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
if (Test-Path -LiteralPath $chrome) { $env:BROWSER_PATH = $chrome }
Push-Location $raiz
try {
    switch ($Herramienta) {
        'Publicados' {
            @(
                'https://shiny-salud-atlantico-409319239507.us-east1.run.app/',
                'https://dataviz-salud-atlantico-409319239507.us-east1.run.app/',
                'https://acarvajalb21.github.io/EDAR/',
                'https://acarvajalb21.github.io/EDAPYTHON/'
            ) | ForEach-Object { Start-Process $_ }
        }
        'Jupyter' {
            $env:JUPYTER_CONFIG_DIR = Join-Path $runtime 'jupyter-config'
            $env:JUPYTER_RUNTIME_DIR = Join-Path $runtime 'jupyter-runtime'
            $env:IPYTHONDIR = Join-Path $runtime 'ipython'
            $env:JUPYTER_NO_CONFIG = '1'
            Get-ChildItem -LiteralPath $env:JUPYTER_RUNTIME_DIR -Filter 'jpserver-*.json' -ErrorAction SilentlyContinue | ForEach-Object {
                try {
                    $info = Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json
                    $uri = [uri]$info.url
                    if ($uri.IsLoopback -and $info.root_dir -eq $raiz) {
                        $estado = Invoke-RestMethod -Uri ($info.url + 'api/status') -Headers @{Authorization=('token ' + $info.token)} -TimeoutSec 3
                        if ($null -ne $estado.started) {
                            if (-not $SinNavegador) { Start-Process ($info.url + 'lab?token=' + $info.token) }
                            Write-Host ('Jupyter ya esta activo en ' + $info.url)
                            exit 0
                        }
                    }
                } catch { Write-Verbose 'Registro anterior de Jupyter sin servidor accesible.' }
            }
            $jupyterArgs = @('-m','jupyterlab','--ServerApp.ip=127.0.0.1','--ServerApp.port=8888',"--ServerApp.root_dir=$raiz")
            if ($SinNavegador) { $jupyterArgs += '--no-browser' }
            & $python @jupyterArgs
        }
        'Shiny' {
            $abrirBrowser = if ($SinNavegador) { 'FALSE' } else { 'TRUE' }
            & $rscript --vanilla -e "Sys.setlocale('LC_CTYPE', 'English_United States.utf8'); shiny::runApp('proyecto_salud/shiny_salud', host='127.0.0.1', port=3838, launch.browser=$abrirBrowser)"
        }
        'Dash' {
            $dashPython = Join-Path $proyecto 'dash_salud\.venv\Scripts\python.exe'
            Write-Host 'Abre http://127.0.0.1:8050 cuando aparezca el servidor.'
            Push-Location $proyecto
            try { & $dashPython -c "from dash_salud.app import app; app.run(host='127.0.0.1', port=8050, debug=False)" }
            finally { Pop-Location }
        }
        'Bookdown' {
            Write-Host 'Abre http://127.0.0.1:4321 para leer el libro compilado.'
            & $python -m http.server 4321 --bind 127.0.0.1 --directory (Join-Path $proyecto 'bookdown_salud\docs')
        }
        'JupyterBook' {
            $htmlDir = Join-Path $proyecto 'jupyter_salud\_build\html'
            if (-not (Test-Path -LiteralPath (Join-Path $htmlDir 'index.html'))) {
                $htmlDir = Join-Path $proyecto 'jupyter_salud\docs'
            }
            Write-Host 'Abre http://127.0.0.1:4322 para leer el Jupyter Book local.'
            & $python -m http.server 4322 --bind 127.0.0.1 --directory $htmlDir
        }
        'CompilarBookdown' {
            Push-Location (Join-Path $proyecto 'bookdown_salud')
            try { & $rscript --vanilla build_bookdown.R }
            finally { Pop-Location }
        }
        'CompilarJupyterBook' {
            $bookPython = Join-Path $proyecto 'jupyter_salud\.venv\Scripts\python.exe'
            $bookCli = Join-Path $proyecto 'jupyter_salud\.venv\Scripts\jupyter-book.exe'
            $bookDir = Join-Path $proyecto 'jupyter_salud'
            & $bookCli build $bookDir
            if ($LASTEXITCODE -ne 0) { throw 'Fallo la compilacion de Jupyter Book.' }
            & $bookPython (Join-Path $bookDir 'libro_interactivo.py') (Join-Path $bookDir '_build\html')
        }
        'CompilarLibroCurso' {
            $bookCli = Join-Path $raiz 'curso\jbook_dataviz_2026\.venv\Scripts\jupyter-book.exe'
            & $bookCli build (Join-Path $raiz 'curso\jbook_dataviz_2026\docs')
        }
        'PruebasShiny' {
            & $rscript --vanilla -e "Sys.setlocale('LC_CTYPE', 'English_United States.utf8'); setwd('proyecto_salud/shiny_salud'); source('pruebas/pruebas.R', encoding='UTF-8')"
        }
        'PruebasModelo' {
            $modelPython = Join-Path $proyecto 'ml_salud\.venv\Scripts\python.exe'
            Push-Location $proyecto
            try { & $modelPython -m unittest ml_salud.pruebas -v }
            finally { Pop-Location }
        }
        'RStudio' {
            $candidates = @(
                (Join-Path $env:LOCALAPPDATA 'Programs\RStudio\rstudio.exe'),
                (Join-Path $env:LOCALAPPDATA 'Programs\RStudio\bin\rstudio.exe'),
                'C:\Program Files\RStudio\rstudio.exe',
                'C:\Program Files\RStudio\bin\rstudio.exe'
            )
            $rstudio = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
            if (-not $rstudio) { throw 'No se encontro RStudio instalado.' }
            Start-Process -FilePath $rstudio -ArgumentList ('"' + (Join-Path $raiz 'DataViz_2026.Rproj') + '"')
        }
    }
    if ($LASTEXITCODE -and $Herramienta -notin 'Publicados','RStudio') { throw "El comando termino con codigo $LASTEXITCODE." }
}
finally { Pop-Location }

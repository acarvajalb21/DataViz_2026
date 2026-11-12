$ErrorActionPreference = 'Stop'
$env:CLOUDSDK_PYTHON = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'
$env:CLOUDSDK_CONFIG = Join-Path $PSScriptRoot '.dataviz-runtime\gcloud-config'
$gcloud = Join-Path $PSScriptRoot '.dataviz-runtime\google-cloud-sdk\bin\gcloud.cmd'
if (-not (Test-Path -LiteralPath $gcloud)) { throw 'Google Cloud CLI no esta instalado.' }
if ($args.Count -eq 0) { & $gcloud version }
else { & $gcloud @args }
if ($LASTEXITCODE -ne 0) { throw "gcloud termino con codigo $LASTEXITCODE." }

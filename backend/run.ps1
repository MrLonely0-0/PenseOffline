Param(
  [int]$Port = 8000
)
$ErrorActionPreference = "Stop"
Write-Host "[run] Verificando ambiente virtual..."
if (!(Test-Path .venv)) {
  Write-Host "[run] Criando venv..." -ForegroundColor Cyan
  python -m venv .venv
}
Write-Host "[run] Ativando venv..." -ForegroundColor Cyan
. .\.venv\Scripts\Activate.ps1
Write-Host "[run] Instalando dependências (silencioso)..." -ForegroundColor Cyan
pip install -r requirements.txt > $null
Write-Host "[run] Iniciando servidor na porta $Port" -ForegroundColor Green
Write-Host "[run] URL: http://127.0.0.1:$Port/" -ForegroundColor Green
python -m uvicorn app.main:app --reload --port $Port

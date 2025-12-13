# Script para iniciar servidor com acesso em rede local
# Permite que outros dispositivos na mesma rede acessem o aplicativo

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Pense Offline - Servidor de Rede Local" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Obter IP local da máquina
Write-Host "[1/4] Obtendo IP da máquina na rede local..." -ForegroundColor Yellow
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" }).IPAddress | Select-Object -First 1

if (-not $localIP) {
    Write-Host "AVISO: Não foi possível detectar IP de rede local automaticamente." -ForegroundColor Red
    Write-Host "Usando 0.0.0.0 (todas as interfaces de rede)" -ForegroundColor Yellow
    $localIP = "0.0.0.0"
}

Write-Host "   IP detectado: $localIP" -ForegroundColor Green
Write-Host ""

# Verificar/ativar ambiente virtual
Write-Host "[2/4] Verificando ambiente virtual Python..." -ForegroundColor Yellow
if (!(Test-Path .venv)) {
    Write-Host "   Criando ambiente virtual..." -ForegroundColor Cyan
    python -m venv .venv
}

Write-Host "   Ativando ambiente virtual..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Instalar dependências
Write-Host "[3/4] Verificando dependências..." -ForegroundColor Yellow
pip install -q -r requirements.txt

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  SERVIDOR INICIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Acesse de:" -ForegroundColor Cyan
Write-Host "  • Este computador: http://127.0.0.1:8000" -ForegroundColor White
if ($localIP -ne "0.0.0.0") {
    Write-Host "  • Outros dispositivos: http://${localIP}:8000" -ForegroundColor White
} else {
    Write-Host "  • Outros dispositivos: http://<IP-da-sua-maquina>:8000" -ForegroundColor White
}
Write-Host ""
Write-Host "IMPORTANTE:" -ForegroundColor Yellow
Write-Host "  1. Certifique-se de que o Firewall do Windows permite conexões na porta 8000" -ForegroundColor White
Write-Host "  2. O dispositivo deve estar na mesma rede Wi-Fi/local" -ForegroundColor White
Write-Host "  3. Para abrir o Firewall, execute:" -ForegroundColor White
Write-Host "     netsh advfirewall firewall add rule name=\"Pense Offline\" dir=in action=allow protocol=TCP localport=8000" -ForegroundColor Gray
Write-Host ""
Write-Host "[4/4] Iniciando servidor Uvicorn..." -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor escutando em todas as interfaces
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

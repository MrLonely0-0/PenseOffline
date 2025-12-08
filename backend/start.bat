@echo off
REM Script alternativo para iniciar o servidor (não requer ExecutionPolicy)
echo ============================================================
echo PENSE OFFLINE - Iniciando Backend
echo ============================================================

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale o Python seguindo o guia: SETUP_PYTHON.md
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Verificar/criar ambiente virtual
if not exist .venv (
    echo [INFO] Criando ambiente virtual...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado
) else (
    echo [OK] Ambiente virtual ja existe
)

echo.
echo [INFO] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo [INFO] Instalando/atualizando dependencias...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependencias
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas
echo.
echo ============================================================
echo Iniciando servidor em http://127.0.0.1:8000
echo Pressione Ctrl+C para parar
echo ============================================================
echo.

python -m uvicorn app.main:app --reload --port 8000

# Instalação do Python - PROBLEMA IDENTIFICADO

## ⚠️ PROBLEMA ENCONTRADO

O banco de dados não está operacional porque **Python não está instalado corretamente** no sistema.

### Sintomas Identificados:
1. ❌ Banco de dados `app.db` não existe
2. ❌ Python não encontrado no PATH
3. ❌ Apenas atalhos da Microsoft Store (não funcionam)
4. ❌ Servidor backend não pode ser iniciado

## 🔧 SOLUÇÃO - Instalar Python

### Opção 1: Instalação via winget (Recomendado)

Abra o PowerShell como **Administrador** e execute:

```powershell
# Instalar Python 3.12
winget install Python.Python.3.12

# Após instalação, feche e abra um novo PowerShell
# Verifique a instalação:
python --version
```

### Opção 2: Instalação Manual

1. Baixe Python 3.12 de: https://www.python.org/downloads/
2. **IMPORTANTE**: Durante a instalação, marque:
   - ✅ "Add Python to PATH"
   - ✅ "Install pip"
3. Após instalação, feche e abra um novo PowerShell
4. Verifique: `python --version`

### Opção 3: Desabilitar Atalhos da Microsoft Store

Se você já tem Python instalado mas não funciona:

1. Abra **Configurações do Windows**
2. Vá em **Aplicativos** → **Aplicativos e recursos**
3. Clique em **Aliases de execução de aplicativo**
4. **Desabilite** os atalhos:
   - ❌ App Installer python.exe
   - ❌ App Installer python3.exe

## 📋 Após Instalar Python

Execute os seguintes comandos na pasta backend:

```powershell
# Ir para o diretório backend
cd c:\PenseOffline\PenseOffline-main\backend

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor (criará o banco de dados automaticamente)
python -m uvicorn app.main:app --reload --port 8000
```

## ✅ Verificação de Sucesso

Após iniciar o servidor, você deve ver:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

E o arquivo `app.db` será criado automaticamente na pasta backend.

## 🔍 Teste o Banco de Dados

Acesse no navegador:
- http://127.0.0.1:8000/health

Deve retornar: `{"status":"ok"}`

## 📝 Notas Adicionais

- O banco SQLite será criado automaticamente na primeira execução
- As tabelas serão criadas pelo SQLModel no startup
- Se quiser popular com dados de teste, execute: `python seed.py`

## ⚠️ Problema com ExecutionPolicy do PowerShell

Se o script `run.ps1` não executar, use:

```powershell
# Temporariamente permitir execução (sessão atual)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# OU execute diretamente os comandos acima sem usar run.ps1
```

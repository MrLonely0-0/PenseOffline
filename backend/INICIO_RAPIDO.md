# 🔥 INÍCIO RÁPIDO - Backend Pense Offline

## ⚠️ PROBLEMA IDENTIFICADO

O banco de dados não está operacional porque **Python não está instalado corretamente**.

## 🚀 SOLUÇÃO RÁPIDA

### 1️⃣ Instalar Python

Escolha UMA das opções:

#### Opção A: Via winget (mais rápido)
```powershell
winget install Python.Python.3.12
```

#### Opção B: Manual
1. Baixe: https://www.python.org/downloads/
2. **MARQUE**: "Add Python to PATH" ✅
3. Instale normalmente

#### Opção C: Desabilitar atalhos da MS Store
Se você já instalou Python mas não funciona:
1. Configurações → Aplicativos → Aliases de execução
2. **Desative** python.exe e python3.exe

### 2️⃣ Iniciar Backend

Abra PowerShell na pasta `backend` e execute:

```powershell
# Use o script .bat (mais simples)
.\start.bat

# OU manualmente (se .bat não funcionar)
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 3️⃣ Verificar

✅ Abra: http://127.0.0.1:8000/health  
Deve retornar: `{"status":"ok"}`

## 🔍 Diagnóstico Automático

Para verificar se está tudo OK:

```powershell
python diagnose_db.py
```

Este script verifica:
- ✅ Python instalado
- ✅ Dependências instaladas
- ✅ Banco de dados funcionando
- ✅ Tabelas criadas
- ✅ Conexão OK

## 📁 Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `start.bat` | **USE ESTE** - Inicia o servidor automaticamente |
| `diagnose_db.py` | Verifica se está tudo funcionando |
| `SETUP_PYTHON.md` | Guia detalhado de instalação do Python |
| `CORREÇÕES_APLICADAS.md` | Lista completa de correções feitas |
| `.env.example` | Configurações do banco de dados |

## 📊 Logs Melhorados

Agora com mensagens claras:

```
============================================================
INICIANDO APLICAÇÃO PENSE OFFLINE
============================================================
INFO: Conectando ao banco de dados: sqlite:///./app.db
INFO: Usando SQLite - modo de desenvolvimento
INFO: ✓ Tabelas criadas com sucesso!
INFO: ✓ Banco de dados inicializado com sucesso
============================================================
```

## 🐛 Problemas Comuns

### "Python não foi encontrado"
➡️ Instale Python (veja passo 1️⃣)

### Script .ps1 não executa
➡️ Use `start.bat` ao invés de `run.ps1`

### "Access is denied"
➡️ Execute PowerShell como Administrador

### Porta 8000 em uso
```powershell
# Use outra porta
python -m uvicorn app.main:app --reload --port 8080
```

## 📚 Documentação Completa

Para mais detalhes, veja:
- `SETUP_PYTHON.md` - Instalação do Python
- `CORREÇÕES_APLICADAS.md` - O que foi corrigido
- `README.md` - Documentação completa da API

## ✅ Checklist

- [ ] Python instalado (`python --version` funciona)
- [ ] Executou `start.bat` ou comandos manuais
- [ ] Viu mensagem "Uvicorn running on http://127.0.0.1:8000"
- [ ] http://127.0.0.1:8000/health retorna OK
- [ ] Arquivo `app.db` foi criado na pasta backend

## 🎯 Próximos Passos

Com o backend funcionando:

1. **Popular com dados de teste**:
   ```powershell
   python seed.py
   ```

2. **Testar API**:
   ```powershell
   python test_api.py
   ```

3. **Ver endpoints disponíveis**:
   - GET /health - Status do servidor
   - POST /users/register - Criar usuário
   - POST /users/login - Login
   - GET /users/me - Perfil atual
   - E muito mais... (veja README.md completo)

## 📞 Ainda com Problemas?

Execute e copie a saída:
```powershell
python diagnose_db.py > diagnostico.txt
type diagnostico.txt
```

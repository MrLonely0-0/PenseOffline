# Quick Start — PenseOffline

Pré-requisitos
- Python 3.11+ (recomendado)
- `git`
- (Opcional) Docker para Postgres local

Rodando localmente (SQLite)

1. Abra um terminal PowerShell na pasta `backend`

```powershell
Set-Location 'c:\Users\Vinicius\Videos\PenseOffline-master\backend'
.\.venv\Scripts\Activate.ps1
$env:DATABASE_URL = "sqlite:///./app.db"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. Popular dados de exemplo (opcional):

```powershell
Set-Location 'c:\Users\Vinicius\Videos\PenseOffline-master\backend'
.\.venv\Scripts\Activate.ps1
$env:DATABASE_URL = "sqlite:///./app.db"
python seed.py
```

Frontend
- Os arquivos estáticos (HTML, CSS, JS) estão na raiz do repositório.
- `api-client.js` usa por padrão `http://127.0.0.1:8000`. Para apontar para um backend remoto, exporte `window.PENSEOFFLINE_API_URL` no HTML antes de carregar o cliente:

```html
<script>window.PENSEOFFLINE_API_URL = 'https://api.seudominio.com'</script>
<script src="/api-client.js"></script>
```

Manter banco fora do Git
- `.gitignore` já inclui `backend/app.db` e `.env`. Se o arquivo `backend/app.db` já estiver em commits anteriores, remova do índice com:

```powershell
git rm --cached backend/app.db
git commit -m "Remove local DB from repository"
```

Deploy (resumo)
- Publique o frontend (GitHub Pages ou outro serviço de arquivos estáticos).
- Hospede o backend (Render, Railway, Heroku, Cloud Run) e configure `DATABASE_URL` apontando para um Postgres gerenciado (Supabase é recomendado).
- Execute `schema_postgres.sql` e `seed_postgres.sql` no Postgres de produção.
- Defina `SECRET_KEY` e `DATABASE_URL` como variáveis de ambiente no serviço.

Contato
- Se quiser que eu automatize os passos acima (workflows, deploy), diga qual opção prefere: GitHub Actions + Pages para frontend, e Render/Railway para backend.
# 🚀 Pense Offline - Guia Rápido de Início

## Iniciar o Sistema em 30 Segundos

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
$env:DATABASE_URL = "sqlite:///./app.db"
python -m uvicorn app.main:app --reload --port 8000
```

✅ Servidor rodando em http://127.0.0.1:8000

---

## Acessar Aplicação

1. **Página Inicial:** http://127.0.0.1:8000/
2. **Login/Registro:** http://127.0.0.1:8000/login.html
3. **Dashboard:** http://127.0.0.1:8000/dashboard.html (após login)

---

## Teste Rápido

```
1. Registre: usuario "teste" + email "teste@test.com" + senha "123456"
2. Dashboard: Adicione 60 minutos sem tela (+10 pontos)
3. Desafios: Complete um desafio (+50 pontos)
4. Ranking: Veja sua posição
```

---

## Documentação Completa

| Arquivo | Descrição |
|---------|-----------|
| **FINAL_STATUS.md** | Resumo executivo completo |
| **INTEGRATION.md** | Arquitetura técnica detalhada |
| **TESTING.md** | Guia com 20+ testes |
| **DEPLOYMENT.md** | Deploy para Supabase/produção |

---

## Endpoints Principais

```
POST   /users/register           → Criar conta
POST   /users/login              → Fazer login
GET    /users/me                 → Dados do usuário
GET    /users                    → Ranking (lista todos)
PUT    /users/me                 → Editar perfil
DELETE /users/me                 → Deletar conta
POST   /rewards/add-time         → Registrar tempo sem tela
POST   /rewards/complete-challenge → Completar desafio
```

---

## Banco de Dados

Visualizar dados SQLite:
```powershell
cd backend
sqlite3 app.db
SELECT * FROM userprofile;
.quit
```

---

## Troubleshooting

### Servidor não inicia?
```powershell
Get-Process python | Stop-Process -Force
# Tentar novamente
```

### Erro de imports?
```powershell
cd backend
pip install -r requirements.txt
```

### Limpar banco de dados?
```powershell
cd backend
rm app.db
# Reiniciar servidor (vai recriar banco vazio)
```

---

## Status

- ✅ Backend: FastAPI (127.0.0.1:8000)
- ✅ Frontend: HTML + JavaScript
- ✅ Database: SQLite
- ✅ Auth: JWT Tokens
- ✅ Gamification: Pontos, Níveis, XP
- ✅ Integração: 100% Funcional

---

**Pronto para começar! 🎉**

Para suporte detalhado, leia a documentação nos arquivos `INTEGRATION.md` e `TESTING.md`.

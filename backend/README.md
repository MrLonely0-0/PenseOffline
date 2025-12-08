# Backend - Pense Offline

Instruções rápidas para preparar o ambiente de desenvolvimento do backend.

Pré-requisitos
- Python 3.10+ instalado e disponível no PATH
- Acesso à internet para instalar dependências (apenas na primeira vez)

Passos (PowerShell):

```powershell
Set-Location 'c:\Users\Vinicius\Videos\PenseOffline-master\backend'
.\run.ps1
```

O `run.ps1` cria um ambiente virtual `.venv`, instala as dependências listadas em
`requirements.txt` e inicia o servidor em `http://127.0.0.1:8000/` por padrão.

Se preferir executar manualmente:

```powershell
Set-Location 'c:\Users\Vinicius\Videos\PenseOffline-master\backend'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Variáveis de ambiente úteis
- `DATABASE_URL` (opcional) — URL do banco de dados. Por padrão o projeto usa SQLite `sqlite:///./app.db`.
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `FROM_EMAIL`, `FROM_NAME` — para envio de emails (opcional).

Arquivo de exemplo de variáveis de ambiente: `.env.example` (copie para `.env` se necessário).

Se ocorrerem erros durante `pip install`, verifique a versão do Python e instale build tools no Windows (ex.: `Build Tools for Visual Studio`) para compilar dependências nativas.

Problemas comuns
- `No module named uvicorn`: execute `pip install uvicorn` dentro do `.venv`.
- Erros com `sqlmodel`/`pydantic`: se ocorrerem incompatibilidades, reporte a versão do Python e o trace do erro.

Se quiser, posso tentar criar o `.venv` e instalar as dependências aqui (pode demorar e requer internet). Diga se quer que eu execute isso agora.
# Backend FastAPI (Desafio Positivo)

Backend simples com FastAPI + SQLModel + SQLite.

## Endpoints
- `GET /health` -> status
- `GET /profiles` -> lista perfis
- `POST /profiles` -> cria perfil
- `GET /profiles/{id}` -> obter perfil
- `PUT /profiles/{id}` -> atualizar perfil
- `DELETE /profiles/{id}` -> remover perfil

## Modelo `UserProfile`
```json
{
  "id": 1,
  "name": "Maria",
  "email": "maria@example.com",
  "phone": "+55 11 99999-0000",
  "created_at": "2025-11-26T12:00:00Z",
  "updated_at": "2025-11-26T12:00:00Z"
}
```

## Execução Rápida (Windows PowerShell)
### Usando script automatizado
Na pasta `backend`:
```powershell
cd backend
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
./run.ps1
```
Página: http://127.0.0.1:8000/
Docs: http://127.0.0.1:8000/docs

### Sem script (manual)
```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
Se a porta 8000 estiver ocupada, troque `--port 8001`.

## Banco de Dados
- Padrão: SQLite (`app.db` criado automaticamente)
- Para migrar para Postgres depois:
  - Instale: `pip install psycopg2-binary`
  - Exporte `DATABASE_URL=postgresql://usuario:senha@host:porta/nome_db`

## Teste rápido (PowerShell / curl)
```powershell
curl http://localhost:8000/health
curl -X POST http://localhost:8000/profiles -H "Content-Type: application/json" -d '{"name":"Joao","email":"joao@example.com"}'
curl http://localhost:8000/profiles
```

## Estrutura
```
backend/
  run.ps1
  start_server.bat
  requirements.txt
  .gitignore
  app/
    main.py
    models.py
    database.py
    seed.py
    templates/
      index.html
```

## Próximos passos opcionais
- Adicionar autenticação (JWT) usando `fastapi-users` ou `authlib`.
- Criar camada de serviços e testes automatizados.
- Dockerizar (adicionar Dockerfile)
- Trocar SQLite por Postgres em produção.
 - Adicionar cache (Redis) para listas grandes.
 - Adicionar paginação em `/profiles`.


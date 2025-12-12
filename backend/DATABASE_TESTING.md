# 🗄️ Guia de Testes de Banco de Dados - PenseOffline

Este guia explica como verificar se o código atual está funcionando corretamente com o banco de dados.

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Teste Rápido com SQLite](#teste-rápido-com-sqlite)
3. [Teste com PostgreSQL (Docker)](#teste-com-postgresql-docker)
4. [Teste da API](#teste-da-api)
5. [Resultados Esperados](#resultados-esperados)
6. [Troubleshooting](#troubleshooting)

## 🎯 Pré-requisitos

### Instalar Dependências Python

```bash
cd backend
pip install -r requirements.txt
```

### Dependências Adicionais para Testes

```bash
pip install httpx  # Para testes de API
```

## 🚀 Teste Rápido com SQLite

O teste mais simples para verificar se o banco de dados está funcionando:

```bash
cd backend
python3 verify_database.py
```

Este script:
- ✅ Cria o banco de dados SQLite (`app.db`)
- ✅ Cria todas as tabelas necessárias
- ✅ Testa operações CRUD para todos os modelos
- ✅ Verifica autenticação e hash de senhas
- ✅ Testa cálculo automático de níveis

### Saída Esperada

```
======================================================================
🔍 VERIFICAÇÃO DE BANCO DE DADOS - PenseOffline
======================================================================

📊 Banco de dados: sqlite:///./app.db

🧪 Executando testes...

--- Testando: Criação de Tabelas ---
✅ Criação de tabelas: Todas as tabelas foram criadas/verificadas

--- Testando: Conexão ---
✅ Conexão com banco de dados: URL: sqlite:///./app.db

...

======================================================================
✨ TODOS OS TESTES PASSARAM! O banco de dados está funcionando corretamente.
======================================================================
```

## 🐘 Teste com PostgreSQL (Docker)

Para testar com PostgreSQL usando Docker Compose:

### 1. Iniciar PostgreSQL

```bash
# Na raiz do projeto
docker compose up -d
```

Isso iniciará:
- PostgreSQL 15
- Usuário: `penseuser`
- Senha: `pensepass`
- Database: `pensedb`
- Porta: `5432`

### 2. Verificar se está rodando

```bash
docker compose ps
```

Deve mostrar:
```
NAME                IMAGE         COMMAND                  SERVICE   CREATED          STATUS          PORTS
penseoffline-db-1   postgres:15   "docker-entrypoint.s…"   db        X seconds ago    Up X seconds    0.0.0.0:5432->5432/tcp
```

### 3. Executar Testes com PostgreSQL

```bash
cd backend
DATABASE_URL="postgresql://penseuser:pensepass@localhost:5432/pensedb" python3 verify_database.py
```

### 4. Parar PostgreSQL (quando terminar)

```bash
docker compose down
```

### 5. Limpar dados (opcional)

Para remover completamente o banco de dados e começar do zero:

```bash
docker compose down -v  # Remove volumes também
```

## 🧪 Teste da API

Para testar a API completa com dados de exemplo:

### 1. Popular o banco com dados de teste

```bash
cd backend
python3 seed.py
```

Isso cria:
- 3 usuários: alice, bob, carol (senha: `password`)
- 2 comunidades: "Família Saudável", "Fitness Offline"
- 2 eventos de teste
- Memberships e histórico de XP

### 2. Executar testes da API

```bash
python3 test_api.py
```

Este script testa:
- ✅ Login com usuário alice
- ✅ Obter ranking de usuários
- ✅ Listar comunidades
- ✅ Entrar em comunidade
- ✅ Listar eventos
- ✅ Participar de evento

### Saída Esperada

```
STATUS: 200
BODY: {"access_token":"eyJ...","token_type":"bearer","user":{...}}

--- SMOKE TESTS ---
/profiles/ranking 200
[{"id":1,"username":"alice",...}]
/communities/ 200
[{"slug":"familia",...}]
/communities/1/join 200 {"message":"Already member"}
/events/ 200
/events/1/attend 200 {"message":"Event marked as attended","xp_awarded":20,"total_xp":40}
```

## ✅ Resultados Esperados

### Script de Verificação (`verify_database.py`)

O script executa **9 categorias de testes**:

1. **Criação de Tabelas** - Verifica que todas as tabelas são criadas corretamente
2. **Conexão** - Testa conexão com o banco de dados
3. **CRUD de Usuários** - Create, Read, Update, Delete de usuários
4. **CRUD de Comunidades** - Operações CRUD para comunidades
5. **CRUD de Eventos** - Operações CRUD para eventos
6. **Histórico de XP** - Registro e leitura de histórico de pontos
7. **Membros de Comunidade** - Associação de usuários a comunidades
8. **Hash de Senha** - Verificação de bcrypt
9. **Cálculo de Nível** - Cálculo automático baseado em pontos

**Total**: 24 testes individuais

### Código de Saída

- `0` = Todos os testes passaram ✅
- `1` = Alguns testes falharam ❌

## 📊 Diferenças SQLite vs PostgreSQL

### SQLite
- ✅ Mais simples, não requer instalação
- ✅ Arquivo único (`app.db`)
- ⚠️ Menos rígido com foreign keys (por padrão)
- 💡 Ideal para desenvolvimento local

### PostgreSQL
- ✅ Mais robusto para produção
- ✅ Melhor performance com muitos usuários
- ✅ Enforce rigoroso de foreign keys
- ✅ Suporte a tipos de dados avançados
- 💡 Ideal para deploy (Supabase, Heroku, Railway)

## 🔧 Troubleshooting

### Erro: "no such table: userprofile"

**Causa**: Banco de dados não foi inicializado

**Solução**: O script `verify_database.py` inicializa automaticamente. Se usar outro script:

```python
from app.database import init_db
init_db()
```

### Erro: "ModuleNotFoundError: No module named 'httpx'"

**Causa**: Dependência para testes não instalada

**Solução**:
```bash
pip install httpx
```

### Erro: "connection refused" (PostgreSQL)

**Causa**: PostgreSQL não está rodando

**Solução**:
```bash
docker compose up -d
sleep 5  # Esperar PostgreSQL iniciar
```

### Erro: "password authentication failed"

**Causa**: Credenciais incorretas no DATABASE_URL

**Solução**: Verificar credenciais no `docker-compose.yml`:
```yaml
POSTGRES_USER: penseuser
POSTGRES_PASSWORD: pensepass
POSTGRES_DB: pensedb
```

### Foreign Key Violations (PostgreSQL)

**Causa**: Tentando deletar registro que tem dependências

**Solução**: Deletar na ordem correta:
1. Registros dependentes (XPHistory, CommunityMembership)
2. Tabelas referenciadas (UserProfile, Community, Event)

## 🎓 Modelos de Dados Testados

### UserProfile
- username (único)
- email (único)
- password_hash (bcrypt)
- pontos, nivel, xp_total
- tempo_sem_tela_minutos
- desafios_completados
- dias_consecutivos

### Community
- slug (único)
- name
- description
- visibility (public/private)
- owner_id

### Event
- creator_id
- community_id (opcional)
- title, description
- xp_reward
- starts_at, ends_at

### XPHistory
- user_id
- event_id (opcional)
- type (manual, event, challenge)
- xp_amount
- meta (JSON)

### CommunityMembership
- community_id
- user_id
- role (member/owner)
- joined_at

## 🌐 Conexões de Banco de Dados Suportadas

### SQLite (padrão)
```bash
DATABASE_URL="sqlite:///./app.db" python3 verify_database.py
```

### PostgreSQL Local
```bash
DATABASE_URL="postgresql://user:pass@localhost:5432/dbname" python3 verify_database.py
```

### Supabase
```bash
DATABASE_URL="postgresql://postgres:pass@db.PROJECT_ID.supabase.co:5432/postgres" python3 verify_database.py
```

## 📝 Notas Importantes

1. **Sempre instale as dependências** antes de executar os testes
2. **SQLite é suficiente** para desenvolvimento local
3. **PostgreSQL é recomendado** para produção
4. O script `verify_database.py` **não afeta dados existentes** - ele cria e deleta apenas dados de teste
5. Use `seed.py` para popular o banco com **dados iniciais realistas**

## 🎉 Conclusão

Se todos os testes passaram (✨ **24/24** ✅), o código está funcionando corretamente com o banco de dados!

Você pode então:
- Iniciar o servidor FastAPI: `uvicorn app.main:app --reload`
- Acessar a documentação: `http://localhost:8000/docs`
- Testar o frontend com o backend rodando

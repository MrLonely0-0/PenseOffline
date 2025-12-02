# 📵 Desafio Positivo - Plataforma de Recompensas por Redução de Tempo de Tela

## 🎯 Visão Geral

Sistema completo de gamificação para incentivar pessoas a reduzirem sua dependência digital, oferecendo pontos, níveis e desafios por tempo longe das telas.

## ✅ Funcionalidades Implementadas

### Backend (FastAPI)
- ✅ Sistema de autenticação JWT com bcrypt
- ✅ CRUD completo de usuários
- ✅ Sistema de pontos e níveis (100 pontos = 1 nível)
- ✅ Registro de tempo sem tela (10 pts/hora)
- ✅ Sistema de desafios com pontuações variadas
- ✅ Ranking global de usuários
- ✅ Estatísticas da plataforma
- ✅ Email de boas-vindas (simulado em dev)
- ✅ CORS configurado para frontend

### Frontend (HTML/CSS/JS)
- ✅ `index.html` - Homepage com tema de dependência digital
- ✅ `login.html` - Login/Cadastro com tabs
- ✅ `dashboard.html` - Dashboard pessoal do usuário
- ✅ `desafios.html` - 9 desafios disponíveis
- ✅ `ranking.html` - Leaderboard top 100
- ✅ Design responsivo com Bootstrap 3
- ✅ Integração completa com API

## 🗂️ Estrutura do Projeto

```
desafio-positivo/
├── backend/
│   ├── .venv/                    # Ambiente virtual Python
│   ├── app/
│   │   ├── main.py              # Aplicação FastAPI + endpoints
│   │   ├── models.py            # Modelos SQLModel (UserProfile)
│   │   ├── auth.py              # Autenticação JWT + bcrypt
│   │   ├── database.py          # Configuração SQLite
│   │   └── email_service.py     # Serviço de email
│   ├── app.db                   # Banco SQLite
│   └── requirements.txt         # Dependências Python
├── index.html                   # Homepage
├── login.html                   # Login/Registro
├── dashboard.html               # Dashboard pessoal
├── desafios.html                # Página de desafios
├── ranking.html                 # Ranking/Leaderboard
├── perfil.html                  # Perfil do usuário
└── web-files/                   # Assets (CSS, imagens)
```

## 🚀 Como Executar

### 1. Backend (porta 8000)

```powershell
cd backend
.\.venv\Scripts\uvicorn.exe app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Frontend (porta 8080)

```powershell
cd desafio-positivo
python -m http.server 8080
```

### 3. Acessar

- **Frontend**: http://127.0.0.1:8080
- **Backend API**: http://127.0.0.1:8000
- **Documentação API**: http://127.0.0.1:8000/docs

## 📊 Modelo de Dados

```python
class UserProfile:
    id: int
    username: str              # Único, para login
    password_hash: str         # Senha criptografada (bcrypt)
    name: str                  # Nome completo
    email: str                 # Email único
    phone: str                 # Telefone (XX) XXXXX-XXXX
    pontos: int = 0           # Pontos acumulados
    nivel: int = 1            # Nível (auto-calculado)
    tempo_sem_tela_minutos: int = 0
    desafios_completados: int = 0
    dias_consecutivos: int = 0
    ultimo_acesso: datetime
    created_at: datetime
    updated_at: datetime
```

## 🔌 Endpoints da API

### Autenticação
- `POST /auth/register` - Criar conta
- `POST /auth/login` - Login
- `GET /auth/me` - Perfil atual (protegido)

### Perfis
- `GET /profiles/ranking` - Top 100 usuários (protegido)
- `GET /profiles/{id}` - Perfil público (protegido)
- `PUT /profiles/me` - Atualizar perfil (protegido)

### Recompensas
- `POST /rewards/add-time` - Registrar tempo sem tela (protegido)
- `POST /rewards/complete-challenge` - Completar desafio (protegido)

### Estatísticas
- `GET /stats/global` - Estatísticas da plataforma

## 🎮 Sistema de Gamificação

### Pontos
- **10 pontos** por hora sem tela registrada
- **50-1000 pontos** por desafio completado

### Níveis
- Cada **100 pontos** = 1 nível
- Cálculo automático: `nivel = pontos // 100 + 1`

### Desafios Disponíveis

| Desafio | Pontos |
|---------|--------|
| 1 Hora Sem Redes Sociais | 50 |
| 3 Horas Sem Celular | 150 |
| Noite Sem Telas | 100 |
| Dia de Leitura | 200 |
| Exercício ao Ar Livre | 250 |
| Hobby Criativo | 300 |
| Tempo em Família | 350 |
| Manhã Desconectada | 400 |
| **24h Sem Telas** | **1000** |

## 🔐 Segurança

- ✅ Senhas hasheadas com bcrypt
- ✅ JWT tokens com expiração de 24h
- ✅ Rotas protegidas com middleware
- ✅ CORS configurado para localhost
- ✅ Validação de dados com Pydantic

## 📦 Dependências

### Backend
```txt
fastapi==0.115.0
uvicorn==0.30.0
sqlmodel==0.0.16
pydantic==2.6.4
python-jose[cryptography]
passlib[bcrypt]
python-multipart
aiosmtplib
email-validator
```

### Frontend
- Bootstrap 3.3.7
- jQuery 3.6.0
- Vanilla JavaScript (ES6+)

## 🎨 Design

- Tema: Dependência digital e bem-estar
- Cores: Gradiente roxo (#667eea → #764ba2)
- Ícones: Emojis nativos
- Responsivo: Mobile-first com Bootstrap

## 📝 Próximos Passos (Opcional)

- [ ] Adicionar sistema de badges/conquistas
- [ ] Implementar streak tracking (dias consecutivos)
- [ ] Gráficos de progresso com Chart.js
- [ ] Notificações push
- [ ] Sistema de amigos/grupos
- [ ] Export de dados (CSV/PDF)
- [ ] Modo escuro
- [ ] Integração com Google/Facebook login
- [ ] Deploy em produção (Heroku/Railway/Vercel)

## 🐛 Troubleshooting

### Erro ao criar conta
- Verificar se backend está rodando na porta 8000
- Verificar CORS no navegador (F12 > Console)
- Senha muito longa truncada em 72 bytes (limitação bcrypt)

### Frontend não carrega
- Verificar se servidor HTTP está na porta 8080
- Verificar paths dos arquivos CSS/JS
- Limpar cache do navegador (Ctrl+Shift+R)

### Banco de dados corrompido
```powershell
cd backend
Remove-Item app.db -Force
# Reiniciar backend (recria tabelas automaticamente)
```

## 📄 Licença

Projeto educacional - Livre para uso e modificação.

---

**Desenvolvido com ❤️ para combater a dependência digital**

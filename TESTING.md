# 🧪 Guia de Teste - Pense Offline

## Verificação Rápida do Sistema

### 1. **Verificar Status do Servidor**

```bash
# Terminal (PowerShell)
$env:DATABASE_URL = "sqlite:///./app.db"
cd backend
.\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

**Esperado:** Mensagem `Application startup complete`

### 2. **Teste Manual via Browser**

1. Abra http://127.0.0.1:8000/health
   - **Esperado:** Response `{"status": "ok"}`

2. Abra http://127.0.0.1:8000/
   - **Esperado:** Página inicial da Pense Offline

## Fluxo de Teste Completo

### **Fase 1: Registro de Novo Usuário**

1. Acesse http://127.0.0.1:8000/login.html
2. Clique na aba **"Cadastrar"**
3. Preencha o formulário:
   - **Nome de usuário:** `testuser001` (ou qualquer nome único)
   - **Email:** `test@example.com` (deve ser único)
   - **Nome completo:** `Test User`
   - **Senha:** `123456` (mínimo 6 caracteres)
4. Clique em **"Criar Conta"**

**Esperado:**
- ✅ Mensagem: "Conta criada com sucesso!"
- ✅ Redirecionamento para `/dashboard.html`
- ✅ Exibição do nome do usuário no dashboard

### **Fase 2: Login com Credenciais**

1. Acesse http://127.0.0.1:8000/login.html
2. Clique na aba **"Entrar"**
3. Preencha com credenciais anteriores:
   - **Usuário:** `testuser001`
   - **Senha:** `123456`
4. Clique em **"Entrar"**

**Esperado:**
- ✅ Mensagem: "Login realizado com sucesso!"
- ✅ Redirecionamento para `/dashboard.html`
- ✅ Exibição de dados: pontos, nível, tempo sem tela, dias consecutivos

### **Fase 3: Dashboard - Registrar Tempo Sem Tela**

1. No dashboard, seção **"Registrar Tempo Sem Tela"**
2. Insira **30** minutos
3. Clique em **"Adicionar Tempo (+10 pontos por hora)"**

**Esperado:**
- ✅ Alerta: "✅ Tempo adicionado! 🎉 Você ganhou 5 pontos!"
- ✅ Atualização dos pontos no dashboard
- ✅ Atualização da barra de progresso

### **Fase 4: Completar Desafios**

1. Acesse http://127.0.0.1:8000/desafios.html
2. Encontre o desafio **"1 Hora Sem Redes Sociais" (+50 pontos)**
3. Clique em **"Completar Desafio"**
4. Confirme a caixa de diálogo

**Esperado:**
- ✅ Alerta: "🎉 Parabéns! ... Você ganhou 50 pontos!"
- ✅ Atualização de pontos

### **Fase 5: Visualizar Perfil**

1. Acesse http://127.0.0.1:8000/perfil.html
2. Verifique informações exibidas:
   - ID, Nome, Email, Telefone
   - Timestamps (Criado em, Atualizado em)
   - Estatísticas: Pontos, Nível, XP Total, etc.
3. Clique em **"Ver Histórico de XP"**

**Esperado:**
- ✅ Modal exibindo histórico de transações XP
- ✅ Dados atualizados refletindo as ações anteriores

### **Fase 6: Editar Perfil**

1. Em `/perfil.html`, clique em **"Editar Perfil"**
2. Altere o **Nome completo** para algo novo
3. Clique em **"Salvar Alterações"**

**Esperado:**
- ✅ Mensagem: "Perfil atualizado com sucesso!"
- ✅ Atualização dos dados exibidos

### **Fase 7: Ranking Global**

1. Acesse http://127.0.0.1:8000/ranking.html
2. Verifique ranking ordenado por pontos
3. Procure seu usuário na lista

**Esperado:**
- ✅ Listagem de usuários ordenada por pontos decrescentes
- ✅ Seção "Sua Posição" mostrando ranking atual
- ✅ Medalhas (🥇🥈🥉) para top 3

### **Fase 8: Logout**

1. Em qualquer página autenticada, clique em **"Sair"** na navbar
2. Verifique redirecionamento para `/login.html`

**Esperado:**
- ✅ Token removido do localStorage
- ✅ Impossível acessar `/dashboard.html` sem login (redirecionamento automático)

## Testes de Validação

### **Validação de Username**

1. Tente registrar com:
   - ✗ Username com **menos de 3 caracteres:** `ab`
   - ✗ Username com **caracteres inválidos:** `user@123` ou `usuário`
   - ✗ Username **duplicado:** tente com `testuser001` novamente
   - ✓ Username **válido:** `test_user-123`

### **Validação de Email**

1. Tente registrar com:
   - ✗ Email **inválido:** `invalid.email`
   - ✗ Email **duplicado:** tente com `test@example.com` novamente
   - ✓ Email **válido:** `newuser@domain.com`

### **Validação de Senha**

1. Tente registrar com:
   - ✗ Senha com **menos de 6 caracteres:** `12345`
   - ✓ Senha **válida:** `minhaSenha123`

### **Proteção de Rotas (Auth)**

1. Abra DevTools (F12 → Console)
2. Delete token do localStorage:
   ```javascript
   localStorage.removeItem('pensOffline_token')
   ```
3. Recarregue a página `/dashboard.html`

**Esperado:**
- ✅ Redirecionamento automático para `/login.html`

## Teste de API Direta

### **Usando cURL no PowerShell**

#### Registrar novo usuário:
```powershell
$body = @{
    username = "apitest"
    email = "apitest@example.com"
    name = "API Test"
    password = "123456"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/users/register" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body
```

#### Fazer login:
```powershell
$body = @{
    username = "apitest"
    password = "123456"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/users/login" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body `
  -UseBasicParsing

$token = ($response.Content | ConvertFrom-Json).access_token
$token
```

#### Obter dados do usuário:
```powershell
$token = "seu_token_aqui"

Invoke-WebRequest -Uri "http://127.0.0.1:8000/users/me" `
  -Headers @{"Authorization"="Bearer $token"} `
  -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

## Checklist de Status

- [ ] Servidor FastAPI rodando em http://127.0.0.1:8000
- [ ] Endpoint `/health` respondendo com status ok
- [ ] Página inicial (`/`) carregando
- [ ] Registro de novo usuário funcionando
- [ ] Login funcionando com credenciais corretas
- [ ] Dashboard exibindo dados do usuário
- [ ] Registrar tempo sem tela adicionando pontos
- [ ] Completar desafios adicionando pontos
- [ ] Perfil exibindo estatísticas completas
- [ ] Edição de perfil funcionando
- [ ] Ranking exibindo usuários ordenados
- [ ] Logout removendo token e redirecionando
- [ ] Proteção de rotas funcionando (redirecionamento sem token)
- [ ] Validações de username/email/senha funcionando

## Banco de Dados

### **Verificar dados SQLite**

```powershell
# Acessar SQLite CLI
cd backend
sqlite3 app.db

# Listar tabelas
.tables

# Contar usuários
SELECT COUNT(*) FROM userprofile;

# Listar todos os usuários
SELECT id, username, email, name, pontos, nivel FROM userprofile;

# Ver histórico de XP
SELECT * FROM xphistory LIMIT 10;

# Sair
.quit
```

## Troubleshooting

### **Problema: Erro 401 Unauthorized**
- **Causa:** Token expirado ou inválido
- **Solução:** Fazer logout e login novamente

### **Problema: 409 Conflict (Username/Email duplicados)**
- **Causa:** Username ou email já existe
- **Solução:** Usar valores únicos

### **Problema: 422 Unprocessable Entity**
- **Causa:** Validação falhou (username/email/senha inválidos)
- **Solução:** Verificar formato dos dados

### **Problema: Backend não responde**
- **Causa:** Servidor desligou
- **Solução:** Reiniciar com comando acima

### **Problema: Página branca/Erro 404**
- **Causa:** Arquivo HTML não encontrado
- **Solução:** Verificar se arquivo existe em `c:\Users\Vinicius\Videos\PenseOffline-master\`

## Próximas Etapas

- [ ] Integração com Supabase (quando tiver conexão de rede)
- [ ] Testes de carga (múltiplos usuários simultâneos)
- [ ] Integração com React Prototype (opcional)
- [ ] Deploy para produção

# 🚀 Guia Completo de Deploy no Render

## 📋 Pré-requisitos

- ✅ Conta no GitHub (já tem, com o repositório)
- ✅ Arquivo `render.yaml` configurado (já existe no projeto)

## 🎯 Passo a Passo

### 1. Criar Conta no Render

1. Acesse: https://render.com
2. Clique em **"Get Started"** ou **"Sign Up"**
3. Escolha uma das opções:
   - **Sign up with GitHub** (Recomendado - mais rápido)
   - Sign up with GitLab
   - Sign up with Google
   - Email/senha

4. Se escolher GitHub, autorize o Render a acessar seus repositórios

### 2. Conectar Repositório

1. No dashboard do Render, clique em **"New +"**
2. Selecione **"Blueprint"** (para usar o render.yaml)
3. Conecte seu repositório GitHub:
   - Se ainda não conectou, clique em **"Connect GitHub"**
   - Autorize o Render
   - Selecione o repositório: **MrLonely0-0/PenseOffline**

### 3. Configurar as Variáveis de Ambiente

O Render vai detectar automaticamente o `render.yaml`, mas você precisa adicionar as variáveis:

1. **DATABASE_URL** - String de conexão do PostgreSQL
2. **SECRET_KEY** - Chave secreta do Django/FastAPI
3. **SUPABASE_URL** (se usar Supabase)
4. **SUPABASE_KEY** (se usar Supabase)

#### Opção A: Usar PostgreSQL do Render (Recomendado)

1. No Render, clique em **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `desafio-positivo-db`
   - **Database**: `desafio_positivo`
   - **User**: (gerado automaticamente)
   - **Region**: Oregon (mesmo da aplicação)
   - **Plan**: Free
3. Clique em **"Create Database"**
4. Copie a **Internal Database URL** (algo como: `postgresql://user:pass@host/db`)
5. Adicione no serviço web como variável `DATABASE_URL`

#### Opção B: Usar Supabase

Se preferir usar o Supabase que já está configurado:

1. Acesse seu projeto no Supabase
2. Vá em Settings → Database
3. Copie a **Connection String** (formato URI)
4. Adicione como `DATABASE_URL`

### 4. Deploy Automático

1. Após conectar o repositório, o Render vai:
   - ✅ Detectar o `render.yaml`
   - ✅ Criar o serviço web automaticamente
   - ✅ Iniciar o build
   - ✅ Fazer o deploy

2. Acompanhe os logs em tempo real no dashboard

### 5. Acessar a Aplicação

Após o deploy bem-sucedido:

1. O Render fornecerá uma URL: `https://desafio-positivo-backend.onrender.com`
2. Teste os endpoints:
   - Health check: `https://desafio-positivo-backend.onrender.com/api/health/`
   - Docs: `https://desafio-positivo-backend.onrender.com/docs`

## ⚠️ Problemas Comuns e Soluções

### Problema 1: Build falha por falta de Dockerfile

**Solução**: Criar Dockerfile no diretório backend

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Problema 2: Serviço não inicia

**Causa**: Variáveis de ambiente faltando

**Solução**: 
1. Vá em Dashboard → Seu serviço → Environment
2. Adicione todas as variáveis necessárias
3. Clique em "Save Changes"
4. O serviço vai reiniciar automaticamente

### Problema 3: Database connection error

**Causa**: DATABASE_URL incorreta ou banco não criado

**Solução**:
1. Verifique se o PostgreSQL está rodando
2. Confirme que a URL está correta
3. Execute as migrações manualmente:
   - No Render, vá em Shell
   - Execute: `python -m alembic upgrade head`

### Problema 4: Free tier dorme após 15 minutos

**Comportamento normal**: O plano free do Render coloca o serviço em sleep após 15 minutos de inatividade

**Impacto**: Primeira requisição após sleep pode demorar 30-60 segundos

**Soluções**:
- Aceitar o comportamento (é grátis!)
- Fazer upgrade para plano pago ($7/mês)
- Usar um serviço de "keep-alive" como UptimeRobot

## 🔧 Configuração Avançada

### Adicionar Domínio Customizado

1. No dashboard do serviço, vá em **"Settings"**
2. Clique em **"Add Custom Domain"**
3. Adicione seu domínio
4. Configure o DNS conforme instruções do Render

### Configurar CI/CD

O deploy automático já está ativo! Toda vez que você fizer push na branch `main`, o Render vai:

1. ✅ Detectar o push
2. ✅ Fazer pull do código
3. ✅ Buildar a aplicação
4. ✅ Fazer deploy automático

### Logs e Monitoramento

1. **Ver logs em tempo real**:
   - Dashboard → Seu serviço → Logs

2. **Eventos de deploy**:
   - Dashboard → Seu serviço → Events

3. **Métricas**:
   - Dashboard → Seu serviço → Metrics (plano pago)

## 💰 Custos

### Plano Free
- ✅ 750 horas/mês de runtime
- ✅ 512MB RAM
- ✅ Deploy automático
- ⚠️ Sleep após 15 min de inatividade
- ⚠️ Limite de 100GB bandwidth/mês

### Plano Starter ($7/mês)
- ✅ Sem sleep
- ✅ 512MB RAM
- ✅ Deploy automático
- ✅ 100GB bandwidth

## 🎓 Recursos Úteis

- 📖 [Documentação Oficial do Render](https://render.com/docs)
- 💬 [Comunidade Render](https://community.render.com)
- 🐛 [Status do Render](https://status.render.com)

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs no dashboard do Render
2. Consulte a [documentação](https://render.com/docs)
3. Pergunte na [comunidade](https://community.render.com)
4. Abra um ticket no [suporte do Render](https://render.com/support)

---

**🎉 Pronto!** Seu backend estará rodando no Render com deploy automático configurado!

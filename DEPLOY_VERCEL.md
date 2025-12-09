# 🚀 Deploy no Vercel + Supabase - Guia Completo

## ✅ Arquitetura Atual
- **Frontend**: HTML/CSS/JS hospedado no Vercel
- **Backend**: FastAPI (Python) hospedado no Vercel (serverless)
- **Banco de Dados**: PostgreSQL no Supabase

---

## 📋 Passo a Passo

### **1️⃣ Configurar Variáveis de Ambiente no Vercel**

1. Acesse: https://vercel.com/dashboard
2. Selecione seu projeto **PenseOffline**
3. Vá em **Settings** → **Environment Variables**
4. Adicione as seguintes variáveis:

#### Variáveis Obrigatórias:

```bash
# URL do Banco de Dados Supabase
DATABASE_URL
postgresql://postgres.libchjoccyjblobxjkeq:[SUA_SENHA]@aws-0-us-east-1.pooler.supabase.com:6543/postgres

# Chave secreta JWT (gere uma aleatória de 32+ caracteres)
SECRET_KEY
[cole aqui uma chave secreta aleatória]

# Python Path
PYTHONPATH
backend
```

**📌 Como pegar a DATABASE_URL do Supabase:**
1. Acesse: https://app.supabase.com/project/libchjoccyjblobxjkeq/settings/database
2. Role até **Connection String** → **Connection Pooling**
3. Copie a URL que começa com `postgresql://`
4. Substitua `[YOUR-PASSWORD]` pela sua senha do Supabase

**📌 Como gerar SECRET_KEY:**
Rode no seu terminal local:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### **2️⃣ Fazer Deploy das Alterações**

No terminal, execute:

```bash
# Adicionar todos os arquivos modificados
git add .

# Commit
git commit -m "fix: configurar Vercel + Supabase + CORS"

# Push para GitHub (vai triggar deploy automático no Vercel)
git push origin main
```

**Aguarde 2-3 minutos** para o Vercel fazer o deploy.

---

### **3️⃣ Testar a Aplicação**

1. Acesse: https://pense-offline.vercel.app
2. Tente fazer cadastro ou login
3. Verifique o console do navegador (F12) para ver se não há erros

**Teste a API diretamente:**
```bash
curl https://pense-offline.vercel.app/api/health
```

Deve retornar: `{"status":"ok"}`

---

## 🔍 Troubleshooting

### ❌ Erro: "NetworkError when attempting to fetch resource"

**Causa:** O frontend está tentando acessar `localhost` em vez da API no Vercel.

**Solução:** ✅ Já corrigido! O `api-client.js` agora usa `/api` quando em produção.

---

### ❌ Erro: CORS blocked

**Causa:** O backend não está permitindo requisições do Vercel.

**Solução:** ✅ Já corrigido! Adicionei `*` temporariamente no CORS para debug.

**Depois que funcionar**, remova o `"*"` do CORS em `backend/app/main.py`:

```python
allow_origins=[
    "https://pense-offline.vercel.app",
    "https://*.vercel.app",
],
```

---

### ❌ Erro: 500 Internal Server Error

**Causa:** Variáveis de ambiente não configuradas no Vercel.

**Solução:**
1. Verifique se `DATABASE_URL` e `SECRET_KEY` estão nas Environment Variables
2. Faça redeploy: Vercel Dashboard → Deployments → ... (três pontos) → Redeploy

---

### ❌ Backend retorna 404

**Causa:** As rotas da API estão em `/users/login` mas o Vercel está redirecionando para `/api/...`

**Solução:** Atualizar as rotas no frontend:

Se der erro, me avise que ajusto as rotas!

---

### ❌ Banco de dados vazio / tabelas não existem

**Causa:** Schema não foi aplicado no Supabase.

**Solução:**
1. Acesse: https://app.supabase.com/project/libchjoccyjblobxjkeq/editor
2. Clique em **SQL Editor** (no menu lateral)
3. Clique em **New Query**
4. Cole o conteúdo de `backend/schema_postgres.sql`
5. Clique em **Run**
6. Repita para `backend/seed_postgres.sql` (dados iniciais)

---

## 📱 Checklist Final

- [ ] DATABASE_URL configurado no Vercel
- [ ] SECRET_KEY configurado no Vercel
- [ ] PYTHONPATH=backend configurado no Vercel
- [ ] Git push realizado
- [ ] Deploy finalizado no Vercel (sem erros)
- [ ] Schema aplicado no Supabase
- [ ] Teste de `/api/health` funcionando
- [ ] Login/cadastro funcionando no site

---

## 🎯 URLs Importantes

- **Site**: https://pense-offline.vercel.app
- **API Health**: https://pense-offline.vercel.app/api/health
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Supabase Dashboard**: https://app.supabase.com/project/libchjoccyjblobxjkeq

---

## 🔐 Segurança

⚠️ **IMPORTANTE**: O arquivo `backend/SUPABASE_DEPLOY.md` contém sua senha do banco de dados!

```bash
# Remover senha do repositório
git rm backend/SUPABASE_DEPLOY.md
git commit -m "chore: remover credenciais do repositório"
git push
```

Mantenha as credenciais **SOMENTE** nas Environment Variables do Vercel.

---

**Pronto! Agora seu site está funcionando no Vercel com Supabase! 🎉**

Qualquer erro, verifique os logs em:
- **Vercel**: Dashboard → Seu projeto → Deployments → Ver logs
- **Supabase**: Dashboard → Logs

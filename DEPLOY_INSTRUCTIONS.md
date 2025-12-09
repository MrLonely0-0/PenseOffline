# 🚀 Guia de Deploy - Pense Offline

## Resumo da Arquitetura
- **Frontend**: Vercel (hospedagem estática)
- **Backend**: Render (API FastAPI)
- **Banco de Dados**: Render PostgreSQL

---

## 1️⃣ Configurar Banco de Dados no Render

1. Acesse: https://dashboard.render.com
2. Clique em **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `penseoffline-db`
   - **Database**: `penseoffline`
   - **Region**: Oregon (ou mais próximo)
   - **Plan**: Free
4. Clique em **"Create Database"**
5. Aguarde provisionar (2-3 minutos)
6. **Copie a "Internal Database URL"** (formato: `postgresql://user:pass@host/db`)

---

## 2️⃣ Configurar Backend no Render

### A) Criar Web Service

1. Clique em **"New +"** → **"Web Service"**
2. Conecte seu GitHub: `MrLonely0-0/PenseOffline`
3. Configure:
   - **Name**: `penseoffline-backend`
   - **Region**: Oregon (mesma do banco)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Docker`
   - **Plan**: Free
   - **Auto-Deploy**: Yes

### B) Adicionar Variáveis de Ambiente

No campo **"Environment Variables"**, adicione:

```bash
DATABASE_URL
postgresql://[copie do passo 1]

SECRET_KEY
[gere uma chave aleatória de 32+ caracteres]

ALLOWED_ORIGINS
https://pense-offline.vercel.app

PYTHON_VERSION
3.11.0
```

**Dica para gerar SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### C) Criar Serviço

1. Clique em **"Create Web Service"**
2. Aguarde o primeiro deploy (5-10 minutos)
3. **Copie a URL do serviço**: `https://penseoffline-backend.onrender.com`

---

## 3️⃣ Atualizar Frontend (URL da API)

### Opção A: Atualizar no código (recomendado)

Edite o arquivo `api-client.js` linha 8:

```javascript
: "https://penseoffline-backend.onrender.com";  // ← Coloque sua URL do Render aqui
```

### Opção B: Configurar variável no Vercel

1. Acesse: https://vercel.com/dashboard
2. Selecione seu projeto
3. **Settings** → **Environment Variables**
4. Adicione:
   - **Key**: `PENSEOFFLINE_API_URL`
   - **Value**: `https://penseoffline-backend.onrender.com`
   - **Environments**: Production, Preview, Development
5. Clique em **Save**

Depois adicione no `index.html` (antes de carregar `api-client.js`):

```html
<script>
  window.PENSEOFFLINE_API_URL = 'https://penseoffline-backend.onrender.com';
</script>
<script src="/api-client.js"></script>
```

---

## 4️⃣ Fazer Deploy das Alterações

```bash
# Commit das alterações de CORS e URL
git add .
git commit -m "fix: configurar URLs de produção e CORS para Vercel"
git push origin main
```

Isso vai triggar:
- ✅ Deploy automático no Render (backend)
- ✅ Deploy automático no Vercel (frontend)

---

## 5️⃣ Testar a Aplicação

1. Aguarde os deploys terminarem (5-10 min)
2. Acesse: https://pense-offline.vercel.app
3. Tente fazer login/cadastro
4. Verifique no console do navegador (F12) se não há erros de CORS

---

## 🔍 Troubleshooting

### Erro: "NetworkError when attempting to fetch"
- ✅ Verifique se a URL do backend está correta no `api-client.js`
- ✅ Confirme que o backend está rodando (acesse `https://seu-backend.onrender.com/health`)
- ✅ Verifique logs no Render Dashboard → Seu serviço → Logs

### Erro: CORS blocked
- ✅ Confirme que `https://pense-offline.vercel.app` está em `ALLOWED_ORIGINS` no Render
- ✅ Faça redeploy do backend após alterar variáveis de ambiente

### Backend não inicia no Render
- ✅ Verifique se `DATABASE_URL` está configurado
- ✅ Confira se o `Dockerfile` está em `backend/Dockerfile`
- ✅ Veja os logs de build no Render

### Banco de dados vazio
Execute migrations manualmente:
1. No Render Dashboard → Seu web service
2. **Shell** (canto superior direito)
3. Execute:
```bash
cd backend
python -m app.seed
```

---

## 📱 URLs Importantes

- **Frontend**: https://pense-offline.vercel.app
- **Backend**: https://penseoffline-backend.onrender.com
- **Health Check**: https://penseoffline-backend.onrender.com/health
- **Render Dashboard**: https://dashboard.render.com
- **Vercel Dashboard**: https://vercel.com/dashboard

---

## 🎯 Checklist Final

- [ ] PostgreSQL criado no Render
- [ ] Web Service criado no Render
- [ ] DATABASE_URL configurado
- [ ] SECRET_KEY configurado
- [ ] ALLOWED_ORIGINS configurado
- [ ] URL do backend atualizada no frontend
- [ ] CORS configurado no backend (main.py)
- [ ] Git push realizado
- [ ] Deploys finalizados
- [ ] Teste de login/cadastro funcionando

---

**Pronto! Seu app está em produção! 🎉**

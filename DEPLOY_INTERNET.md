# 🌐 Deploy Público na Internet - Guia Completo

## Opção 1: Render.com (Recomendado - Gratuito)

### Passo 1: Preparar o Repositório

Já está pronto! O código foi enviado para: https://github.com/MrLonely0-0/PenseOffline

### Passo 2: Criar Conta no Render

1. Acesse: https://render.com
2. Clique em **"Get Started for Free"**
3. Faça login com sua conta GitHub

### Passo 3: Deploy do Backend

1. No dashboard do Render, clique em **"New +"** → **"Web Service"**
2. Conecte seu repositório GitHub: `MrLonely0-0/PenseOffline`
3. Configure:
   - **Name:** `pense-offline-api`
   - **Region:** `Oregon (US West)` (ou mais próximo)
   - **Branch:** `master`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** `Free`

4. **Environment Variables** (adicionar):
   ```
   DATABASE_URL=sua-url-do-supabase
   SECRET_KEY=sua-chave-secreta-jwt
   ```
   
   Para obter do seu `.env`:
   - DATABASE_URL: `postgresql://postgres:SUA_SENHA@db.libchjoccyjblobxjkeq.supabase.co:5432/postgres`
   - SECRET_KEY: copie do arquivo `backend/.env`

5. Clique em **"Create Web Service"**

### Passo 4: Deploy dos Arquivos Estáticos (Frontend)

Render serve backend, mas para frontend precisamos de outra estratégia:

**Opção A - GitHub Pages (Mais Simples):**

1. No repositório GitHub, vá em **Settings** → **Pages**
2. Em **Source**, selecione `Deploy from a branch`
3. Escolha branch `master` e pasta `/ (root)`
4. Clique em **Save**
5. Aguarde alguns minutos
6. Seu site estará em: `https://mrlonely0-0.github.io/PenseOffline/`

**Opção B - Render Static Site:**

1. No Render, clique **"New +"** → **"Static Site"**
2. Conecte o mesmo repositório
3. Configure:
   - **Name:** `pense-offline-web`
   - **Branch:** `master`
   - **Root Directory:** deixe vazio
   - **Build Command:** deixe vazio
   - **Publish Directory:** `.` (ponto)

4. Clique em **"Create Static Site"**

### Passo 5: Configurar URLs

Após o deploy, você receberá URLs como:
- **Backend:** `https://pense-offline-api.onrender.com`
- **Frontend:** `https://pense-offline-web.onrender.com` ou `https://mrlonely0-0.github.io/PenseOffline/`

Precisamos atualizar o frontend para usar a URL do backend em produção.

---

## Opção 2: Vercel (Backend + Frontend)

### Backend no Vercel

1. Acesse: https://vercel.com
2. Faça login com GitHub
3. Importe o repositório `PenseOffline`
4. Configure:
   - **Framework Preset:** `Other`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Output Directory:** deixe vazio

5. Adicione arquivo `vercel.json` no backend (já vou criar)

### Frontend no Vercel

1. Crie novo projeto no Vercel
2. Importe o mesmo repositório
3. Configure:
   - **Framework Preset:** `Other`
   - **Root Directory:** deixe vazio (usa raiz)
   - **Build Command:** deixe vazio
   - **Output Directory:** `.`

---

## Opção 3: Railway (Simples e Rápido)

1. Acesse: https://railway.app
2. Login com GitHub
3. **"New Project"** → **"Deploy from GitHub repo"**
4. Selecione `PenseOffline`
5. Railway detectará automaticamente o Python
6. Configure variáveis de ambiente no dashboard

---

## Próximos Passos Após Deploy

### 1. Atualizar api-client.js

Editar `api-client.js` para usar URL de produção:

```javascript
const API_URL = (typeof window !== 'undefined' && window.PENSEOFFLINE_API_URL) 
  ? window.PENSEOFFLINE_API_URL 
  : "https://pense-offline-api.onrender.com"; // SUA URL AQUI
```

### 2. Testar o Site

Acesse a URL do frontend e teste:
- ✅ Criar conta
- ✅ Fazer login
- ✅ Acessar dashboard
- ✅ Completar desafios

### 3. Compartilhar

Seu site estará acessível de qualquer lugar do mundo! 🌍

Compartilhe a URL com amigos:
```
https://pense-offline-web.onrender.com
ou
https://mrlonely0-0.github.io/PenseOffline/
```

---

## 🆘 Troubleshooting

### "Application failed to respond"
- Verifique os logs no Render
- Certifique-se de que o comando de start está correto
- Verifique se DATABASE_URL está configurado

### "CORS Error"
- Backend já está configurado com `allow_origins=["*"]`
- Se ainda ocorrer, verifique se a URL do backend está correta

### "Database connection error"
- Verifique se DATABASE_URL está correto
- Certifique-se de que Supabase permite conexões externas

---

## 💰 Custos

- **Render Free Tier:** Gratuito, mas dorme após 15 min de inatividade
- **Vercel Free Tier:** Gratuito, sempre ativo
- **Railway Free Tier:** $5 de crédito grátis/mês
- **GitHub Pages:** Totalmente gratuito (apenas frontend estático)

---

## 🚀 Recomendação

Para começar rapidamente:

1. **Backend:** Render.com (mais confiável para Python/FastAPI)
2. **Frontend:** GitHub Pages (gratuito e sempre ativo)

Quer que eu configure isso agora? Posso criar os arquivos necessários!

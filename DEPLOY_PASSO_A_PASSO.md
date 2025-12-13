# 🚀 Deploy Rápido - 15 Minutos

## 📋 O que você precisa:
- Conta GitHub (já tem ✅)
- Conta Render.com (criar grátis)
- Acesso ao banco Supabase (já tem ✅)

---

## Parte 1️⃣: Deploy do Backend (API) - Render.com

### Passo 1: Criar conta no Render
1. Acesse: https://render.com
2. Clique em **"Get Started for Free"**
3. Escolha **"Sign up with GitHub"**
4. Autorize o Render a acessar seus repositórios

### Passo 2: Criar Web Service
1. No dashboard, clique em **"New +"** no canto superior direito
2. Selecione **"Web Service"**
3. Clique em **"Build and deploy from a Git repository"** → **Next**

### Passo 3: Conectar Repositório
1. Encontre **"PenseOffline"** na lista (ou clique em "Configure account" se não aparecer)
2. Clique em **"Connect"** ao lado do repositório

### Passo 4: Configurar o Serviço
Preencha exatamente assim:

```
Name: pense-offline-api
Region: Oregon (US West) [ou o mais próximo de você]
Branch: master
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

### Passo 5: Variáveis de Ambiente
Role para baixo até **"Environment Variables"** e clique em **"Add Environment Variable"**

Adicione estas 2 variáveis:

**Variável 1:**
```
Key: DATABASE_URL
Value: postgresql://postgres:uCJFgTWrFbkvfMKI@db.libchjoccyjblobxjkeq.supabase.co:5432/postgres
```

**Variável 2:**
```
Key: SECRET_KEY
Value: sua-chave-jwt-do-arquivo-.env-no-backend
```

> **Como encontrar SECRET_KEY:**
> Abra o arquivo `backend/.env` no seu computador e copie o valor de `SECRET_KEY`

### Passo 6: Criar!
1. Clique em **"Create Web Service"** no final da página
2. Aguarde 3-5 minutos enquanto o Render faz o deploy
3. Quando aparecer **"Live"** com bolinha verde, está pronto! ✅

### Passo 7: Copiar URL
Copie a URL que aparece no topo, será algo como:
```
https://pense-offline-api.onrender.com
```

⚠️ **IMPORTANTE:** Guarde essa URL! Você vai precisar dela no próximo passo.

---

## Parte 2️⃣: Deploy do Frontend (Site) - GitHub Pages

### Passo 1: Ativar GitHub Pages
1. Acesse: https://github.com/MrLonely0-0/PenseOffline
2. Clique em **"Settings"** (configurações)
3. No menu lateral esquerdo, clique em **"Pages"**

### Passo 2: Configurar Source
Em **"Build and deployment"**:
```
Source: Deploy from a branch
Branch: master
Folder: / (root)
```

Clique em **"Save"**

### Passo 3: Aguardar Deploy
1. Aguarde 2-3 minutos
2. Atualize a página
3. Aparecerá uma mensagem: **"Your site is live at https://mrlonely0-0.github.io/PenseOffline/"**

---

## Parte 3️⃣: Conectar Frontend com Backend

### Passo 1: Atualizar api-client.js

No seu computador, abra o arquivo: `api-client.js`

Encontre esta linha (linha 6):
```javascript
const API_URL = (typeof window !== 'undefined' && window.PENSEOFFLINE_API_URL) 
  ? window.PENSEOFFLINE_API_URL 
  : (typeof window !== 'undefined' ? `http://${window.location.hostname}:8000` : "http://127.0.0.1:8000");
```

Substitua por:
```javascript
const API_URL = (typeof window !== 'undefined' && window.PENSEOFFLINE_API_URL) 
  ? window.PENSEOFFLINE_API_URL 
  : "https://pense-offline-api.onrender.com"; // COLE SUA URL DO RENDER AQUI
```

### Passo 2: Fazer Commit e Push

No PowerShell:
```powershell
cd C:\PenseOffline\PenseOffline-main
git add api-client.js
git commit -m "Configurar URL de produção"
git push origin master
```

### Passo 3: Aguardar Atualização
Aguarde 2-3 minutos para GitHub Pages atualizar.

---

## 🎉 PRONTO! Testando...

### Seu site está no ar em:
```
https://mrlonely0-0.github.io/PenseOffline/
```

### Teste completo:
1. ✅ Abra o link acima
2. ✅ Clique em "Criar Conta Grátis"
3. ✅ Preencha o formulário de cadastro
4. ✅ Faça login
5. ✅ Acesse o dashboard

### Compartilhe com o mundo! 🌍
Envie o link para amigos:
```
https://mrlonely0-0.github.io/PenseOffline/
```

Qualquer pessoa, de qualquer lugar, pode:
- Criar uma conta
- Fazer login
- Completar desafios
- Ver ranking

---

## ⚠️ Notas Importantes

### Render Free Tier
- O backend **hiberna após 15 minutos sem uso**
- Primeira requisição após hibernar demora ~30 segundos (cold start)
- Depois funciona normalmente
- Para manter sempre ativo, upgrade para plano pago ($7/mês)

### GitHub Pages
- Frontend sempre ativo, sem hibernar
- Atualizações levam 2-3 minutos para propagar
- Totalmente gratuito, sem limites

---

## 🆘 Problemas Comuns

### "Failed to fetch" ao criar conta
- Aguarde 30 segundos e tente novamente (cold start)
- Verifique se a URL no `api-client.js` está correta
- Confirme que o backend está "Live" no Render

### "Not Found" ao acessar o site
- Aguarde GitHub Pages completar o deploy (2-3 min)
- Limpe o cache do navegador (Ctrl+Shift+R)

### Site carrega mas não cria conta
- Verifique logs no Render: Dashboard → Logs
- Confirme DATABASE_URL está correto
- Teste a URL da API diretamente: `https://sua-url.onrender.com/health`

---

## 📱 Acesso Mobile

Funciona perfeitamente em celular! Basta acessar:
```
https://mrlonely0-0.github.io/PenseOffline/
```

Adicione à tela inicial:
- **iPhone:** Safari → Compartilhar → "Adicionar à Tela de Início"
- **Android:** Chrome → Menu → "Adicionar à tela inicial"

---

## 💡 Próximos Passos (Opcional)

### Domínio Personalizado
Em vez de `mrlonely0-0.github.io/PenseOffline`, tenha:
```
www.penseoffline.com.br
```

1. Compre domínio (.com.br ~R$40/ano)
2. Configure no GitHub Pages Settings
3. Atualize URL no Render

### Melhorias de Performance
- Ativar CDN no Render
- Comprimir arquivos estáticos
- Adicionar cache HTTP

Quer ajuda com algo específico?

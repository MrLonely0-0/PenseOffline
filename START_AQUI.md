# ⚡ GUIA RÁPIDO - 10 MINUTOS

## 🎯 Objetivo
Colocar seu site na internet para que **QUALQUER PESSOA**, de **QUALQUER LUGAR**, possa acessar.

---

## ✅ PARTE 1: BACKEND (API) - 5 minutos

### 1. Criar conta no Render
🔗 **https://render.com**
- Clique "Get Started for Free"
- Escolha "Sign up with GitHub"
- Autorize o Render

### 2. Criar Web Service
- Clique "New +" → "Web Service"
- Conecte o repositório **PenseOffline**

### 3. Preencher campos:
```
Name: pense-offline-api
Region: Oregon (US West)
Branch: master
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 4. Adicionar 2 variáveis de ambiente:

**DATABASE_URL:**
```
postgresql://postgres:uCJFgTWrFbkvfMKI@db.libchjoccyjblobxjkeq.supabase.co:5432/postgres
```

**SECRET_KEY:**
```
(copie do arquivo backend/.env no seu computador)
```

### 5. Criar e aguardar
- Clique "Create Web Service"
- Aguarde 3-5 minutos
- Quando ficar verde "Live", copie a URL:
  ```
  https://pense-offline-api-XXXX.onrender.com
  ```

---

## ✅ PARTE 2: FRONTEND (SITE) - 3 minutos

### 1. Ativar GitHub Pages
🔗 **https://github.com/MrLonely0-0/PenseOffline/settings/pages**

- Source: **Deploy from a branch**
- Branch: **master**
- Folder: **/ (root)**
- Clique "Save"

### 2. Aguardar
- Espere 2-3 minutos
- Recarregue a página
- Aparecerá: "Your site is live at..."

---

## ✅ PARTE 3: CONECTAR - 2 minutos

### 1. Editar api-client.js
No VS Code, abra `api-client.js`

Encontre a linha 21:
```javascript
return "https://pense-offline-api.onrender.com";
```

Substitua pela **SUA URL** copiada do Render.

### 2. Salvar e enviar
No PowerShell:
```powershell
cd C:\PenseOffline\PenseOffline-main
git add api-client.js
git commit -m "Atualizar URL de produção"
git push origin master
```

### 3. Aguardar GitHub Pages atualizar (2 min)

---

## 🎉 PRONTO!

Seu site está em:
```
https://mrlonely0-0.github.io/PenseOffline/
```

**Compartilhe com o mundo!** 🌍

Qualquer pessoa pode:
- ✅ Criar uma conta
- ✅ Fazer login
- ✅ Completar desafios
- ✅ Ver ranking

---

## ⚠️ IMPORTANTE

**Cold Start do Render:**
- Backend hiberna após 15 min sem uso
- Primeiro acesso demora ~30 segundos
- Depois funciona normalmente
- Para manter sempre ativo: upgrade $7/mês

---

## 🆘 PROBLEMAS?

### "Failed to fetch"
→ Aguarde 30s (cold start) e tente novamente

### Site não carrega
→ Aguarde GitHub Pages terminar (2-3 min)
→ Limpe cache (Ctrl+Shift+R)

### Erro ao criar conta
→ Verifique se URL no api-client.js está correta
→ Confirme backend está "Live" no Render

---

## 📱 MOBILE

Funciona perfeitamente!

**Adicionar à tela inicial:**
- iPhone: Safari → Compartilhar → "Adicionar à Tela de Início"
- Android: Chrome → Menu → "Adicionar à tela inicial"

---

## ✨ PRÓXIMOS PASSOS

Após colocar no ar:

1. Teste completo (criar conta, login, desafios)
2. Compartilhe nas redes sociais
3. Peça feedback de amigos
4. Continue desenvolvendo!

**Precisa de ajuda?** Consulte [DEPLOY_PASSO_A_PASSO.md](DEPLOY_PASSO_A_PASSO.md)

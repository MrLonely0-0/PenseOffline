# Correção do Erro "NetworkError" no Deploy

## 🐛 Problema
Erro "NetworkError when attempting to fetch resource" ao tentar fazer cadastro ou login no Vercel.

## ✅ Solução Implementada

### 1. CORS Dinâmico no Backend
O backend agora aceita configuração de CORS via variável de ambiente `CORS_ORIGINS`.

### 2. Como Configurar

#### Backend (Render/Railway/Heroku)

Adicione estas variáveis de ambiente:

**Obrigatórias:**
```
DATABASE_URL=postgresql://postgres:senha@db.abc123.supabase.co:5432/postgres
CORS_ORIGINS=https://seu-app.vercel.app
ENVIRONMENT=production
```

⚠️ **IMPORTANTE**: `CORS_ORIGINS` é obrigatória em produção por segurança.

Se tiver múltiplos domínios:

```
CORS_ORIGINS=https://seu-app.vercel.app,https://www.seu-app.com
```

#### Frontend (Vercel)

✅ **DETECÇÃO AUTOMÁTICA**: O frontend agora detecta automaticamente se está em localhost ou produção!

- **Localhost**: Usa `http://127.0.0.1:8000` automaticamente
- **Produção**: Usa a mesma origem do frontend (ex: `https://seu-app.vercel.app`)

⚙️ **Configuração Manual** (apenas se backend em servidor separado):

Se seu backend está no Render/Railway (não no Vercel), edite `config.js`:

```javascript
window.PENSEOFFLINE_API_URL = 'https://seu-backend.onrender.com';
```

### 3. Exemplo Completo

**Cenário 1: Backend no Vercel (junto com frontend)**
```env
# Backend
DATABASE_URL=postgresql://postgres:senha@db.abc123.supabase.co:5432/postgres
CORS_ORIGINS=https://penseoffline.vercel.app
ENVIRONMENT=production

# Frontend
# Nenhuma configuração necessária! ✅ Detecção automática
```

**Cenário 2: Backend no Render, Frontend no Vercel**
```env
# Backend (Render)
DATABASE_URL=postgresql://postgres:senha@db.abc123.supabase.co:5432/postgres
CORS_ORIGINS=https://penseoffline.vercel.app
ENVIRONMENT=production
```

**Frontend - config.js:**
```javascript
window.PENSEOFFLINE_API_URL = 'https://penseoffline-backend.onrender.com';
```

## 📚 Documentação Completa

Veja o arquivo `VERCEL_DEPLOYMENT.md` para instruções detalhadas passo a passo.

## 🧪 Testar Localmente

```bash
# Backend
cd backend
export CORS_ORIGINS="http://localhost:8080"
python -m uvicorn app.main:app --reload

# Frontend (outro terminal)
python -m http.server 8080
```

Acesse: http://localhost:8080

## 🔧 Arquivos Alterados

- `backend/app/main.py` - CORS dinâmico
- `config.js` - Configuração do frontend (novo)
- `backend/.env.example` - Exemplo de variáveis (novo)
- `VERCEL_DEPLOYMENT.md` - Guia completo (novo)
- `*.html` - Adiciona config.js antes de api-client.js

## 🆘 Troubleshooting

### Ainda dá erro de CORS?
1. Verifique se `CORS_ORIGINS` está correta no backend
2. Confirme que o backend foi reiniciado
3. Limpe o cache do navegador (Ctrl+Shift+Del)

### Backend não responde?
1. Verifique os logs do Render/Railway
2. Teste: `https://seu-backend.onrender.com/health`
3. Confirme que `DATABASE_URL` está correta

### Frontend não conecta?
1. Verifique se `config.js` está configurado
2. Abra DevTools (F12) → Console
3. Verifique qual URL está sendo usada

## ⚠️ Importante

- **Nunca commite** senhas no código
- Use **variáveis de ambiente** para credenciais
- Configure **CORS_ORIGINS** com domínios específicos
- Use **HTTPS** em produção

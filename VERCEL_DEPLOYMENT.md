# Guia de Deploy: Vercel + Supabase

Este guia explica como resolver o erro "NetworkError when attempting to fetch resource" ao fazer deploy da aplicação PenseOffline no Vercel com banco de dados Supabase.

## Problema

Quando a aplicação é deployada no Vercel, as requisições de cadastro e login falham com erro de rede. Isso ocorre porque:

1. O backend FastAPI tem CORS configurado para aceitar apenas origins localhost
2. O frontend no Vercel tem uma origem diferente (ex: `https://seu-app.vercel.app`)
3. O navegador bloqueia as requisições devido à política CORS

## Solução

### 1. Configurar Variáveis de Ambiente no Backend

O backend agora suporta configuração dinâmica de CORS através de variáveis de ambiente.

#### Opção A: Configurar CORS_ORIGINS (Recomendado)

Defina a variável `CORS_ORIGINS` com as origens permitidas, separadas por vírgula:

```
CORS_ORIGINS=https://seu-app.vercel.app,https://www.seu-app.com
```

#### Opção B: Usar ENVIRONMENT=production (Fallback)

Se você não puder configurar `CORS_ORIGINS`, defina:

```
ENVIRONMENT=production
```

Isso permitirá todas as origens automaticamente (menos seguro, mas funcional).

### 2. Configurar Backend no Render/Railway/Heroku

Se você está usando Render, Railway ou Heroku para o backend:

1. Acesse o dashboard do serviço
2. Vá para configurações de ambiente / Environment Variables
3. Adicione as variáveis:

**Obrigatórias:**
- `DATABASE_URL`: String de conexão do Supabase
  - Exemplo: `postgresql://postgres:SUA_SENHA@db.PROJECT_ID.supabase.co:5432/postgres`
- `CORS_ORIGINS`: Domínio(s) do frontend Vercel
  - Exemplo: `https://seu-app.vercel.app`

**Opcional:**
- `ENVIRONMENT`: `production`
- `SECRET_KEY`: Chave secreta para JWT (gere uma aleatória)

### 3. Obter Credenciais do Supabase

1. Acesse https://app.supabase.com
2. Selecione seu projeto
3. Vá em **Settings** → **Database**
4. Copie a **Connection String** (URI mode)
5. Substitua `[YOUR-PASSWORD]` pela senha do banco

### 4. Configurar URL do Backend no Frontend

Você tem duas opções para configurar a URL do backend no frontend:

#### Opção A: Usando config.js (Recomendado)

1. Edite o arquivo `config.js` na raiz do projeto
2. Descomente e configure a URL do backend:

```javascript
window.PENSEOFFLINE_API_URL = 'https://seu-backend.onrender.com';
```

3. Commit e push as alterações

#### Opção B: Variáveis de Ambiente do Vercel

1. No dashboard do Vercel, vá em **Settings** → **Environment Variables**
2. Adicione:
   - **Name**: `PENSEOFFLINE_API_URL`
   - **Value**: `https://seu-backend.onrender.com`

**Nota**: A Opção A é mais simples pois não requer reconstrução do projeto no Vercel.

### 5. Deploy no Vercel

1. Conecte seu repositório ao Vercel
2. Configure as build settings (geralmente detectadas automaticamente)
3. Deploy!

O Vercel irá automaticamente servir os arquivos HTML estáticos.

### 6. Verificar Configuração

Após o deploy:

1. Abra o DevTools do navegador (F12)
2. Vá para a aba **Console**
3. Tente fazer login ou cadastro
4. Verifique se há erros de CORS

Se ainda houver erros:
- Verifique se as variáveis de ambiente foram salvas corretamente
- Confirme que o backend foi reiniciado após adicionar as variáveis
- Teste a conexão com o backend diretamente: `https://seu-backend.onrender.com/health`

## Exemplo de Configuração Completa

### Backend (Render/Railway)

```env
DATABASE_URL=postgresql://postgres:senha@db.abc123.supabase.co:5432/postgres
CORS_ORIGINS=https://penseoffline.vercel.app,https://www.penseoffline.com
ENVIRONMENT=production
SECRET_KEY=sua-chave-secreta-aleatoria-aqui-min-32-caracteres
```

### Frontend (Vercel)

```env
PENSEOFFLINE_API_URL=https://penseoffline-backend.onrender.com
```

Ou adicione no `index.html`, `login.html`, `cadastro.html`, etc:

```html
<head>
  <!-- outras tags -->
  <script>
    window.PENSEOFFLINE_API_URL = 'https://penseoffline-backend.onrender.com';
  </script>
</head>
```

## Troubleshooting

### Erro: "CORS policy blocked"
- **Causa**: CORS_ORIGINS não inclui o domínio do Vercel
- **Solução**: Adicione o domínio completo em CORS_ORIGINS

### Erro: "Failed to fetch"
- **Causa**: Backend não está respondendo ou URL incorreta
- **Solução**: Verifique se `PENSEOFFLINE_API_URL` está correta e o backend está online

### Erro: "Authorization required"
- **Causa**: Token JWT inválido ou expirado
- **Solução**: Faça logout e login novamente

### Backend retorna 500
- **Causa**: Erro de conexão com Supabase
- **Solução**: Verifique a DATABASE_URL e se o IP do serviço está na whitelist do Supabase

## Segurança

⚠️ **Importante:**

1. Nunca commite senhas ou chaves secretas no repositório
2. Use variáveis de ambiente para todas as credenciais
3. Configure CORS_ORIGINS com domínios específicos, evite usar `*`
4. Use HTTPS em produção
5. Mantenha o SECRET_KEY com no mínimo 32 caracteres aleatórios

## Suporte

Se ainda tiver problemas:
1. Verifique os logs do backend no Render/Railway
2. Verifique os logs do Vercel
3. Teste localmente com as mesmas variáveis de ambiente
4. Abra uma issue no repositório com detalhes do erro

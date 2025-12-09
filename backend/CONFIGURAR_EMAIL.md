# 📧 Configuração de Email - Pense Offline

## ⚠️ Importante
Atualmente, o sistema está **simulando** o envio de emails (apenas exibe no console). Para enviar emails reais, siga um dos guias abaixo.

**Recomendação:** Use SendGrid (100 emails/dia grátis) - mais simples e seguro.

---

## 🌟 Opção 1: SendGrid (RECOMENDADO - Grátis)

### Por que SendGrid?
- ✅ 100 emails por dia gratuitamente
- ✅ Não precisa usar seu email pessoal
- ✅ Configuração em 5 minutos
- ✅ Emails não vão para spam
- ✅ Profissional e confiável

### Passo 1: Criar Conta SendGrid
1. Acesse: https://signup.sendgrid.com/
2. Preencha o formulário (use dados reais)
3. Confirme seu email
4. Complete o questionário inicial:
   - **I'm sending emails for:** Website/App
   - **How many emails:** Less than 40k
   - **How many contacts:** Less than 1k

### Passo 2: Criar API Key
1. Acesse: https://app.sendgrid.com/settings/api_keys
2. Clique em **Create API Key**
3. Nome: `Pense Offline Backend`
4. Tipo: **Full Access**
5. Clique em **Create & View**
6. **COPIE A API KEY** (você só verá uma vez!)
   - Formato: `SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Passo 3: Verificar Remetente
1. Acesse: https://app.sendgrid.com/settings/sender_auth/senders
2. Clique em **Create New Sender**
3. Preencha:
   - **From Name:** Pense Offline
   - **From Email:** noreply@penseoffline.com (ou seu domínio)
   - **Reply To:** danielpereira09@outlook.com
   - **Company Address:** (preencha com dados reais)
4. Clique em **Save**
5. Você receberá um email de verificação - clique no link

### Passo 4: Configurar no .env
Edite o arquivo `backend/.env`:

```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.sua-api-key-completa-aqui
FROM_EMAIL=noreply@penseoffline.com
FROM_NAME=Pense Offline
```

**Substitua:**
- `SG.sua-api-key-completa-aqui` → Sua API Key do SendGrid

---

## 🟢 Opção 1: Gmail (Recomendado)

### Passo 1: Habilitar Verificação em Duas Etapas
1. Acesse: https://myaccount.google.com/security
2. Ative "Verificação em duas etapas"

### Passo 2: Criar Senha de App
1. Acesse: https://myaccount.google.com/apppasswords
2. Selecione:
   - App: **Email**
   - Dispositivo: **Outro (nome personalizado)**
   - Digite: **Pense Offline Backend**
3. Clique em **Gerar**
4. Copie a senha de 16 dígitos (formato: xxxx xxxx xxxx xxxx)

### Passo 3: Configurar no .env
Edite o arquivo `backend/.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx
FROM_EMAIL=seu-email@gmail.com
FROM_NAME=Pense Offline
```

**Substitua:**
- `seu-email@gmail.com` → Seu email Gmail
- `xxxx-xxxx-xxxx-xxxx` → A senha de 16 dígitos gerada

---

## 🔵 Opção 2: Outlook/Hotmail

### Método A: Autenticação Padrão (Mais Simples)

Edite o arquivo `backend/.env`:

```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=danielpereira09@outlook.com
SMTP_PASSWORD=sua-senha-normal-do-outlook
FROM_EMAIL=danielpereira09@outlook.com
FROM_NAME=Pense Offline
```

**Substitua:**
- `danielpereira09@outlook.com` → Seu email Outlook/Hotmail
- `sua-senha-normal-do-outlook` → Sua senha normal da conta

### Método B: Com Verificação em Duas Etapas (Mais Seguro)

Se você tem verificação em duas etapas ativada:

1. Acesse: https://account.microsoft.com/security
2. Vá em **Segurança Avançada**
3. Clique em **Criar nova senha de aplicativo**
4. Use a senha gerada no `.env`

---

## 🚀 Como Usar

### 1. Editar .env
Abra `backend/.env` e escolha **UMA** das opções:

**Gmail:**
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-gmail@gmail.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx
FROM_EMAIL=seu-gmail@gmail.com
FROM_NAME=Pense Offline
```

**OU Outlook:**
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=seu-outlook@outlook.com
SMTP_PASSWORD=sua-senha
FROM_EMAIL=seu-outlook@outlook.com
FROM_NAME=Pense Offline
```

### 2. Reiniciar o Servidor
```powershell
# Parar servidor atual
Get-Process -Name python | Stop-Process -Force

# Iniciar novamente
cd C:\PenseOffline\PenseOffline-main\backend
& .\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8000
```

### 3. Testar
Crie um novo usuário via API ou frontend. Você deve receber o email de boas-vindas.

---

## 🧪 Teste Manual via PowerShell

```powershell
$body = @{
    username="teste_email"
    email="seu-email-pessoal@gmail.com"
    password="SenhaSegura123!"
    name="Teste Email"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/users/register" `
    -Method POST -Body $body -ContentType "application/json"
```

Verifique sua caixa de entrada (e spam) em alguns segundos.

---

## 🔍 Verificar Logs

Se o email não chegar, verifique os logs no console do servidor:

✅ **Sucesso:**
```
Email enviado com sucesso para usuario@email.com
```

❌ **Erro:**
```
Erro ao enviar email: [detalhes do erro]
```

---

## ⚡ Provedores Alternativos (Avançado)

### SendGrid (100 emails/dia grátis)
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.sua-api-key-aqui
FROM_EMAIL=seu-email@dominio.com
FROM_NAME=Pense Offline
```

### Mailgun
```env
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@seu-dominio.mailgun.org
SMTP_PASSWORD=sua-senha-mailgun
FROM_EMAIL=noreply@seu-dominio.com
FROM_NAME=Pense Offline
```

---

## ❓ Problemas Comuns

### Gmail: "Senha incorreta"
- ✓ Certifique-se de usar **Senha de App**, não a senha normal
- ✓ Verificação em duas etapas deve estar ativada

### Outlook: "Autenticação falhou"
- ✓ Verifique se o email e senha estão corretos
- ✓ Tente desabilitar temporariamente verificação em duas etapas

### Email não chega
- ✓ Verifique a pasta de **Spam/Lixo Eletrônico**
- ✓ Adicione o remetente aos contatos
- ✓ Verifique os logs do servidor

### Erro de conexão
- ✓ Verifique sua conexão com internet
- ✓ Confirme que a porta 587 não está bloqueada
- ✓ Alguns antivírus bloqueiam SMTP

---

## 📝 Notas

- 📧 Emails são enviados de forma **assíncrona** (não bloqueiam o cadastro)
- ⚠️ Se o email falhar, o usuário ainda é criado com sucesso
- 🔒 As credenciais no `.env` **NÃO** são commitadas no Git (arquivo em .gitignore)
- 🎯 Em produção, use variáveis de ambiente do servidor/hosting

---

## ✅ Status Atual

**Modo:** Simulação (console only)  
**Para ativar:** Configure credenciais SMTP no arquivo `.env`  
**Após configurar:** Reinicie o servidor

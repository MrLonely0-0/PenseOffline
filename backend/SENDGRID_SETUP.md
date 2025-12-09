# 🚀 Setup SendGrid - Guia Rápido (5 minutos)

## Passo 1: Criar Conta (2 minutos)
1. Abra: https://signup.sendgrid.com/
2. Preencha:
   - Email: danielpereira09@outlook.com
   - Password: (crie uma senha forte)
   - Clique em "Create Account"
3. Confirme seu email (cheque a caixa de entrada)

## Passo 2: Completar Questionário (1 minuto)
Após login, você verá um questionário. Responda:
- **Tell us about yourself:** Developer
- **What do you do?** Build and send emails for my app
- **What kind of emails?** Transactional (welcome emails, confirmations)
- **How many emails per month?** Less than 40,000
- **How many contacts?** Less than 1,000

## Passo 3: Criar API Key (1 minuto)
1. Vá em: https://app.sendgrid.com/settings/api_keys
   - Ou: Settings → API Keys (menu lateral)
2. Clique em **"Create API Key"**
3. Configurações:
   - Name: `PenseOffline-Backend`
   - API Key Permissions: **Full Access**
4. Clique em **"Create & View"**
5. **COPIE A API KEY AGORA** (formato: SG.xxxxxxxxxx)
   - ⚠️ Você só verá ela uma vez!
   - Cole temporariamente no Notepad

## Passo 4: Verificar Remetente (1 minuto)
1. Vá em: https://app.sendgind.com/settings/sender_auth/senders
   - Ou: Settings → Sender Authentication → Single Sender Verification
2. Clique em **"Create New Sender"**
3. Preencha o formulário:
   ```
   From Name: Pense Offline
   From Email: noreply@penseoffline.com
   Reply To: danielpereira09@outlook.com
   Company Address: (use seu endereço real)
   Company City: (sua cidade)
   Company State: (seu estado)
   Company Zip: (seu CEP)
   Company Country: Brazil
   ```
4. Clique em **"Save"**
5. Você receberá um email - **CLIQUE NO LINK** para verificar

## Passo 5: Configurar no Projeto (30 segundos)
Volte aqui e me envie a API Key que você copiou.

Formato esperado: `SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## ⚠️ Importante
- A API Key é secreta - não compartilhe publicamente
- Guarde ela em local seguro
- Se perder, crie uma nova

## 🆘 Problemas?
- **Não recebi email de verificação:** Cheque spam/lixo eletrônico
- **API Key não funciona:** Certifique-se de selecionar "Full Access"
- **Erro de autenticação:** Verifique se copiou a key completa

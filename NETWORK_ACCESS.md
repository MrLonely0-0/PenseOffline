# Acesso em Rede Local - Guia de Configuração

## 🌐 Como acessar de outros dispositivos

### Passo 1: Iniciar o servidor para rede local

Execute o script especial para rede local:

```powershell
cd backend
.\start_network.ps1
```

Este script irá:
- Detectar automaticamente o IP da sua máquina
- Configurar o servidor para aceitar conexões externas
- Mostrar as URLs de acesso

### Passo 2: Configurar Firewall do Windows

**Opção A - Automática (Recomendado):**

Execute este comando no PowerShell como Administrador:

```powershell
netsh advfirewall firewall add rule name="Pense Offline" dir=in action=allow protocol=TCP localport=8000
```

**Opção B - Manual:**

1. Abra o Painel de Controle
2. Vá em "Sistema e Segurança" → "Firewall do Windows Defender"
3. Clique em "Configurações avançadas"
4. Clique em "Regras de Entrada" (à esquerda)
5. Clique em "Nova Regra..." (à direita)
6. Selecione "Porta" → Avançar
7. Selecione "TCP" e digite "8000" em "Portas locais específicas" → Avançar
8. Selecione "Permitir a conexão" → Avançar
9. Marque todas as opções (Domínio, Privado, Público) → Avançar
10. Digite um nome: "Pense Offline" → Concluir

### Passo 3: Conectar outros dispositivos

1. **Certifique-se de que o dispositivo está na mesma rede Wi-Fi**
2. **Abra o navegador** no celular/tablet/outro computador
3. **Digite o endereço** mostrado pelo script, exemplo:
   ```
   http://192.168.1.10:8000
   ```

### 🔍 Como descobrir o IP da sua máquina manualmente

Se o script não detectar automaticamente, execute:

```powershell
ipconfig
```

Procure por "Endereço IPv4" na seção "Adaptador de Rede Sem Fio" ou "Ethernet".
Geralmente começa com `192.168.` ou `10.`

### ✅ Verificação

Para testar se está funcionando:

1. **No seu computador**, acesse: `http://127.0.0.1:8000`
2. **No celular**, acesse: `http://<SEU-IP>:8000` (exemplo: `http://192.168.1.10:8000`)

Se funcionar no computador mas não no celular:
- ✓ Verifique se o firewall está configurado
- ✓ Verifique se estão na mesma rede Wi-Fi
- ✓ Tente desabilitar temporariamente o firewall para testar

### 🚨 Solução de Problemas

#### "Site não pode ser acessado" / "Not Found"

1. Verifique se o servidor está rodando com `start_network.ps1`
2. Confirme que o firewall permite a porta 8000
3. Certifique-se de usar HTTP (não HTTPS) - `http://` não `https://`
4. Teste usando o IP em vez de localhost

#### "CORS Error" no navegador

O backend já está configurado para permitir todas as origens (`allow_origins=["*"]`).
Se ainda assim der erro, verifique se o arquivo `backend/app/main.py` tem:
```python
allow_origins=["*"],
```

#### Conexão recusada

Execute como administrador:
```powershell
netsh advfirewall firewall show rule name="Pense Offline"
```

Se não aparecer nada, a regra não foi criada. Execute novamente o comando de adicionar regra.

### 📱 Dica para Celular

Salve o endereço IP como favorito no navegador do celular para acesso rápido!

Exemplo: `http://192.168.1.10:8000`

### 🔒 Segurança

**IMPORTANTE:** Este servidor está configurado para aceitar conexões de qualquer origem (`*`). 
Isso é adequado para uso em rede local/doméstica, mas **NÃO** para produção ou internet pública.

Para uso em produção:
1. Use HTTPS (certificado SSL)
2. Configure CORS para domínios específicos
3. Implemente rate limiting
4. Use variáveis de ambiente para configurações sensíveis

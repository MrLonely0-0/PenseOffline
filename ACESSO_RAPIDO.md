# 🌐 Acesso Rápido - Rede Local

## Para acessar de outros dispositivos (celular, tablet, etc):

### 1️⃣ Inicie o servidor
```powershell
cd backend
.\start_network.ps1
```

### 2️⃣ Configure o Firewall
Execute como Administrador:
```powershell
netsh advfirewall firewall add rule name="Pense Offline" dir=in action=allow protocol=TCP localport=8000
```

### 3️⃣ Acesse do seu celular/outro dispositivo
Use o IP mostrado pelo script (exemplo):
```
http://192.168.1.10:8000
```

**IMPORTANTE:** 
- Dispositivos devem estar na mesma rede Wi-Fi
- Use `http://` não `https://`

---

Para mais detalhes, veja: [NETWORK_ACCESS.md](NETWORK_ACCESS.md)

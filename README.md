# 📵 Pense Offline

Plataforma gamificada para redução do tempo de tela. Ganhe pontos, complete desafios e conquiste sua liberdade digital!

## 🌐 Site Online

**Acesse agora:** [https://mrlonely0-0.github.io/PenseOffline/](https://mrlonely0-0.github.io/PenseOffline/)

Qualquer pessoa pode criar uma conta e começar a usar!

---

## ✨ Funcionalidades

- 🔐 **Sistema de autenticação** completo (cadastro, login, perfil)
- 🎯 **Desafios gamificados** com pontos e níveis
- 📊 **Dashboard pessoal** com estatísticas
- 🏆 **Ranking global** de usuários
- 📱 **Responsivo** - funciona em celular, tablet e desktop
- 🌍 **Acesso público** - disponível na internet

---

## 🚀 Tecnologias

### Backend
- **FastAPI** - Framework web Python
- **SQLModel** - ORM para PostgreSQL
- **Supabase** - Banco de dados PostgreSQL
- **JWT** - Autenticação com tokens
- **Bcrypt** - Hash seguro de senhas

### Frontend
- **HTML5 + CSS3 + JavaScript** puro
- **Bootstrap 3** - Interface responsiva
- **LocalStorage** - Gerenciamento de sessão

### Hospedagem
- **Render.com** - Backend API (gratuito)
- **GitHub Pages** - Frontend estático (gratuito)

---

## 📖 Como Usar

### Opção 1: Acessar Online (Mais Fácil) 🌐

Simplesmente acesse: **https://mrlonely0-0.github.io/PenseOffline/**

Nenhuma instalação necessária!

### Opção 2: Rodar Localmente 💻

#### Pré-requisitos
- Python 3.10+
- PostgreSQL ou Supabase

#### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/MrLonely0-0/PenseOffline.git
cd PenseOffline
```

2. Configure o backend:
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Configure variáveis de ambiente:
Crie `backend/.env`:
```env
DATABASE_URL=postgresql://user:password@host:5432/database
SECRET_KEY=sua-chave-secreta-jwt
```

4. Inicie o servidor:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Acesse: `http://localhost:8000`

---

## 🌍 Deploy na Internet

Quer disponibilizar seu próprio site? Veja os guias:

- **[DEPLOY_PASSO_A_PASSO.md](DEPLOY_PASSO_A_PASSO.md)** - Guia completo para iniciantes
- **[DEPLOY_INTERNET.md](DEPLOY_INTERNET.md)** - Opções de hospedagem
- **[NETWORK_ACCESS.md](NETWORK_ACCESS.md)** - Acesso em rede local

---

## 📱 Uso em Dispositivos Móveis

O site funciona perfeitamente em celulares e tablets!

**Adicionar à tela inicial:**
- **iPhone:** Safari → Compartilhar → "Adicionar à Tela de Início"
- **Android:** Chrome → Menu → "Adicionar à tela inicial"

---

## 🎮 Como Funciona

1. **Cadastre-se** gratuitamente
2. **Registre tempo sem tela** (ganhe 10 pontos por hora)
3. **Complete desafios** (50 a 1000 pontos cada)
4. **Suba de nível** (100 pontos = 1 nível)
5. **Compete no ranking** global

---

## 📊 Estrutura do Projeto

```
PenseOffline/
├── backend/                # API FastAPI
│   ├── app/
│   │   ├── main.py        # Aplicação principal
│   │   ├── models.py      # Modelos do banco
│   │   ├── auth.py        # Autenticação JWT
│   │   └── routers/       # Endpoints da API
│   ├── requirements.txt
│   └── .env.example
├── *.html                 # Páginas do site
├── api-client.js          # Cliente HTTP
├── user-indicator.js      # Componente de usuário
└── web-files/            # CSS, imagens
```

---

## 🔒 Segurança

- ✅ Senhas com hash bcrypt
- ✅ Autenticação JWT
- ✅ CORS configurado
- ✅ Validação de dados
- ✅ HTTPS em produção

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit suas mudanças: `git commit -m 'Adicionar feature X'`
4. Push para a branch: `git push origin minha-feature`
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é open source e está disponível para uso pessoal e educacional.

---

## 👨‍💻 Autor

**MrLonely0-0**
- GitHub: [@MrLonely0-0](https://github.com/MrLonely0-0)
- Repositório: [PenseOffline](https://github.com/MrLonely0-0/PenseOffline)

---

## 🆘 Suporte

Encontrou um bug ou tem uma sugestão?

- Abra uma [Issue](https://github.com/MrLonely0-0/PenseOffline/issues)
- Consulte a [Documentação de Deploy](DEPLOY_PASSO_A_PASSO.md)

---

## 📈 Roadmap Futuro

- [ ] Notificações push
- [ ] Sistema de comunidades
- [ ] Eventos e meetups
- [ ] App mobile nativo
- [ ] Integração com apps de bem-estar
- [ ] Gráficos de progresso avançados
- [ ] Modo escuro

---

## 🎉 Agradecimentos

Obrigado por usar Pense Offline! Juntos, vamos reconquistar nosso tempo e atenção. 📵✨

---

**⭐ Se este projeto te ajudou, deixe uma estrela no GitHub!**

/**
 * API Client para PenseOffline
 * Gerencia autenticação, requisições autenticadas e armazenamento de token JWT
 */

// Detecção automática do URL da API
// Se estiver definido em window.PENSEOFFLINE_API_URL, usar esse valor
// Caso contrário, usar o host atual (para funcionar em rede local)
const API_URL = (typeof window !== 'undefined' && window.PENSEOFFLINE_API_URL) 
  ? window.PENSEOFFLINE_API_URL 
  : (typeof window !== 'undefined' ? `http://${window.location.hostname}:8000` : "http://127.0.0.1:8000");
const TOKEN_KEY = "pensOffline_token";
const USER_KEY = "pensOffline_user";

class APIClient {
  constructor() {
    this.token = localStorage.getItem(TOKEN_KEY);
    this.user = JSON.parse(localStorage.getItem(USER_KEY) || "null");
  }

  // ===== AUTENTICAÇÃO =====

  /**
   * Registrar novo usuário
   * @param {Object} data - { username, email, password, name, phone? }
   */
  async register(data) {
    try {
      const response = await fetch(`${API_URL}/users/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Erro ao registrar");
      }

      const result = await response.json();
      this.setToken(result.access_token, result.user);
      return result;
    } catch (error) {
      console.error("Register error:", error);
      throw error;
    }
  }

  /**
   * Fazer login
   * @param {string} username
   * @param {string} password
   */
  async login(username, password) {
    try {
      const response = await fetch(`${API_URL}/users/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Usuário ou senha incorretos");
      }

      const result = await response.json();
      this.setToken(result.access_token, result.user);
      return result;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  }

  /**
   * Fazer logout
   */
  logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    this.token = null;
    this.user = null;
  }

  /**
   * Armazenar token e usuário
   */
  setToken(token, user) {
    this.token = token;
    this.user = user;
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  /**
   * Obter token JWT
   */
  getAuthHeader() {
    if (!this.token) throw new Error("Não autenticado");
    return { Authorization: `Bearer ${this.token}` };
  }

  /**
   * Verificar se está autenticado
   */
  isAuthenticated() {
    return !!this.token && !!this.user;
  }

  /**
   * Obter dados do usuário do cache
   */
  getUser() {
    return this.user;
  }

  // ===== USUÁRIOS =====

  /**
   * Obter perfil do usuário autenticado
   */
  async getCurrentUser() {
    const response = await fetch(`${API_URL}/users/me`, {
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Erro ao obter usuário");
    const user = await response.json();
    this.setToken(this.token, user);
    return user;
  }

  /**
   * Obter perfil de um usuário por ID
   */
  async getUser(userId) {
    const response = await fetch(`${API_URL}/users/${userId}`, {
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Usuário não encontrado");
    return response.json();
  }

  // ===== COMUNIDADES =====

  /**
   * Listar todas as comunidades
   */
  async getCommunities() {
    const response = await fetch(`${API_URL}/communities/`, {
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Erro ao buscar comunidades");
    return response.json();
  }

  /**
   * Obter comunidade por ID
   */
  async getCommunity(communityId) {
    const response = await fetch(`${API_URL}/communities/${communityId}`, {
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Comunidade não encontrada");
    return response.json();
  }

  /**
   * Criar nova comunidade
   */
  async createCommunity(data) {
    const response = await fetch(`${API_URL}/communities/`, {
      method: "POST",
      headers: {
        ...this.getAuthHeader(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Erro ao criar comunidade");
    return response.json();
  }

  /**
   * Entrar em uma comunidade
   */
  async joinCommunity(communityId) {
    const response = await fetch(`${API_URL}/communities/${communityId}/join`, {
      method: "POST",
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Erro ao entrar na comunidade");
    return response.json();
  }

  /**
   * Sair de uma comunidade
   */
  async leaveCommunity(communityId) {
    const response = await fetch(`${API_URL}/communities/${communityId}/leave`, {
      method: "POST",
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Erro ao sair da comunidade");
    return response.json();
  }

  // ===== EVENTOS =====

  /**
   * Listar todos os eventos
   */
  async getEvents() {
    const response = await fetch(`${API_URL}/events/`, {
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Erro ao buscar eventos");
    return response.json();
  }

  /**
   * Obter evento por ID
   */
  async getEvent(eventId) {
    const response = await fetch(`${API_URL}/events/${eventId}`, {
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Evento não encontrado");
    return response.json();
  }

  /**
   * Criar novo evento
   */
  async createEvent(data) {
    const response = await fetch(`${API_URL}/events/`, {
      method: "POST",
      headers: {
        ...this.getAuthHeader(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Erro ao criar evento");
    return response.json();
  }

  /**
   * Participar/completar um evento (ganhar XP)
   */
  async attendEvent(eventId) {
    const response = await fetch(`${API_URL}/events/${eventId}/attend`, {
      method: "POST",
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Erro ao participar do evento");
    const result = await response.json();
    // Atualizar usuário com novos pontos/XP
    await this.getCurrentUser();
    return result;
  }

  // ===== PRÊMIOS / XP =====

  /**
   * Adicionar tempo sem tela e ganhar pontos
   */
  async addScreenFreeTime(minutes) {
    const response = await fetch(`${API_URL}/rewards/add-time`, {
      method: "POST",
      headers: {
        ...this.getAuthHeader(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ minutos: minutes }),
    });
    if (!response.ok) throw new Error("Erro ao adicionar tempo");
    const result = await response.json();
    // Atualizar usuário
    await this.getCurrentUser();
    return result;
  }

  /**
   * Obter histórico de XP
   */
  async getXPHistory() {
    const response = await fetch(`${API_URL}/users/me/xp_history`, {
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Erro ao buscar histórico");
    return response.json();
  }

  /**
   * Obter ranking global
   */
  async getGlobalStats() {
    const response = await fetch(`${API_URL}/profiles/ranking`, {
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Erro ao buscar ranking");
    return response.json();
  }

  // ===== NOTIFICAÇÕES =====

  /**
   * Obter notificações do usuário
   */
  async getNotifications() {
    const response = await fetch(`${API_URL}/notifications`, {
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Erro ao buscar notificações");
    return response.json();
  }

  /**
   * Marcar notificação como lida
   */
  async markNotificationAsRead(notificationId) {
    const response = await fetch(`${API_URL}/notifications/${notificationId}/read`, {
      method: "POST",
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Erro ao marcar notificação");
    return response.json();
  }

  /**
   * Obter contagem de notificações não lidas
   */
  async getUnreadNotificationsCount() {
    const response = await fetch(`${API_URL}/notifications/unread/count`, {
      headers: this.getAuthHeader(),
    });
    if (!response.ok) throw new Error("Erro ao contar notificações");
    const data = await response.json();
    return data.count;
  }
}

// Exportar instância global
const api = new APIClient();
if (typeof window !== 'undefined') window.PenseOfflineAPI = api;

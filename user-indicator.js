/**
 * Sistema de indicação de usuário logado
 * Adiciona automaticamente indicador de login em todas as páginas
 */

(function() {
  'use strict';

  // Verificar se API client está disponível
  if (typeof api === 'undefined') {
    console.warn('API client não carregado');
    return;
  }

  /**
   * Atualizar navbar com informações do usuário
   */
  function updateNavbar() {
    const navbarRight = document.querySelector('.navbar-nav.navbar-right');
    if (!navbarRight) return;

    // Limpar links de login/entrar existentes se usuário estiver logado
    if (api.isAuthenticated()) {
      const user = api.getUser();
      
      // Remover link "Entrar" se existir
      const loginLinks = navbarRight.querySelectorAll('a[href*="login"]');
      loginLinks.forEach(link => {
        const li = link.parentElement;
        if (li) li.remove();
      });

      // Verificar se já existe indicador de usuário
      let userIndicator = navbarRight.querySelector('.user-indicator');
      
      if (!userIndicator) {
        // Criar indicador de usuário logado
        const li = document.createElement('li');
        li.className = 'dropdown user-indicator';
        li.innerHTML = `
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
            <span class="user-avatar">👤</span>
            <span class="user-name">${user.name || user.username}</span>
            <span class="user-level-badge">Nv. ${user.nivel || 1}</span>
            <span class="caret"></span>
          </a>
          <ul class="dropdown-menu">
            <li class="dropdown-header">
              <strong>${user.name}</strong><br>
              <small>@${user.username}</small>
            </li>
            <li role="separator" class="divider"></li>
            <li><a href="/dashboard.html"><span class="glyphicon glyphicon-dashboard"></span> Dashboard</a></li>
            <li><a href="/perfil.html"><span class="glyphicon glyphicon-user"></span> Meu Perfil</a></li>
            <li><a href="/desafios.html"><span class="glyphicon glyphicon-tasks"></span> Desafios</a></li>
            <li><a href="/ranking.html"><span class="glyphicon glyphicon-star"></span> Ranking</a></li>
            <li role="separator" class="divider"></li>
            <li>
              <a href="#" onclick="api.logout(); window.location.href='/'; return false;">
                <span class="glyphicon glyphicon-log-out"></span> Sair
              </a>
            </li>
          </ul>
        `;
        navbarRight.appendChild(li);

        // Adicionar estilos inline se não existirem
        if (!document.getElementById('user-indicator-styles')) {
          const style = document.createElement('style');
          style.id = 'user-indicator-styles';
          style.textContent = `
            .user-indicator .user-avatar {
              font-size: 18px;
              margin-right: 5px;
            }
            .user-indicator .user-name {
              font-weight: 500;
              margin-right: 8px;
            }
            .user-indicator .user-level-badge {
              background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
              color: white;
              padding: 2px 8px;
              border-radius: 10px;
              font-size: 11px;
              font-weight: bold;
              margin-right: 5px;
            }
            .user-indicator .dropdown-header {
              padding: 10px 20px;
            }
            .user-indicator .dropdown-menu {
              min-width: 200px;
            }
            .user-indicator .dropdown-menu li a {
              padding: 8px 20px;
            }
            .user-indicator .dropdown-menu .glyphicon {
              margin-right: 8px;
              width: 14px;
            }
          `;
          document.head.appendChild(style);
        }
      } else {
        // Atualizar informações do usuário existente
        const nameSpan = userIndicator.querySelector('.user-name');
        const levelSpan = userIndicator.querySelector('.user-level-badge');
        if (nameSpan) nameSpan.textContent = user.name || user.username;
        if (levelSpan) levelSpan.textContent = `Nv. ${user.nivel || 1}`;
      }

      // Adicionar badge de notificações se estiver na API
      loadNotificationBadge();
    }
  }

  /**
   * Carregar badge de notificações não lidas
   */
  async function loadNotificationBadge() {
    try {
      const count = await api.getUnreadNotificationsCount();
      if (count > 0) {
        const userIndicator = document.querySelector('.user-indicator > a');
        if (userIndicator) {
          let badge = userIndicator.querySelector('.notification-badge');
          if (!badge) {
            badge = document.createElement('span');
            badge.className = 'notification-badge badge badge-danger';
            badge.style.cssText = 'position: absolute; top: 8px; right: 8px; background: #dc3545; color: white; border-radius: 10px; padding: 2px 6px; font-size: 10px;';
            userIndicator.style.position = 'relative';
            userIndicator.appendChild(badge);
          }
          badge.textContent = count > 9 ? '9+' : count;
        }
      }
    } catch (err) {
      // Silenciar erro se API de notificações não estiver disponível
    }
  }

  /**
   * Adicionar indicador de status de login em páginas sem navbar
   */
  function addLoginStatusIndicator() {
    // Se já existe navbar, não adicionar indicador extra
    if (document.querySelector('.navbar')) return;

    if (api.isAuthenticated()) {
      const user = api.getUser();
      const indicator = document.createElement('div');
      indicator.id = 'login-status-indicator';
      indicator.innerHTML = `
        <div style="position: fixed; top: 10px; right: 10px; background: white; padding: 10px 20px; border-radius: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 9999;">
          <span style="color: #28a745; font-weight: bold;">● Logado</span>
          <span style="margin-left: 10px;">${user.name || user.username}</span>
          <a href="/dashboard.html" style="margin-left: 15px; color: #667eea; text-decoration: none;">Dashboard</a>
        </div>
      `;
      document.body.appendChild(indicator);
    }
  }

  /**
   * Inicializar quando DOM estiver pronto
   */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      updateNavbar();
      addLoginStatusIndicator();
    });
  } else {
    updateNavbar();
    addLoginStatusIndicator();
  }

  // Atualizar quando usuário fizer login/logout
  window.addEventListener('storage', function(e) {
    if (e.key === 'pensOffline_token') {
      updateNavbar();
    }
  });

  // Expor função para atualização manual
  window.updateUserIndicator = updateNavbar;

})();

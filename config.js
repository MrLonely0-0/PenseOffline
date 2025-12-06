/**
 * Configuração do ambiente para PenseOffline
 * 
 * ✅ URL da API configurada para produção no Vercel
 */

// Detecta automaticamente se está rodando em localhost ou em produção
const isLocalhost = typeof window !== 'undefined' && 
  (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1");

// Configuração da URL da API
if (isLocalhost) {
  // Desenvolvimento local
  window.PENSEOFFLINE_API_URL = 'http://127.0.0.1:8000';
} else {
  // Produção no Vercel
  window.PENSEOFFLINE_API_URL = 'https://pense-offline.vercel.app';
}

// Helper para fazer fetch com a URL correta automaticamente
window.getApiUrl = function(path) {
  const baseUrl = window.PENSEOFFLINE_API_URL || 'http://127.0.0.1:8000';
  // Remove barra inicial do path se existir para evitar duplicação
  const cleanPath = path.startsWith('/') ? path : '/' + path;
  return baseUrl + cleanPath;
};

console.log('[PenseOffline] API URL configurada:', window.PENSEOFFLINE_API_URL);

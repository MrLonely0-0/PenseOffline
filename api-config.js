/**
 * Configuração global da API
 * Detecta automaticamente o URL correto baseado no hostname atual
 */

// Função para obter URL base da API
function getApiUrl() {
  // Se houver configuração manual em window.PENSEOFFLINE_API_URL, usar ela
  if (typeof window !== 'undefined' && window.PENSEOFFLINE_API_URL) {
    return window.PENSEOFFLINE_API_URL;
  }
  
  // Caso contrário, usar o hostname atual com porta 8000
  // Isso permite funcionar tanto localmente quanto em rede local
  if (typeof window !== 'undefined') {
    const protocol = window.location.protocol; // http: ou https:
    const hostname = window.location.hostname; // IP ou localhost
    return `${protocol}//${hostname}:8000`;
  }
  
  // Fallback para localhost
  return 'http://127.0.0.1:8000';
}

// Exportar para uso global
if (typeof window !== 'undefined') {
  window.getApiUrl = getApiUrl;
  window.API_BASE_URL = getApiUrl();
}

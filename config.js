/**
 * Configuração do ambiente para PenseOffline
 * 
 * Este arquivo é OPCIONAL e deve ser incluído ANTES do api-client.js se necessário.
 * 
 * ✅ DETECÇÃO AUTOMÁTICA (Recomendado):
 *   O api-client.js detecta automaticamente o ambiente:
 *   - Localhost (127.0.0.1 ou localhost): usa http://127.0.0.1:8000
 *   - Produção (Vercel/outro): usa a mesma origem do frontend
 * 
 * ⚙️ CONFIGURAÇÃO MANUAL (Apenas se backend em servidor separado):
 *   Se seu backend está em um servidor diferente do frontend (ex: Render, Railway),
 *   descomente e configure a URL abaixo:
 * 
 *   Exemplo: window.PENSEOFFLINE_API_URL = 'https://seu-backend.onrender.com';
 */

// 🔧 BACKEND SEPARADO: Descomente e configure apenas se usar servidor separado
// window.PENSEOFFLINE_API_URL = 'https://seu-backend.onrender.com';

// 💡 DICA: Se frontend e backend estão ambos no Vercel, não precisa configurar nada!

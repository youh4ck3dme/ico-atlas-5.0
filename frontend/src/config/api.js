/**
 * API konfigurácia
 * Automaticky používa HTTPS, ak je dostupný (pre lokálny vývoj s SSL)
 */

// Detekcia, či používame HTTPS
const isHTTPS = window.location.protocol === 'https:';

// API URL - automaticky používa HTTPS, ak je frontend na HTTPS
const getApiUrl = () => {
  // Vite uses import.meta.env with VITE_ prefix
  const apiUrl = import.meta.env.VITE_API_URL;

  if (apiUrl) {
    return apiUrl;
  }

  // Ak je frontend na HTTPS, použij HTTPS aj pre backend
  if (isHTTPS) {
    return 'https://localhost:8000';
  }

  // Inak použij HTTP
  return 'http://localhost:8000';
};

// Debug: Log API URL
console.log('🔧 API URL Configuration:');
console.log('   Current protocol:', window.location.protocol);
console.log('   Is HTTPS:', isHTTPS);
console.log('   API URL:', getApiUrl());

export const API_URL = getApiUrl();

// Export pre použitie v komponentoch
export default API_URL;


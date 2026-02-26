/**
 * API Configuration
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const API_ENDPOINTS = {
  // Furniture
  FURNITURE_LIST: `${API_BASE_URL}/api/furniture`,
  FURNITURE_DETAIL: (id) => `${API_BASE_URL}/api/furniture/${id}`,
  FURNITURE_BATCH: `${API_BASE_URL}/api/furniture/batch`,
  
  // AI
  ANALYZE_ROOM: `${API_BASE_URL}/api/analyze-room`,
  REDESIGN_ROOM: `${API_BASE_URL}/api/redesign`,
  HEALTH: `${API_BASE_URL}/api/health`
};

export default API_BASE_URL;

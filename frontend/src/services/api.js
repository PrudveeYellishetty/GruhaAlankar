/**
 * API Configuration and Service Layer
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || window.location.origin;

class APIService {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...options.headers,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Request failed' }));
        throw new Error(error.error || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Furniture endpoints
  async getFurnitureList(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.request(`/api/furniture?${params}`);
  }

  async getFurnitureById(id) {
    return this.request(`/api/furniture/${id}`);
  }

  async getFurnitureBatch(ids) {
    return this.request('/api/furniture/batch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ids }),
    });
  }

  // AI endpoints
  async analyzeRoom(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);

    return this.request('/api/analyze-room', {
      method: 'POST',
      body: formData,
    });
  }

  async redesignRoom(imageFile, preferences = {}) {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    Object.entries(preferences).forEach(([key, value]) => {
      formData.append(key, value);
    });

    return this.request('/api/redesign', {
      method: 'POST',
      body: formData,
    });
  }

  async healthCheck() {
    return this.request('/api/health');
  }
}

export const api = new APIService(API_BASE_URL);

export const furnitureAPI = {
  getAll: (filters) => api.getFurnitureList(filters),
  getList: (filters) => api.getFurnitureList(filters),
  getById: (id) => api.getFurnitureById(id),
  getBatch: (ids) => api.getFurnitureBatch(ids),
  getByIds: (ids) => api.getFurnitureBatch(ids),
};

export const aiAPI = {
  analyzeRoom: (imageFile) => api.analyzeRoom(imageFile),
  redesignRoom: (imageFile, preferences) => api.redesignRoom(imageFile, preferences),
};

export default api;

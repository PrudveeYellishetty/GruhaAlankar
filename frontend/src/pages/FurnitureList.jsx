import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { furnitureAPI } from '../services/api';
import './FurnitureList.css';

function FurnitureList() {
  const [furniture, setFurniture] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    category: '',
    style: ''
  });

  useEffect(() => {
    loadFurniture();
  }, [filters]);

  const loadFurniture = async () => {
    try {
      setLoading(true);
      const data = await furnitureAPI.getAll(filters);
      setFurniture(data);
      setError(null);
    } catch (err) {
      setError('Failed to load furniture. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading furniture...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="error-container">
          <p className="error-message">{error}</p>
          <button onClick={loadFurniture} className="btn btn-primary">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="furniture-list-page">
      <div className="container">
        <div className="page-header">
          <h1>Furniture Collection</h1>
          <p>Explore our curated collection of AR-ready furniture</p>
        </div>

        <div className="filters">
          <div className="filter-group">
            <label htmlFor="category">Category</label>
            <select
              id="category"
              value={filters.category}
              onChange={(e) => handleFilterChange('category', e.target.value)}
            >
              <option value="">All Categories</option>
              <option value="living">Living Room</option>
              <option value="bedroom">Bedroom</option>
              <option value="dining">Dining</option>
              <option value="office">Office</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="style">Style</label>
            <select
              id="style"
              value={filters.style}
              onChange={(e) => handleFilterChange('style', e.target.value)}
            >
              <option value="">All Styles</option>
              <option value="modern">Modern</option>
              <option value="minimal">Minimal</option>
              <option value="scandinavian">Scandinavian</option>
              <option value="industrial">Industrial</option>
              <option value="traditional">Traditional</option>
            </select>
          </div>
        </div>

        {furniture.length === 0 ? (
          <div className="no-results">
            <p>No furniture found matching your filters.</p>
            <button 
              onClick={() => setFilters({ category: '', style: '' })}
              className="btn btn-secondary"
            >
              Clear Filters
            </button>
          </div>
        ) : (
          <div className="furniture-grid">
            {furniture.map((item) => (
              <Link 
                key={item.id} 
                to={`/furniture/${item.id}`}
                className="furniture-card"
              >
                <div className="furniture-image">
                  <img 
                    src={item.thumbnail_url} 
                    alt={item.name}
                    onError={(e) => {
                      e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="300"%3E%3Crect fill="%23ddd" width="300" height="300"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" text-anchor="middle" dy=".3em"%3ENo Image%3C/text%3E%3C/svg%3E';
                    }}
                  />
                </div>
                <div className="furniture-info">
                  <h3>{item.name}</h3>
                  <div className="furniture-meta">
                    <span className="category">{item.category}</span>
                    <span className="style">{item.style}</span>
                  </div>
                  {item.dimensions && (
                    <p className="dimensions">
                      {item.dimensions.width}m × {item.dimensions.depth}m × {item.dimensions.height}m
                    </p>
                  )}
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default FurnitureList;

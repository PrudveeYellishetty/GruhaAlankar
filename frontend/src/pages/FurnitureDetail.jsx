import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { furnitureAPI } from '../services/api';
import './FurnitureDetail.css';

function FurnitureDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [furniture, setFurniture] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedColor, setSelectedColor] = useState('');

  useEffect(() => {
    loadFurnitureDetail();
  }, [id]);

  const loadFurnitureDetail = async () => {
    try {
      setLoading(true);
      const data = await furnitureAPI.getById(id);
      setFurniture(data);
      if (data.available_colors && data.available_colors.length > 0) {
        setSelectedColor(data.available_colors[0]);
      }
      setError(null);
    } catch (err) {
      setError('Failed to load furniture details.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleViewInAR = () => {
    navigate(`/ar/${id}`, { 
      state: { 
        furniture,
        color: selectedColor 
      } 
    });
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading furniture details...</p>
        </div>
      </div>
    );
  }

  if (error || !furniture) {
    return (
      <div className="container">
        <div className="error-container">
          <p className="error-message">{error || 'Furniture not found'}</p>
          <button onClick={() => navigate('/furniture')} className="btn btn-primary">
            Back to Furniture
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="furniture-detail-page">
      <div className="container">
        <button onClick={() => navigate(-1)} className="back-button">
          ← Back
        </button>

        <div className="detail-container">
          <div className="detail-image">
            <img 
              src={furniture.thumbnail_url} 
              alt={furniture.name}
              onError={(e) => {
                e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="600" height="600"%3E%3Crect fill="%23ddd" width="600" height="600"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" text-anchor="middle" dy=".3em"%3ENo Image%3C/text%3E%3C/svg%3E';
              }}
            />
          </div>

          <div className="detail-info">
            <h1>{furniture.name}</h1>
            
            <div className="meta-info">
              <span className="category">{furniture.category}</span>
              <span className="style">{furniture.style}</span>
            </div>

            {furniture.description && (
              <p className="description">{furniture.description}</p>
            )}

            {furniture.dimensions && (
              <div className="dimensions-info">
                <h3>Dimensions</h3>
                <div className="dimensions-grid">
                  <div>
                    <span className="label">Width</span>
                    <span className="value">{furniture.dimensions.width}m</span>
                  </div>
                  <div>
                    <span className="label">Depth</span>
                    <span className="value">{furniture.dimensions.depth}m</span>
                  </div>
                  <div>
                    <span className="label">Height</span>
                    <span className="value">{furniture.dimensions.height}m</span>
                  </div>
                </div>
              </div>
            )}

            {furniture.available_colors && furniture.available_colors.length > 0 && (
              <div className="color-selector">
                <h3>Available Colors</h3>
                <div className="color-options">
                  {furniture.available_colors.map((color) => (
                    <button
                      key={color}
                      className={`color-option ${selectedColor === color ? 'selected' : ''}`}
                      style={{ backgroundColor: color }}
                      onClick={() => setSelectedColor(color)}
                      title={color}
                    />
                  ))}
                </div>
              </div>
            )}

            <div className="actions">
              <button 
                onClick={handleViewInAR}
                className="btn btn-primary btn-large"
              >
                View in AR
              </button>
            </div>

            {furniture.tags && furniture.tags.length > 0 && (
              <div className="tags">
                {furniture.tags.map((tag, index) => (
                  <span key={index} className="tag">{tag}</span>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default FurnitureDetail;

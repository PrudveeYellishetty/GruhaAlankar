import React, { useEffect, useRef, useState } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { furnitureAPI } from '../services/api';
import ARScene from '../components/AR/ARScene';
import './ARViewer.css';

function ARViewer() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  
  const [furniture, setFurniture] = useState(null);
  const [selectedColor, setSelectedColor] = useState('#808080');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [arSupported, setArSupported] = useState(false);

  useEffect(() => {
    checkARSupport();
    loadFurniture();
  }, [id]);

  const checkARSupport = async () => {
    if ('xr' in navigator) {
      try {
        const supported = await navigator.xr.isSessionSupported('immersive-ar');
        setArSupported(supported);
        if (!supported) {
          setError('WebXR AR is not supported on this device. Please use AR-compatible browser on Android.');
        }
      } catch (err) {
        console.error('Error checking AR support:', err);
        setArSupported(false);
        setError('Unable to check AR support. Please use HTTPS and an AR-capable device.');
      }
    } else {
      setArSupported(false);
      setError('WebXR is not available. Please use Chrome on Android with AR support.');
    }
  };

  const loadFurniture = async () => {
    try {
      setLoading(true);
      
      // Check if furniture data is passed via navigation state
      if (location.state?.furniture) {
        const furnitureData = location.state.furniture;
        setFurniture(furnitureData);
        if (location.state?.color) {
          setSelectedColor(location.state.color);
        } else if (furnitureData.available_colors?.[0]) {
          setSelectedColor(furnitureData.available_colors[0]);
        }
      } else if (id) {
        // Load from API
        const data = await furnitureAPI.getById(id);
        setFurniture(data);
        if (data.available_colors?.[0]) {
          setSelectedColor(data.available_colors[0]);
        }
      } else {
        setError('No furniture selected');
      }
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load furniture');
      console.error(err);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="ar-viewer-page">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading AR viewer...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="ar-viewer-page">
        <div className="error-container">
          <h2>⚠️ AR Not Available</h2>
          <p className="error-message">{error}</p>
          <div className="error-info">
            <h3>Requirements:</h3>
            <ul>
              <li>Android device with ARCore support</li>
              <li>Chrome browser (latest version)</li>
              <li>HTTPS connection</li>
              <li>Camera permissions enabled</li>
            </ul>
          </div>
          <button onClick={() => navigate(-1)} className="btn btn-primary">
            Go Back
          </button>
        </div>
      </div>
    );
  }

  if (!furniture) {
    return (
      <div className="ar-viewer-page">
        <div className="error-container">
          <p>No furniture selected</p>
          <button onClick={() => navigate('/furniture')} className="btn btn-primary">
            Browse Furniture
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="ar-viewer-page">
      <ARScene
        modelUrl={furniture.model_url}
        color={selectedColor}
        furnitureName={furniture.name}
        arSupported={arSupported}
      />
      
      <div className="ar-controls">
        <div className="furniture-info-bar">
          <div className="info-content">
            <h3>{furniture.name}</h3>
            <p className="dimensions">
              {furniture.dimensions?.width}m × {furniture.dimensions?.depth}m × {furniture.dimensions?.height}m
            </p>
          </div>
          
          <button
            onClick={() => navigate(-1)}
            className="close-btn"
          >
            ✕
          </button>
        </div>

        {furniture.available_colors && furniture.available_colors.length > 1 && (
          <div className="color-selector-bar">
            <span className="color-label">Color:</span>
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

        <div className="instructions">
          <p>📱 Tap "Start AR" to begin</p>
          <p>👆 Tap on surface to place furniture</p>
          <p>🔄 Pinch to scale, drag to rotate</p>
        </div>
      </div>
    </div>
  );
}

export default ARViewer;

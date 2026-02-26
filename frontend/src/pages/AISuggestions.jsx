import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { furnitureAPI } from '../services/api';
import './AISuggestions.css';

function AISuggestions() {
  const location = useLocation();
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [furnitureDetails, setFurnitureDetails] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!location.state?.result) {
      navigate('/upload');
      return;
    }

    loadSuggestions();
  }, []);

  const loadSuggestions = async () => {
    try {
      const resultData = location.state.result;
      setResult(resultData);

      // Load full furniture details for recommended assets
      if (resultData.assets && resultData.assets.length > 0) {
        const assetIds = resultData.assets.map(asset => asset.asset_id);
        const furniture = await furnitureAPI.getByIds(assetIds);
        
        // Merge with AI data (color, reason)
        const mergedData = furniture.map(item => {
          const aiData = resultData.assets.find(a => a.asset_id === item.id);
          return {
            ...item,
            ...aiData
          };
        });
        
        setFurnitureDetails(mergedData);
      }
      
      setLoading(false);
    } catch (err) {
      console.error('Error loading suggestions:', err);
      setLoading(false);
    }
  };

  const handleViewInAR = (furniture) => {
    navigate(`/ar/${furniture.id}`, {
      state: {
        furniture,
        color: furniture.color
      }
    });
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading suggestions...</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  const isRedesign = result.mode === 'redesign';

  return (
    <div className="ai-suggestions-page">
      <div className="container">
        <div className="page-header">
          <h1>
            {isRedesign ? '🎨 Redesign Preview' : '🤖 AI Recommendations'}
          </h1>
          <p>
            {isRedesign 
              ? 'Here are AI-generated redesign concepts for your space'
              : 'Based on your room analysis, here are personalized furniture suggestions'
            }
          </p>
        </div>

        {!isRedesign && result.analysis && (
          <div className="analysis-card">
            <h2>Room Analysis</h2>
            <div className="analysis-grid">
              <div className="analysis-item">
                <span className="analysis-label">Room Type</span>
                <span className="analysis-value">{result.analysis.room_type}</span>
              </div>
              <div className="analysis-item">
                <span className="analysis-label">Style</span>
                <span className="analysis-value">{result.analysis.style}</span>
              </div>
              <div className="analysis-item">
                <span className="analysis-label">Confidence</span>
                <span className="analysis-value">
                  {Math.round(result.analysis.confidence * 100)}%
                </span>
              </div>
            </div>
            
            {result.analysis.color_scheme && result.analysis.color_scheme.length > 0 && (
              <div className="color-palette">
                <span className="analysis-label">Detected Colors:</span>
                <div className="color-swatches">
                  {result.analysis.color_scheme.map((color, index) => (
                    <div
                      key={index}
                      className="color-swatch"
                      style={{ backgroundColor: color }}
                      title={color}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {isRedesign && result.generated_images && result.generated_images.length > 0 && (
          <div className="redesign-images">
            <h2>Generated Designs</h2>
            <div className="images-grid">
              {result.generated_images.map((imageUrl, index) => (
                <div key={index} className="redesign-image-card">
                  <img src={imageUrl} alt={`Redesign ${index + 1}`} />
                </div>
              ))}
            </div>
          </div>
        )}

        {furnitureDetails.length > 0 && (
          <div className="recommendations-section">
            <h2>Recommended Furniture</h2>
            <div className="furniture-grid">
              {furnitureDetails.map((item) => (
                <div key={item.id} className="suggestion-card">
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
                    
                    {item.reason && (
                      <p className="recommendation-reason">
                        💡 {item.reason}
                      </p>
                    )}
                    
                    {item.confidence && (
                      <div className="confidence-bar">
                        <div className="confidence-label">
                          Match: {Math.round(item.confidence * 100)}%
                        </div>
                        <div className="confidence-progress">
                          <div 
                            className="confidence-fill"
                            style={{ width: `${item.confidence * 100}%` }}
                          />
                        </div>
                      </div>
                    )}
                    
                    {item.color && (
                      <div className="suggested-color">
                        <span>Suggested Color:</span>
                        <div
                          className="color-preview"
                          style={{ backgroundColor: item.color }}
                          title={item.color}
                        />
                      </div>
                    )}
                    
                    <div className="card-actions">
                      <button
                        onClick={() => navigate(`/furniture/${item.id}`)}
                        className="btn btn-outline"
                      >
                        View Details
                      </button>
                      <button
                        onClick={() => handleViewInAR(item)}
                        className="btn btn-primary"
                      >
                        View in AR
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {furnitureDetails.length === 0 && (
          <div className="no-suggestions">
            <p>No furniture recommendations available at this time.</p>
            <button
              onClick={() => navigate('/furniture')}
              className="btn btn-secondary"
            >
              Browse All Furniture
            </button>
          </div>
        )}

        <div className="action-buttons">
          <button onClick={() => navigate('/upload')} className="btn btn-outline">
            Try Another Image
          </button>
          <button onClick={() => navigate('/furniture')} className="btn btn-secondary">
            Browse All Furniture
          </button>
        </div>
      </div>
    </div>
  );
}

export default AISuggestions;

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { aiAPI } from '../services/api';
import './UploadRoom.css';

function UploadRoom() {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [mode, setMode] = useState('recommendation'); // 'recommendation' or 'redesign'
  const [preferences, setPreferences] = useState({
    style: 'modern',
    color_scheme: 'neutral',
    furniture_focus: 'overall ambiance'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Please select an image file');
        return;
      }
      
      if (file.size > 16 * 1024 * 1024) {
        setError('File size must be less than 16MB');
        return;
      }

      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setError(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      setError('Please select an image');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      let result;
      if (mode === 'recommendation') {
        result = await aiAPI.analyzeRoom(selectedFile);
      } else {
        result = await aiAPI.redesignRoom(selectedFile, preferences);
      }

      // Navigate to suggestions page with result data
      navigate('/suggestions', { state: { result } });
      
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process image. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handlePreferenceChange = (key, value) => {
    setPreferences(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <div className="upload-room-page">
      <div className="container">
        <div className="page-header">
          <h1>AI-Powered Interior Design</h1>
          <p>Upload a photo of your room to get intelligent recommendations or redesign previews</p>
        </div>

        <div className="mode-selector">
          <button
            className={`mode-btn ${mode === 'recommendation' ? 'active' : ''}`}
            onClick={() => setMode('recommendation')}
          >
            🤖 AI Recommendations
          </button>
          <button
            className={`mode-btn ${mode === 'redesign' ? 'active' : ''}`}
            onClick={() => setMode('redesign')}
          >
            🎨 Redesign Preview
          </button>
        </div>

        <div className="upload-container">
          <form onSubmit={handleSubmit}>
            <div className="upload-area">
              {previewUrl ? (
                <div className="preview-container">
                  <img src={previewUrl} alt="Room preview" />
                  <button
                    type="button"
                    className="change-image-btn"
                    onClick={() => {
                      setSelectedFile(null);
                      setPreviewUrl(null);
                    }}
                  >
                    Change Image
                  </button>
                </div>
              ) : (
                <label className="file-input-label">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="file-input"
                  />
                  <div className="upload-placeholder">
                    <div className="upload-icon">📸</div>
                    <p>Click to upload room image</p>
                    <span className="file-hint">PNG, JPG, JPEG or WEBP (max 16MB)</span>
                  </div>
                </label>
              )}
            </div>

            {mode === 'redesign' && selectedFile && (
              <div className="preferences-section">
                <h3>Design Preferences</h3>
                
                <div className="preference-group">
                  <label>Style</label>
                  <select
                    value={preferences.style}
                    onChange={(e) => handlePreferenceChange('style', e.target.value)}
                  >
                    <option value="modern">Modern</option>
                    <option value="minimal">Minimal</option>
                    <option value="scandinavian">Scandinavian</option>
                    <option value="industrial">Industrial</option>
                    <option value="traditional">Traditional</option>
                  </select>
                </div>

                <div className="preference-group">
                  <label>Color Scheme</label>
                  <select
                    value={preferences.color_scheme}
                    onChange={(e) => handlePreferenceChange('color_scheme', e.target.value)}
                  >
                    <option value="neutral">Neutral</option>
                    <option value="warm">Warm Tones</option>
                    <option value="cool">Cool Tones</option>
                    <option value="monochrome">Monochrome</option>
                    <option value="vibrant">Vibrant Colors</option>
                  </select>
                </div>

                <div className="preference-group">
                  <label>Focus</label>
                  <input
                    type="text"
                    value={preferences.furniture_focus}
                    onChange={(e) => handlePreferenceChange('furniture_focus', e.target.value)}
                    placeholder="e.g., cozy reading corner, spacious living area"
                  />
                </div>
              </div>
            )}

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            <div className="submit-section">
              <button
                type="submit"
                className="btn btn-primary btn-large"
                disabled={!selectedFile || loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Processing...
                  </>
                ) : mode === 'recommendation' ? (
                  'Get Recommendations'
                ) : (
                  'Generate Redesign'
                )}
              </button>
            </div>
          </form>
        </div>

        <div className="info-section">
          <h3>How it works</h3>
          <div className="info-grid">
            {mode === 'recommendation' ? (
              <>
                <div className="info-item">
                  <div className="info-number">1</div>
                  <p>Upload a clear photo of your room</p>
                </div>
                <div className="info-item">
                  <div className="info-number">2</div>
                  <p>AI analyzes room style and available space</p>
                </div>
                <div className="info-item">
                  <div className="info-number">3</div>
                  <p>Get personalized furniture recommendations</p>
                </div>
                <div className="info-item">
                  <div className="info-number">4</div>
                  <p>View suggested items in AR</p>
                </div>
              </>
            ) : (
              <>
                <div className="info-item">
                  <div className="info-number">1</div>
                  <p>Upload your current room photo</p>
                </div>
                <div className="info-item">
                  <div className="info-number">2</div>
                  <p>Choose your preferred style</p>
                </div>
                <div className="info-item">
                  <div className="info-number">3</div>
                  <p>AI generates redesigned room concepts</p>
                </div>
                <div className="info-item">
                  <div className="info-number">4</div>
                  <p>Explore before/after comparisons</p>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default UploadRoom;

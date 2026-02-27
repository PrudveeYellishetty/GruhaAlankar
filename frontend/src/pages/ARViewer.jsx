import React, { useState, useEffect, useRef } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { furnitureAPI } from '../services/api';
import './ARViewer.css';

const CAMERA_PRESETS = [
  { label: 'Front', icon: '🔲', orbit: '0deg 75deg 2.5m' },
  { label: 'Side', icon: '◻️', orbit: '90deg 75deg 2.5m' },
  { label: 'Top', icon: '⬜', orbit: '0deg 0deg 3m' },
  { label: 'Corner', icon: '🔳', orbit: '45deg 60deg 2.5m' },
  { label: 'Low', icon: '📐', orbit: '30deg 85deg 2m' },
];

const ENVIRONMENTS = [
  { label: 'Studio', value: 'neutral', icon: '💡' },
  { label: 'Outdoor', value: 'legacy', icon: '🌤️' },
  { label: 'None', value: '', icon: '⚫' },
];

function ARViewer() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const viewerRef = useRef(null);

  const [furniture, setFurniture] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [autoRotate, setAutoRotate] = useState(true);
  const [wireframe, setWireframe] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(100);
  const [activeEnv, setActiveEnv] = useState('neutral');
  const [showControls, setShowControls] = useState(true);
  const [modelLoaded, setModelLoaded] = useState(false);

  useEffect(() => {
    loadFurniture();
  }, [id]);

  useEffect(() => {
    const viewer = viewerRef.current;
    if (!viewer) return;

    const onLoad = () => setModelLoaded(true);
    viewer.addEventListener('load', onLoad);
    return () => viewer.removeEventListener('load', onLoad);
  }, [furniture]);

  const loadFurniture = async () => {
    try {
      setLoading(true);
      if (location.state?.furniture) {
        setFurniture(location.state.furniture);
      } else if (id) {
        const data = await furnitureAPI.getById(id);
        setFurniture(data);
      } else {
        setError('No furniture selected');
      }
      setLoading(false);
    } catch (err) {
      setError('Failed to load furniture');
      setLoading(false);
    }
  };

  const setCameraOrbit = (orbit) => {
    const viewer = viewerRef.current;
    if (viewer) {
      viewer.cameraOrbit = orbit;
      viewer.jumpCameraToGoal();
    }
  };

  const handleZoom = (value) => {
    setZoomLevel(value);
    const viewer = viewerRef.current;
    if (viewer) {
      const distance = 5 - (value / 100) * 4; // 5m at 0%, 1m at 100%
      const currentOrbit = viewer.getCameraOrbit();
      viewer.cameraOrbit = `${currentOrbit.theta}rad ${currentOrbit.phi}rad ${distance}m`;
    }
  };

  const resetCamera = () => {
    const viewer = viewerRef.current;
    if (viewer) {
      viewer.cameraOrbit = '45deg 60deg 2.5m';
      viewer.cameraTarget = 'auto auto auto';
      viewer.jumpCameraToGoal();
      setZoomLevel(100);
      setAutoRotate(true);
    }
  };

  if (loading) {
    return (
      <div className="fullscreen-viewer">
        <div className="viewer-loading">
          <div className="loading-ring"></div>
          <p>Loading 3D model...</p>
        </div>
      </div>
    );
  }

  if (error || !furniture) {
    return (
      <div className="fullscreen-viewer">
        <div className="viewer-error">
          <p>{error || 'Furniture not found'}</p>
          <button onClick={() => navigate('/furniture')} className="btn btn-primary">
            Browse Furniture
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fullscreen-viewer">
      <model-viewer
        ref={viewerRef}
        src={furniture.model_url}
        alt={furniture.name}
        ar
        ar-modes="webxr scene-viewer quick-look"
        ar-placement="floor"
        camera-controls
        touch-action="pan-y"
        auto-rotate={autoRotate ? '' : undefined}
        {...(autoRotate ? { 'auto-rotate': '' } : {})}
        shadow-intensity="1.2"
        shadow-softness="0.8"
        environment-image={activeEnv}
        exposure="1.1"
        camera-orbit="45deg 60deg 2.5m"
        min-camera-orbit="auto auto 0.5m"
        max-camera-orbit="auto auto 8m"
        interpolation-decay="100"
        style={{
          width: '100%',
          height: '100%',
          backgroundColor: '#12121a',
          '--poster-color': '#12121a',
        }}
      >
        <button slot="ar-button" className="ar-launch-btn">
          <span className="ar-icon">📱</span> View in Your Room
        </button>

        <div className="model-loading-bar" slot="progress-bar">
          <div className="model-loading-fill"></div>
        </div>
      </model-viewer>

      {/* Top bar */}
      <div className="top-bar">
        <button onClick={() => navigate(-1)} className="top-btn back-btn">
          ← Back
        </button>
        <h2 className="viewer-title">{furniture.name}</h2>
        <button
          onClick={() => setShowControls(!showControls)}
          className="top-btn toggle-controls-btn"
          title={showControls ? 'Hide controls' : 'Show controls'}
        >
          {showControls ? '✕' : '⚙️'}
        </button>
      </div>

      {/* Control panel */}
      {showControls && (
        <div className="control-panel">
          {/* Camera presets */}
          <div className="control-section">
            <span className="section-label">Camera</span>
            <div className="preset-row">
              {CAMERA_PRESETS.map((p) => (
                <button
                  key={p.label}
                  className="preset-btn"
                  onClick={() => setCameraOrbit(p.orbit)}
                  title={p.label}
                >
                  <span className="preset-icon">{p.icon}</span>
                  <span className="preset-label">{p.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Zoom */}
          <div className="control-section">
            <span className="section-label">Zoom</span>
            <div className="slider-row">
              <span className="slider-icon">−</span>
              <input
                type="range"
                min="20"
                max="200"
                value={zoomLevel}
                onChange={(e) => handleZoom(Number(e.target.value))}
                className="zoom-slider"
              />
              <span className="slider-icon">+</span>
            </div>
          </div>

          {/* Lighting */}
          <div className="control-section">
            <span className="section-label">Lighting</span>
            <div className="preset-row">
              {ENVIRONMENTS.map((env) => (
                <button
                  key={env.label}
                  className={`preset-btn ${activeEnv === env.value ? 'active' : ''}`}
                  onClick={() => setActiveEnv(env.value)}
                >
                  <span className="preset-icon">{env.icon}</span>
                  <span className="preset-label">{env.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Toggles */}
          <div className="control-section toggles-row">
            <button
              className={`toggle-btn ${autoRotate ? 'active' : ''}`}
              onClick={() => {
                setAutoRotate(!autoRotate);
                const v = viewerRef.current;
                if (v) {
                  if (autoRotate) v.removeAttribute('auto-rotate');
                  else v.setAttribute('auto-rotate', '');
                }
              }}
            >
              🔄 Auto-Rotate
            </button>
            <button className="toggle-btn" onClick={resetCamera}>
              🎯 Reset View
            </button>
          </div>
        </div>
      )}

      {/* Bottom info */}
      <div className="bottom-bar">
        <div className="bottom-tags">
          <span className="bottom-tag">{furniture.category}</span>
          <span className="bottom-tag">{furniture.style}</span>
          {furniture.dimensions && (
            <span className="bottom-dims">
              {furniture.dimensions.width}m × {furniture.dimensions.depth}m × {furniture.dimensions.height}m
            </span>
          )}
        </div>
        <p className="bottom-hint">Drag to rotate · Pinch to zoom · AR button for your room</p>
      </div>
    </div>
  );
}

export default ARViewer;

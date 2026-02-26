import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
  return (
    <div className="home">
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <h1 className="hero-title">Transform Your Space with AI-Powered AR Interior Design</h1>
            <p className="hero-subtitle">
              Browse furniture, get AI recommendations, and visualize designs in your real space using augmented reality.
            </p>
            <div className="hero-actions">
              <Link to="/furniture" className="btn btn-primary btn-large">
                Browse Furniture
              </Link>
              <Link to="/upload" className="btn btn-outline btn-large">
                Try AI Design
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="features">
        <div className="container">
          <h2 className="section-title">How It Works</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🪑</div>
              <h3>Browse Furniture</h3>
              <p>Explore our curated collection of 3D furniture models optimized for AR viewing.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI Recommendations</h3>
              <p>Upload a photo of your room and get intelligent furniture suggestions powered by AI.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🎨</div>
              <h3>Redesign Preview</h3>
              <p>Generate AI-powered redesign concepts to visualize different interior styles.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📱</div>
              <h3>AR Placement</h3>
              <p>View furniture in your real space using WebXR augmented reality on your mobile device.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta">
        <div className="container">
          <h2>Ready to Transform Your Space?</h2>
          <p>Start your interior design journey today</p>
          <Link to="/upload" className="btn btn-primary btn-large">
            Get Started
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Home;

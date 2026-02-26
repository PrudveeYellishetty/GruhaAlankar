import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import './Layout.css';

function Layout() {
  return (
    <div className="layout">
      <Header />
      <main className="main-content">
        <Outlet />
      </main>
      <footer className="footer">
        <div className="container">
          <p>&copy; 2026 GruhaAlankar. AI-powered AR Interior Design.</p>
        </div>
      </footer>
    </div>
  );
}

export default Layout;

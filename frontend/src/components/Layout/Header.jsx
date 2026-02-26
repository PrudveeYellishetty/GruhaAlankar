import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Header.css';

function Header() {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <header className="header">
      <div className="container">
        <nav className="nav">
          <Link to="/" className="logo">
            <h1>GruhaAlankar</h1>
          </Link>
          
          <ul className="nav-links">
            <li>
              <Link to="/" className={isActive('/')}>Home</Link>
            </li>
            <li>
              <Link to="/furniture" className={isActive('/furniture')}>Furniture</Link>
            </li>
            <li>
              <Link to="/upload" className={isActive('/upload')}>AI Design</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;

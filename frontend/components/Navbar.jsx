import React from 'react'
import { Link } from 'react-router-dom';
// import '../components/nav.css'

export default function NavBar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <ul className="nav-links">
        <li className="logo"></li> <br />
          <li className="nav-item">
            <Link to="/" className="nav-link">Home</Link> 
          </li> <br />
          <li className="nav-item">
            <Link to="/alerts" className="nav-link">Alerts</Link>
          </li> <br />
          <li className="nav-item">
            <Link to="/awareness" className="nav-link">Awareness</Link>
          </li> <br />
          <li className="nav-item">
            <Link to="/emergency" className="nav-link">Emergency Details</Link>
          </li> 
        </ul>
      </div>
    </nav>
  )
}


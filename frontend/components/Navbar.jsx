import React from 'react'
import { Link } from 'react-router-dom';
 import '../components/nav.css'

export default function NavBar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <ul className="nav-links">
        <li className="logo"></li> 
          <li className="nav-item">
            <Link to="/" className="nav-link"><b>Home</b></Link> 
          </li> 
          <li className="nav-item">
            <Link to="/alerts" className="nav-link"><b>Alerts</b></Link>
          </li> 
          <li className="nav-item">
            <Link to="/awareness" className="nav-link"><b>Awareness</b></Link>
          </li> 
          <li className="nav-item">
            <Link to="/emergency" className="nav-link"><b>Emergency Details</b></Link>
          </li> 
        </ul>
      </div>
    </nav>
  )
}


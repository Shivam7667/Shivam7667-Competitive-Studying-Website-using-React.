import React from 'react';
import { Link } from 'react-router-dom';
import './Dashboard.css'; // Import the CSS file

function Dashboard() {
  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Welcome to the Competitive Studying Platform!</h1>
      <nav className="dashboard-nav">
        <Link to="/friends" className="nav-link">Admin Panel</Link>
        <Link to="/timer" className="nav-link">Manage Friends</Link>
        <Link to="/admin" className="nav-link">Study Timer</Link>
        {/* New Button for Study Materials */}
        <a href="http://localhost:3000/study/sessions" className="nav-link">Study Materials</a>
      </nav>
    </div>
  );
}

export default Dashboard;

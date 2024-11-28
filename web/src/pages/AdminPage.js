import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './AdminPage.css'; // Import the CSS file

function AdminPage() {
  const [adminData, setAdminData] = useState({ total_users: 0, total_sessions: 0 });

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/admin/overview');
        setAdminData(response.data);
      } catch (error) {
        console.error('Error fetching admin data:', error);
      }
    };

    fetchAdminData();
  }, []);

  return (
    <div className="admin-page-container">
      <h1 className="admin-page-title">Admin Panel</h1>
      <div className="admin-data-container">
        <p className="admin-data-item"><strong>Total Users:</strong> {adminData.total_users}</p>
        <p className="admin-data-item"><strong>Total Study Sessions:</strong> {adminData.total_sessions}</p>
      </div>
    </div>
  );
}

export default AdminPage;

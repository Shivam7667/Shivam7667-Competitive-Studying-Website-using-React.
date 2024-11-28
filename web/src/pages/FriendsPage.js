import React from 'react';
import FriendManagement from '../components/FriendManagement';
import FriendRequests from '../components/FriendRequests';
import './FriendsPage.css'; // Import the CSS file

function FriendsPage() {
  return (
    <div className="friends-page-container">
      <h1 className="friends-page-title">Friends Management</h1>
      <div className="friends-page-content">
        <FriendManagement />
        <FriendRequests />
      </div>
    </div>
  );
}

export default FriendsPage;


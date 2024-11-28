import React, { useState, useEffect } from 'react';
import { getFriendsList, sendFriendRequest } from './friendService';

function FriendManagement() {
  const [friends, setFriends] = useState([]);
  const [newFriendEmail, setNewFriendEmail] = useState('');

  useEffect(() => {
    fetchFriends();
  }, []);

  const fetchFriends = async () => {
    try {
      const response = await getFriendsList();
      setFriends(response);
    } catch (error) {
      console.error('Error fetching friends list:', error);
      alert(error.message); // Show error message to user
    }
  };

  const handleSendFriendRequest = async () => {
    try {
      await sendFriendRequest(newFriendEmail);
      setNewFriendEmail('');  // Clear input after sending
      fetchFriends();  // Optionally refresh friends list
    } catch (error) {
      console.error('Error sending friend request:', error);
      alert(error.message); // Show error message to user
    }
  };

  return (
    <div>
      <h2>Friends List</h2>
      {friends.length > 0 ? (
        friends.map((friend) => <div key={friend._id}>{friend.name}</div>)
      ) : (
        <p>No friends found</p>
      )}
      <input
        type="email"
        value={newFriendEmail}
        onChange={(e) => setNewFriendEmail(e.target.value)}
        placeholder="Friend's email"
      />
      <button onClick={handleSendFriendRequest}>Send Friend Request</button>
    </div>
  );
}

export default FriendManagement;

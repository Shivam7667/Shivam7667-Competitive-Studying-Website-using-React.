import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000';

export default function StudyHistory() {
  const [history, setHistory] = useState([]);
  const [userId] = useState('user_id_here');  // Replace with actual user ID

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/study/history`, {
        params: { user_id: userId },
      });
      setHistory(response.data);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div>
      <h2></h2>
      <ul>
        {history.map(session => (
          <li key={session.session_id}>
            Session ID: {session.session_id}, Start Time: {session.start_time}, End Time: {session.end_time}
          </li>
        ))}
      </ul>
    </div>
  );
}

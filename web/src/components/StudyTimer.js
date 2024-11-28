import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000';

export default function StudyTimer() {
  const [time, setTime] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [userId] = useState('user_id_here');  // Replace with actual user ID

  const startTimer = async () => {
    try {
      const response = await axios.post(`${API_URL}/study/start`, {
        user_id: userId,
        start_time: new Date().toISOString(),
      });
      setSessionId(response.data.session_id);
      setIsActive(true);
    } catch (error) {
      console.error('Error starting session:', error);
    }
  };

  const stopTimer = async () => {
    try {
      if (sessionId) {
        await axios.put(`${API_URL}/study/stop`, {
          session_id: sessionId,
          end_time: new Date().toISOString(),
        });
        setIsActive(false);
        setTime(0); // Reset the timer
      }
    } catch (error) {
      console.error('Error stopping session:', error);
    }
  };

  useEffect(() => {
    let interval = null;
    if (isActive) {
      interval = setInterval(() => {
        setTime((prevTime) => prevTime + 1);
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isActive]);

  return (
    <div>
      <h2>Timer: {time}s</h2>
      <button onClick={startTimer} disabled={isActive}>Start</button>
      <button onClick={stopTimer} disabled={!isActive}>Stop</button>
    </div>
  );
}

import axios from 'axios';

const API_URL = 'http://localhost:5000/study';

export const startStudySession = async () => {
  try {
    return await axios.post(`${API_URL}/start`);
  } catch (error) {
    console.error('Error starting study session:', error);
    throw error;
  }
};

export const stopStudySession = async (sessionId) => {
  try {
    return await axios.put(`${API_URL}/stop`, { session_id: sessionId });
  } catch (error) {
    console.error('Error stopping study session:', error);
    throw error;
  }
};

export const getStudyHistory = async () => {
  try {
    return await axios.get(`${API_URL}/history`);
  } catch (error) {
    console.error('Error fetching study history:', error);
    throw error;
  }
};


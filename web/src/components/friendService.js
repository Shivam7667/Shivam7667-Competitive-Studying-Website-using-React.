import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const getPendingRequests = async () => {
    const userId = localStorage.getItem('userId');  
    if (!userId) {
        console.error('User ID is not available'); // Log this for debugging
        throw new Error('User ID is not available');
    }

    try {
        const response = await axios.get(`${API_URL}/friends/requests/${userId}`);
        return response.data; 
    } catch (error) {
        console.error('Error fetching pending requests:', error);
        throw error;
    }
};

export const getFriendsList = async () => {
    const userId = localStorage.getItem('userId');  
    if (!userId) {
        console.error('User ID is not available');
        throw new Error('User ID is not available');
    }

    try {
        const response = await axios.get(`${API_URL}/friends/list/${userId}`);
        return response.data; 
    } catch (error) {
        console.error('Error fetching friends list:', error);
        throw error;
    }
};

export const sendFriendRequest = async (recipientId) => {
    const userId = localStorage.getItem('userId');
    if (!userId) {
        console.error('User ID is not available');
        throw new Error('User ID is not available');
    }

    try {
        const response = await axios.post(`${API_URL}/friends/request`, {
            senderId: userId,
            recipientId,
        });
        return response.data; 
    } catch (error) {
        console.error('Error sending friend request:', error);
        throw error;
    }
};

export const acceptFriendRequest = async (requestId) => {
    try {
        const response = await axios.post(`${API_URL}/friends/accept`, { requestId });
        return response.data; 
    } catch (error) {
        console.error('Error accepting friend request:', error);
        throw error;
    }
};

export const rejectFriendRequest = async (requestId) => {
    try {
        const response = await axios.post(`${API_URL}/friends/reject`, { requestId });
        return response.data; 
    } catch (error) {
        console.error('Error rejecting friend request:', error);
        throw error;
    }
};

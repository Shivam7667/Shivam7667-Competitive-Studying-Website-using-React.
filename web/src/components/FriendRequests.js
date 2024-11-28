import React, { useState, useEffect } from 'react';
import { getPendingRequests, acceptFriendRequest, rejectFriendRequest } from './friendService';

function FriendRequests() {
    const [pendingRequests, setPendingRequests] = useState([]);

    useEffect(() => {
        fetchFriendRequests();
    }, []);

    const fetchFriendRequests = async () => {
        try {
            const response = await getPendingRequests();
            setPendingRequests(response);
        } catch (error) {
            console.error('Error fetching friend requests:', error);
            alert(error.message);  // Alert the user if the user ID is missing
        }
    };

    const handleAccept = async (requestId) => {
        try {
            await acceptFriendRequest(requestId);
            fetchFriendRequests();  
        } catch (error) {
            console.error('Error accepting friend request:', error);
        }
    };

    const handleReject = async (requestId) => {
        try {
            await rejectFriendRequest(requestId);
            fetchFriendRequests();  
        } catch (error) {
            console.error('Error rejecting friend request:', error);
        }
    };

    return (
        <div>
            <h2>Pending Friend Requests</h2>
            {pendingRequests.length > 0 ? (
                pendingRequests.map((request) => (
                    <div key={request._id}>
                        {request.sender.name} sent you a friend request.
                        <button onClick={() => handleAccept(request._id)}>Accept</button>
                        <button onClick={() => handleReject(request._id)}>Reject</button>
                    </div>
                ))
            ) : (
                <p>No pending requests</p>
            )}
        </div>
    );
}

export default FriendRequests;

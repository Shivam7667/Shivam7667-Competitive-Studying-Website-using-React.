import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';  // Assuming you have a CSS file for styling

function Login() {
    const [username, setUsername] = useState(''); // Stores the username (or email)
    const [password, setPassword] = useState(''); // Stores the password
    const [loading, setLoading] = useState(false);  // Manages loading state
    const [error, setError] = useState('');  // Error state to display any errors

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);  // Set loading to true to show loading state
        setError('');  // Clear any previous errors

        try {
            const response = await axios.post('http://localhost:5000/api/signin', {
                email: username,  // Assuming username is the email
                password,
            });

            // Assuming the API response contains a token and user ID
            localStorage.setItem('token', response.data.access_token);
            localStorage.setItem('userId', response.data.user_id);  // Store user ID

            // Redirect to the main page upon successful login
            window.location.href = 'http://localhost:3000/dashboard';  // Adjust the URL accordingly
        } catch (error) {
            console.error('Login Error:', error.response ? error.response.data : error.message);
            
            if (error.response && error.response.status === 401) {
                setError('Invalid credentials. Please check your email and password.');
            } else {
                setError('An error occurred. Please try again later.');
            }
        } finally {
            setLoading(false);  // Reset loading state after request completion
        }
    };

    return (
        <form onSubmit={handleLogin} className="login-form">
            <h2>Login</h2>
            <h3>Competitive Studying</h3>

            <input 
                type="text" 
                placeholder="Email" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
                required 
                disabled={loading}  
            />

            <input 
                type="password" 
                placeholder="Password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                required 
                disabled={loading}  
            />

            {error && <p className="error-message">{error}</p>}

            <button type="submit" disabled={loading}>
                {loading ? 'Logging in...' : 'Login'}  
            </button>

            {loading && <div className="spinner"></div>} 
        </form>
    );
}

export default Login;

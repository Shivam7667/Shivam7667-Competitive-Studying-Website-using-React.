// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

// Import your components/pages
import Register from './components/Register';
import Login from './components/Login';
import Dashboard from './pages/Dashboard';
import Friends from './pages/AdminPage'; // Assuming Friends component is for AdminPage
import Timer from './pages/FriendsPage'; // Assuming Timer component is for FriendsPage
import Admin from './pages/TimerPage'; // Assuming Admin component is for TimerPage
import StudySessionsPage from './pages/StudySessionsPage'; // Study sessions page
import StudyTimer from './components/StudyTimer'; // Study timer component

import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        {/* Authentication Routes */}
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        {/* Dashboard and Admin Routes */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/friends" element={<Friends />} />
        <Route path="/timer" element={<Timer />} />
        <Route path="/admin" element={<Admin />} />

        {/* Study Sessions and Timer Routes */}
        <Route path="/study/sessions" element={<StudySessionsPage />} />
        <Route path="/study/timer" element={<StudyTimer />} />
      </Routes>
    </Router>
  );
}

export default App;

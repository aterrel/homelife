import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Navbar from './components/Navbar';
import MyCalendar from './components/Calendar';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');

  useEffect(() => {
    // Check if user is logged in on component mount
    const token = localStorage.getItem('access_token');
    const storedUsername = localStorage.getItem('username');
    if (token && storedUsername) {
      setIsLoggedIn(true);
      setUsername(storedUsername);
    }
  }, []);

  const handleLogin = (userData) => {
    setIsLoggedIn(true);
    setUsername(userData.username);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUsername('');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
  };

  return (
    <div className="App">
      <Navbar 
        isLoggedIn={isLoggedIn} 
        username={username} 
        onLogin={handleLogin}
        onLogout={handleLogout}
      />
      <main className="container">
        <MyCalendar 
          isLoggedIn={isLoggedIn}
          onLogin={handleLogin}
        />
      </main>
    </div>
  );
}

export default App;
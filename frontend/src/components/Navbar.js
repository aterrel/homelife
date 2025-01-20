import React, { useState, useEffect } from 'react';
import LoginModal from './LoginModal';
import { Navbar as BootstrapNavbar, Nav, Container, Button } from 'react-bootstrap';

const Navbar = () => {
  const [showLoginModal, setShowLoginModal] = useState(false);
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
    localStorage.setItem('username', userData.username);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUsername('');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
  };

  return (
    <>
      <BootstrapNavbar bg="light" expand="lg" className="mb-3">
        <Container>
          <BootstrapNavbar.Brand href="/">HomeLife</BootstrapNavbar.Brand>
          <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
          <BootstrapNavbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="/events">Events</Nav.Link>
              <Nav.Link href="/recipes">Recipes</Nav.Link>
            </Nav>
            <Nav>
              {isLoggedIn ? (
                <div className="d-flex align-items-center">
                  <span className="me-3">Welcome, {username}!</span>
                  <Button 
                    variant="outline-danger" 
                    onClick={handleLogout}
                  >
                    Logout
                  </Button>
                </div>
              ) : (
                <Button 
                  variant="primary" 
                  onClick={() => setShowLoginModal(true)}
                >
                  Login
                </Button>
              )}
            </Nav>
          </BootstrapNavbar.Collapse>
        </Container>
      </BootstrapNavbar>

      <LoginModal
        show={showLoginModal}
        onHide={() => setShowLoginModal(false)}
        onLogin={handleLogin}
      />
    </>
  );
};

export default Navbar;

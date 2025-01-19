import React, { useState } from 'react';
import LoginModal from './LoginModal';
import { Navbar as BootstrapNavbar, Nav, Container, Button } from 'react-bootstrap';

const Navbar = () => {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');

  const handleLogin = (userData) => {
    setIsLoggedIn(true);
    setUsername(userData.username);
    setShowLoginModal(false);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUsername('');
    localStorage.removeItem('token');
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

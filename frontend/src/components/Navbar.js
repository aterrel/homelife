import React, { useState } from 'react';
import { Navbar as BootstrapNavbar, Nav, Container, Button } from 'react-bootstrap';
import LoginModal from './LoginModal';

const Navbar = ({ isLoggedIn, username, onLogin, onLogout }) => {
  const [showLoginModal, setShowLoginModal] = useState(false);

  const handleLogin = (userData) => {
    onLogin(userData);
    setShowLoginModal(false);
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
                    onClick={onLogout}
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

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
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
          <BootstrapNavbar.Brand as={Link} to="/">HomeLife</BootstrapNavbar.Brand>
          <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
          <BootstrapNavbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/events">Calendar</Nav.Link>
              <Nav.Link as={Link} to="/recipes">Recipes</Nav.Link>
              <Nav.Link as={Link} to="/meals">Meals</Nav.Link>
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

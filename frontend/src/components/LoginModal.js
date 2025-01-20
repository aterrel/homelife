import React, { useState } from 'react';
import { Modal, Form, Button, Alert } from 'react-bootstrap';

const LoginModal = ({ show, onHide, onLogin }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    password2: '',
    email: '',
    firstName: '',
    lastName: ''
  });
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const endpoint = isRegistering ? '/api/register/' : '/api/token/';
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(isRegistering ? {
          username: formData.username,
          password: formData.password,
          password2: formData.password2,
          email: formData.email,
          first_name: formData.firstName,
          last_name: formData.lastName
        } : {
          username: formData.username,
          password: formData.password
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || Object.values(data)[0]?.[0] || 'An error occurred');
      }

      if (!isRegistering) {
        // Store both tokens
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
      } else {
        // After successful registration, automatically log in
        const loginResponse = await fetch('/api/token/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: formData.username,
            password: formData.password,
          }),
        });

        const loginData = await loginResponse.json();
        if (!loginResponse.ok) {
          throw new Error('Registration successful but login failed');
        }

        localStorage.setItem('access_token', loginData.access);
        localStorage.setItem('refresh_token', loginData.refresh);
      }
      
      onLogin({ username: formData.username });
      onHide();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>{isRegistering ? 'Register' : 'Login'}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {error && (
          <Alert variant="danger" className="mb-3">
            {error}
          </Alert>
        )}
        
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Username</Form.Label>
            <Form.Control
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              required
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
            />
          </Form.Group>

          {isRegistering && (
            <>
              <Form.Group className="mb-3">
                <Form.Label>Confirm Password</Form.Label>
                <Form.Control
                  type="password"
                  name="password2"
                  value={formData.password2}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Email</Form.Label>
                <Form.Control
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>First Name</Form.Label>
                <Form.Control
                  type="text"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Last Name</Form.Label>
                <Form.Control
                  type="text"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>
            </>
          )}

          <div className="d-grid gap-2">
            <Button variant="primary" type="submit">
              {isRegistering ? 'Register' : 'Login'}
            </Button>
          </div>
        </Form>
      </Modal.Body>
      <Modal.Footer className="justify-content-center">
        <Button
          variant="link"
          onClick={() => {
            setIsRegistering(!isRegistering);
            setError('');
            setFormData({
              username: '',
              password: '',
              password2: '',
              email: '',
              firstName: '',
              lastName: ''
            });
          }}
        >
          {isRegistering ? 'Already have an account? Login' : "Don't have an account? Register"}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default LoginModal;

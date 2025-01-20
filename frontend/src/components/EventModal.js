import React, { useState, useEffect } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import axios from 'axios';

const EventModal = ({ show, handleClose, event, onEventAdded }) => {
    const [title, setTitle] = useState('');
    const [date, setDate] = useState('');
    const [time, setTime] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        if (event) {
            setTitle(event.title || '');
            setDate(event.date || '');
            setTime(event.time || '');
        } else {
            // Clear form when creating new event
            setTitle('');
            setDate('');
            setTime('');
        }
    }, [event]);

    const getAuthHeaders = () => {
        const token = localStorage.getItem('access_token');
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        const updatedEvent = { title, date, time };

        try {
            if (!localStorage.getItem('access_token')) {
                throw new Error('Please log in to create or edit events');
            }

            if (event?.id) {
                // Update existing event
                const response = await axios.put(`/api/events/${event.id}/`, updatedEvent, {
                    headers: getAuthHeaders(),
                });
                if (response.data) {
                    alert('Event updated successfully');
                }
            } else {
                const response = await axios.post('/api/events/', updatedEvent, {
                    headers: getAuthHeaders(),
                });
                if (response.data) {
                    alert('Event added successfully');
                }
            }
            onEventAdded && onEventAdded();
            handleClose();
        } catch (error) {
            console.error('Error saving event:', error);
            if (error.response?.data) {
                setError(Object.values(error.response.data)[0]?.[0] || 'Failed to save event');
            } else {
                setError(error.message || 'Failed to save event. Please check your input.');
            }
        }
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{event ? 'Edit Event' : 'Create Event'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {error && (
                    <div className="alert alert-danger" role="alert">
                        {error}
                    </div>
                )}
                <Form onSubmit={handleSubmit}>
                    <Form.Group className="mb-3">
                        <Form.Label>Title</Form.Label>
                        <Form.Control
                            type="text"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Date</Form.Label>
                        <Form.Control
                            type="date"
                            value={date}
                            onChange={(e) => setDate(e.target.value)}
                            required
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Time</Form.Label>
                        <Form.Control
                            type="time"
                            value={time}
                            onChange={(e) => setTime(e.target.value)}
                            required
                        />
                    </Form.Group>
                    <div className="d-flex justify-content-end">
                        <Button variant="secondary" onClick={handleClose} className="me-2">
                            Cancel
                        </Button>
                        <Button variant="primary" type="submit">
                            {event ? 'Update Event' : 'Create Event'}
                        </Button>
                    </div>
                </Form>
            </Modal.Body>
        </Modal>
    );
};

export default EventModal;
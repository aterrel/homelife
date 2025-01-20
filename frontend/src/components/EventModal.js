import React, { useState, useEffect } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import { eventApi } from '../services/api';

const EventModal = ({ show, onHide, event, onEventAdded }) => {
    const [formData, setFormData] = useState({
        title: '',
        date: '',
        time: ''
    });

    useEffect(() => {
        if (event) {
            setFormData({
                title: event.title,
                date: event.date,
                time: event.time || ''
            });
        } else {
            setFormData({
                title: '',
                date: '',
                time: ''
            });
        }
    }, [event]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (event) {
                await eventApi.update(event.id, formData);
            } else {
                await eventApi.create(formData);
            }
            onEventAdded();
            onHide();
        } catch (error) {
            console.error('Error saving event:', error);
        }
    };

    const handleDelete = async () => {
        if (!event) return;
        
        if (window.confirm('Are you sure you want to delete this event?')) {
            try {
                await eventApi.delete(event.id);
                onEventAdded();
                onHide();
            } catch (error) {
                console.error('Error deleting event:', error);
            }
        }
    };

    return (
        <Modal show={show} onHide={onHide}>
            <Form onSubmit={handleSubmit}>
                <Modal.Header closeButton>
                    <Modal.Title>
                        {event ? 'Edit Event' : 'Add New Event'}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form.Group className="mb-3">
                        <Form.Label>Event Title</Form.Label>
                        <Form.Control
                            type="text"
                            name="title"
                            value={formData.title}
                            onChange={handleInputChange}
                            required
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Date</Form.Label>
                        <Form.Control
                            type="date"
                            name="date"
                            value={formData.date}
                            onChange={handleInputChange}
                            required
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Time (optional)</Form.Label>
                        <Form.Control
                            type="time"
                            name="time"
                            value={formData.time}
                            onChange={handleInputChange}
                        />
                    </Form.Group>
                </Modal.Body>
                <Modal.Footer>
                    {event && (
                        <Button 
                            variant="danger" 
                            className="me-auto"
                            onClick={handleDelete}
                        >
                            Delete
                        </Button>
                    )}
                    <Button variant="secondary" onClick={onHide}>
                        Cancel
                    </Button>
                    <Button variant="primary" type="submit">
                        {event ? 'Save Changes' : 'Add Event'}
                    </Button>
                </Modal.Footer>
            </Form>
        </Modal>
    );
};

export default EventModal;
import React, { useState, useEffect } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import axios from 'axios';

const EventModal = ({ show, handleClose, event, onEventUpdated }) => {
    const [title, setTitle] = useState('');
    const [date, setDate] = useState('');
    const [time, setTime] = useState('');

    useEffect(() => {
        if (event) {
            setTitle(event.title || '');
            setDate(event.date || '');
            setTime(event.time || '');
        }
    }, [event]);


    const handleSubmit = async (e) => {
        e.preventDefault();

        const updatedEvent = { title, date, time };

        try {
            if (event?.id) {
                // Update existing event
                await axios.put(`/api/events/${event.id}/`, updatedEvent, {
                    headers: { 'Content-Type': 'application/json' },
                });
                alert('Event updated successfully');
            } else {
                const response = await axios.post('/api/events/', updatedEvent, {
                    headers: { 'Content-Type': 'application/json' },
                });
                alert('Event added successfully');
            }
            onEventUpdated();
            handleClose();
        } catch (error) {
            console.error('Error saving event:', error.response.data);
            alert('Failed to save event. Please check your input.');
        }
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{event ? 'Edit Event' : 'Create Event'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={handleSubmit}>
                    <Form.Group className="mb-3">
                        <Form.Label>Title</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter event title"
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
                    <Button variant="primary" type="submit">
                        Save Event
                    </Button>
                </Form>
            </Modal.Body>
        </Modal>
    )
};

export default EventModal;
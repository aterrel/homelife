import React, { useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import { mealPlanApi } from '../services/api';

const MealPlanModal = ({ show, onHide, onMealPlanAdded }) => {
    const [name, setName] = useState('Weekly Meal Plan');
    const [startDate, setStartDate] = useState('');
    const [notes, setNotes] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await mealPlanApi.create({
                name,
                start_date: startDate,
                notes
            });
            onMealPlanAdded();
            onHide();
        } catch (error) {
            console.error('Error creating meal plan:', error);
        }
    };

    return (
        <Modal show={show} onHide={onHide}>
            <Modal.Header closeButton>
                <Modal.Title>Create New Meal Plan</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={handleSubmit}>
                    <Form.Group className="mb-3">
                        <Form.Label>Name</Form.Label>
                        <Form.Control
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Start Date</Form.Label>
                        <Form.Control
                            type="date"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                            required
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Notes</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={3}
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                        />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={onHide}>
                    Cancel
                </Button>
                <Button variant="primary" onClick={handleSubmit}>
                    Create Meal Plan
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default MealPlanModal;

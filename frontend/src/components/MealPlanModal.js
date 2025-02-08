import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Row, Col, ListGroup, Badge } from 'react-bootstrap';
import { mealPlanApi, recipeApi } from '../services/api';

const MealPlanModal = ({ show, onHide, onMealPlanAdded }) => {
    const [name, setName] = useState('Weekly Meal Plan');
    const [startDate, setStartDate] = useState('');
    const [notes, setNotes] = useState('');
    const [slots, setSlots] = useState([]);
    const [recipes, setRecipes] = useState([]);
    const [loading, setLoading] = useState(true);

    // Form state for new slot
    const [newSlot, setNewSlot] = useState({
        recipe: '',
        date: '',
        meal_type: 'breakfast',
        servings: 1,
        notes: ''
    });

    useEffect(() => {
        const fetchRecipes = async () => {
            try {
                const response = await recipeApi.getAll();
                setRecipes(response.data);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching recipes:', error);
                setLoading(false);
            }
        };
        if (show) {
            fetchRecipes();
        }
    }, [show]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await mealPlanApi.create({
                name,
                start_date: startDate,
                notes
            });
            
            if (slots.length > 0) {
                // Format slots data for the API
                const formattedSlots = slots.map(slot => ({
                    recipe: slot.recipe.id,
                    date: slot.date,
                    meal_type: slot.meal_type,
                    servings: slot.servings,
                    notes: slot.notes
                }));
                
                await mealPlanApi.createSlots(response.data.id, formattedSlots);
            }
            
            onMealPlanAdded();
            onHide();
            // Reset form
            setName('Weekly Meal Plan');
            setStartDate('');
            setNotes('');
            setSlots([]);
            setNewSlot({
                recipe: '',
                date: '',
                meal_type: 'breakfast',
                servings: 1,
                notes: ''
            });
        } catch (error) {
            console.error('Error creating meal plan:', error);
        }
    };

    const handleAddSlot = (e) => {
        e.preventDefault();
        const recipe = recipes.find(r => r.id === parseInt(newSlot.recipe));
        setSlots([...slots, { ...newSlot, recipe }]);
        setNewSlot({
            recipe: '',
            date: '',
            meal_type: 'breakfast',
            servings: 1,
            notes: ''
        });
    };

    const handleRemoveSlot = (index) => {
        setSlots(slots.filter((_, i) => i !== index));
    };

    return (
        <Modal show={show} onHide={onHide} size="lg">
            <Modal.Header closeButton>
                <Modal.Title>Create New Meal Plan</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={handleSubmit}>
                    <Row>
                        <Col md={6}>
                            <Form.Group className="mb-3">
                                <Form.Label>Name</Form.Label>
                                <Form.Control
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    required
                                />
                            </Form.Group>
                        </Col>
                        <Col md={6}>
                            <Form.Group className="mb-3">
                                <Form.Label>Start Date</Form.Label>
                                <Form.Control
                                    type="date"
                                    value={startDate}
                                    onChange={(e) => setStartDate(e.target.value)}
                                    required
                                />
                            </Form.Group>
                        </Col>
                    </Row>
                    <Form.Group className="mb-3">
                        <Form.Label>Notes</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={2}
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                        />
                    </Form.Group>
                    <hr />
                    <h5>Add Meals</h5>
                    <Row className="mb-3">
                        <Col md={6}>
                            <Form.Group className="mb-3">
                                <Form.Label>Recipe</Form.Label>
                                <Form.Select
                                    value={newSlot.recipe}
                                    onChange={(e) => setNewSlot({ ...newSlot, recipe: e.target.value })}
                                    disabled={loading}
                                >
                                    <option value="">Select a recipe...</option>
                                    {recipes.map(recipe => (
                                        <option key={recipe.id} value={recipe.id}>
                                            {recipe.name}
                                        </option>
                                    ))}
                                </Form.Select>
                            </Form.Group>
                        </Col>
                        <Col md={6}>
                            <Form.Group className="mb-3">
                                <Form.Label>Date</Form.Label>
                                <Form.Control
                                    type="date"
                                    value={newSlot.date}
                                    onChange={(e) => setNewSlot({ ...newSlot, date: e.target.value })}
                                />
                            </Form.Group>
                        </Col>
                    </Row>
                    <Row className="mb-3">
                        <Col md={6}>
                            <Form.Group className="mb-3">
                                <Form.Label>Meal Type</Form.Label>
                                <Form.Select
                                    value={newSlot.meal_type}
                                    onChange={(e) => setNewSlot({ ...newSlot, meal_type: e.target.value })}
                                >
                                    <option value="breakfast">Breakfast</option>
                                    <option value="lunch">Lunch</option>
                                    <option value="dinner">Dinner</option>
                                    <option value="snack">Snack</option>
                                </Form.Select>
                            </Form.Group>
                        </Col>
                        <Col md={6}>
                            <Form.Group className="mb-3">
                                <Form.Label>Servings</Form.Label>
                                <Form.Control
                                    type="number"
                                    min="1"
                                    value={newSlot.servings}
                                    onChange={(e) => setNewSlot({ ...newSlot, servings: parseInt(e.target.value) })}
                                />
                            </Form.Group>
                        </Col>
                    </Row>
                    <Row className="mb-3">
                        <Col>
                            <Form.Group className="mb-3">
                                <Form.Label>Notes</Form.Label>
                                <Form.Control
                                    as="textarea"
                                    rows={2}
                                    value={newSlot.notes}
                                    onChange={(e) => setNewSlot({ ...newSlot, notes: e.target.value })}
                                />
                            </Form.Group>
                        </Col>
                    </Row>
                    <div className="d-grid">
                        <Button
                            variant="secondary"
                            onClick={handleAddSlot}
                            disabled={!newSlot.recipe || !newSlot.date}
                        >
                            Add Meal
                        </Button>
                    </div>
                    {slots.length > 0 && (
                        <div className="mt-3">
                            <h6>Added Meals:</h6>
                            <ListGroup>
                                {slots.map((slot, index) => (
                                    <ListGroup.Item
                                        key={index}
                                        className="d-flex justify-content-between align-items-center"
                                    >
                                        <div>
                                            <Badge bg="info" className="me-2">
                                                {slot.meal_type.charAt(0).toUpperCase() + slot.meal_type.slice(1)}
                                            </Badge>
                                            {slot.recipe.name}
                                            <small className="text-muted ms-2">
                                                ({slot.date})
                                            </small>
                                        </div>
                                        <Button
                                            variant="outline-danger"
                                            size="sm"
                                            onClick={() => handleRemoveSlot(index)}
                                        >
                                            Remove
                                        </Button>
                                    </ListGroup.Item>
                                ))}
                            </ListGroup>
                        </div>
                    )}
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

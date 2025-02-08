import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Row, Col } from 'react-bootstrap';
import { recipeApi } from '../services/api';

const MealSlotModal = ({ show, onHide, mealSlot, onSave, onDelete }) => {
    const [recipes, setRecipes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({
        recipe: '',
        date: '',
        meal_type: 'breakfast',
        servings: 1,
        notes: '',
        meal_plan: null
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

    useEffect(() => {
        if (mealSlot) {
            setFormData({
                recipe: mealSlot.recipe.id,
                date: mealSlot.date,
                meal_type: mealSlot.meal_type,
                servings: mealSlot.servings,
                notes: mealSlot.notes || '',
                meal_plan: mealSlot.meal_plan
            });
        }
    }, [mealSlot]);

    const handleSubmit = (e) => {
        e.preventDefault();
        const recipe = recipes.find(r => r.id === parseInt(formData.recipe));
        onSave({ 
            ...formData,
            recipe: formData.recipe // Send just the ID
        });
    };

    const handleDelete = () => {
        if (window.confirm('Are you sure you want to delete this meal slot?')) {
            onDelete();
        }
    };

    return (
        <Modal show={show} onHide={onHide}>
            <Modal.Header closeButton>
                <Modal.Title>{mealSlot ? 'Edit Meal' : 'Add Meal'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={handleSubmit}>
                    <Row>
                        <Col md={12}>
                            <Form.Group className="mb-3">
                                <Form.Label>Recipe</Form.Label>
                                <Form.Select
                                    value={formData.recipe}
                                    onChange={(e) => setFormData({ ...formData, recipe: e.target.value })}
                                    disabled={loading}
                                    required
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
                    </Row>
                    <Row>
                        <Col md={6}>
                            <Form.Group className="mb-3">
                                <Form.Label>Date</Form.Label>
                                <Form.Control
                                    type="date"
                                    value={formData.date}
                                    onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                                    required
                                />
                            </Form.Group>
                        </Col>
                        <Col md={6}>
                            <Form.Group className="mb-3">
                                <Form.Label>Meal Type</Form.Label>
                                <Form.Select
                                    value={formData.meal_type}
                                    onChange={(e) => setFormData({ ...formData, meal_type: e.target.value })}
                                    required
                                >
                                    <option value="breakfast">Breakfast</option>
                                    <option value="lunch">Lunch</option>
                                    <option value="dinner">Dinner</option>
                                    <option value="snack">Snack</option>
                                </Form.Select>
                            </Form.Group>
                        </Col>
                    </Row>
                    <Row>
                        <Col md={12}>
                            <Form.Group className="mb-3">
                                <Form.Label>Servings</Form.Label>
                                <Form.Control
                                    type="number"
                                    min="1"
                                    value={formData.servings}
                                    onChange={(e) => setFormData({ ...formData, servings: parseInt(e.target.value) })}
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
                            value={formData.notes}
                            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                        />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                {mealSlot && (
                    <Button 
                        variant="danger" 
                        onClick={handleDelete}
                        className="me-auto"
                    >
                        Delete
                    </Button>
                )}
                <Button variant="secondary" onClick={onHide}>
                    Cancel
                </Button>
                <Button variant="primary" onClick={handleSubmit}>
                    {mealSlot ? 'Save Changes' : 'Add Meal'}
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default MealSlotModal;

import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Row, Col, ListGroup } from 'react-bootstrap';
import { recipeApi } from '../services/api';

const RecipeEditModal = ({ show, handleClose, recipe, onSave }) => {
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        instructions: '',
        prep_time: '',
        cook_time: '',
        servings: '',
        difficulty: 'medium',
        ingredients: []
    });

    const [newIngredient, setNewIngredient] = useState({
        name: '',
        quantity: '',
        unit: '',
        notes: ''
    });

    // Transform backend ingredient data to form format
    const transformIngredientsFromBackend = (recipeData) => {
        if (!recipeData?.ingredients) return [];
        return recipeData.ingredients.map(ing => ({
            name: ing.ingredient.name,
            quantity: ing.quantity,
            unit: ing.unit,
            notes: ing.notes || '',
            // Store the original ingredient ID if it exists
            ingredient_id: ing.ingredient.id
        }));
    };

    // Transform form ingredient data to backend format
    const transformIngredientsForBackend = (ingredients) => {
        return ingredients.map(ing => ({
            ingredient: {
                name: ing.name,
                id: ing.ingredient_id
            },
            quantity: ing.quantity,
            unit: ing.unit,
            notes: ing.notes || ''
        }));
    };

    useEffect(() => {
        if (recipe) {
            setFormData({
                name: recipe.name || '',
                description: recipe.description || '',
                instructions: recipe.instructions || '',
                prep_time: recipe.prep_time || '',
                cook_time: recipe.cook_time || '',
                servings: recipe.servings || '',
                difficulty: recipe.difficulty || 'medium',
                ingredients: transformIngredientsFromBackend(recipe)
            });
        } else {
            // Reset form when adding new recipe
            setFormData({
                name: '',
                description: '',
                instructions: '',
                prep_time: '',
                cook_time: '',
                servings: '',
                difficulty: 'medium',
                ingredients: []
            });
        }
    }, [recipe]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleIngredientChange = (e) => {
        const { name, value } = e.target;
        setNewIngredient(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const addIngredient = () => {
        if (newIngredient.name && newIngredient.quantity && newIngredient.unit) {
            setFormData(prev => ({
                ...prev,
                ingredients: [...prev.ingredients, { ...newIngredient }]
            }));
            setNewIngredient({
                name: '',
                quantity: '',
                unit: '',
                notes: ''
            });
        }
    };

    const removeIngredient = (index) => {
        setFormData(prev => ({
            ...prev,
            ingredients: prev.ingredients.filter((_, i) => i !== index)
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Prepare the data for submission
            const submissionData = {
                ...formData,
                ingredients: transformIngredientsForBackend(formData.ingredients)
            };

            console.log('Submitting recipe data:', submissionData);

            let savedRecipe;
            if (recipe) {
                savedRecipe = await recipeApi.update(recipe.id, submissionData);
            } else {
                savedRecipe = await recipeApi.create(submissionData);
            }
            onSave(savedRecipe);
            handleClose();
        } catch (error) {
            console.error('Error saving recipe:', error);
            // TODO: Add error handling UI
        }
    };

    return (
        <Modal show={show} onHide={handleClose} size="lg">
            <Form onSubmit={handleSubmit}>
                <Modal.Header closeButton>
                    <Modal.Title>
                        {recipe ? 'Edit Recipe' : 'Add New Recipe'}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form.Group className="mb-3">
                        <Form.Label>Recipe Name</Form.Label>
                        <Form.Control
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleInputChange}
                            required
                        />
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                            as="textarea"
                            name="description"
                            value={formData.description}
                            onChange={handleInputChange}
                            rows={2}
                        />
                    </Form.Group>

                    <Row className="mb-3">
                        <Col md={4}>
                            <Form.Group>
                                <Form.Label>Prep Time (minutes)</Form.Label>
                                <Form.Control
                                    type="number"
                                    name="prep_time"
                                    value={formData.prep_time}
                                    onChange={handleInputChange}
                                    required
                                />
                            </Form.Group>
                        </Col>
                        <Col md={4}>
                            <Form.Group>
                                <Form.Label>Cook Time (minutes)</Form.Label>
                                <Form.Control
                                    type="number"
                                    name="cook_time"
                                    value={formData.cook_time}
                                    onChange={handleInputChange}
                                    required
                                />
                            </Form.Group>
                        </Col>
                        <Col md={4}>
                            <Form.Group>
                                <Form.Label>Servings</Form.Label>
                                <Form.Control
                                    type="number"
                                    name="servings"
                                    value={formData.servings}
                                    onChange={handleInputChange}
                                    required
                                />
                            </Form.Group>
                        </Col>
                    </Row>

                    <Form.Group className="mb-3">
                        <Form.Label>Difficulty</Form.Label>
                        <Form.Select
                            name="difficulty"
                            value={formData.difficulty}
                            onChange={handleInputChange}
                        >
                            <option value="easy">Easy</option>
                            <option value="medium">Medium</option>
                            <option value="hard">Hard</option>
                        </Form.Select>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Instructions</Form.Label>
                        <Form.Control
                            as="textarea"
                            name="instructions"
                            value={formData.instructions}
                            onChange={handleInputChange}
                            rows={4}
                            required
                        />
                    </Form.Group>

                    <div className="mb-3">
                        <h5>Ingredients</h5>
                        <ListGroup className="mb-3">
                            {formData.ingredients.map((ingredient, index) => (
                                <ListGroup.Item key={index} className="d-flex justify-content-between align-items-center">
                                    <span>
                                        {ingredient.quantity} {ingredient.unit} {ingredient.name}
                                        {ingredient.notes && ` (${ingredient.notes})`}
                                    </span>
                                    <Button
                                        variant="outline-danger"
                                        size="sm"
                                        onClick={() => removeIngredient(index)}
                                    >
                                        Remove
                                    </Button>
                                </ListGroup.Item>
                            ))}
                        </ListGroup>

                        <Row className="g-2">
                            <Col md={3}>
                                <Form.Control
                                    type="text"
                                    placeholder="Ingredient name"
                                    name="name"
                                    value={newIngredient.name}
                                    onChange={handleIngredientChange}
                                />
                            </Col>
                            <Col md={2}>
                                <Form.Control
                                    type="number"
                                    step="0.01"
                                    placeholder="Quantity"
                                    name="quantity"
                                    value={newIngredient.quantity}
                                    onChange={handleIngredientChange}
                                />
                            </Col>
                            <Col md={2}>
                                <Form.Control
                                    type="text"
                                    placeholder="Unit"
                                    name="unit"
                                    value={newIngredient.unit}
                                    onChange={handleIngredientChange}
                                />
                            </Col>
                            <Col md={3}>
                                <Form.Control
                                    type="text"
                                    placeholder="Notes (optional)"
                                    name="notes"
                                    value={newIngredient.notes}
                                    onChange={handleIngredientChange}
                                />
                            </Col>
                            <Col md={2}>
                                <Button
                                    variant="outline-primary"
                                    onClick={addIngredient}
                                    className="w-100"
                                >
                                    Add
                                </Button>
                            </Col>
                        </Row>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Cancel
                    </Button>
                    <Button variant="primary" type="submit">
                        {recipe ? 'Save Changes' : 'Create Recipe'}
                    </Button>
                </Modal.Footer>
            </Form>
        </Modal>
    );
};

export default RecipeEditModal;
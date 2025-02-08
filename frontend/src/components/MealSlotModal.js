import React, { useState, useEffect } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import { recipeApi, mealPlanApi } from '../services/api';

const MealSlotModal = ({ show, onHide, mealPlan, onMealSlotAdded }) => {
    const [recipes, setRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState('');
    const [date, setDate] = useState('');
    const [mealType, setMealType] = useState('breakfast');
    const [servings, setServings] = useState(1);
    const [notes, setNotes] = useState('');
    const [loading, setLoading] = useState(true);

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
        fetchRecipes();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await mealPlanApi.createSlots(mealPlan.id, [{
                recipe: selectedRecipe,
                date,
                meal_type: mealType,
                servings,
                notes
            }]);
            onMealSlotAdded();
            onHide();
        } catch (error) {
            console.error('Error creating meal slot:', error);
        }
    };

    return (
        <Modal show={show} onHide={onHide}>
            <Modal.Header closeButton>
                <Modal.Title>Add Recipe to Meal Plan</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={handleSubmit}>
                    <Form.Group className="mb-3">
                        <Form.Label>Recipe</Form.Label>
                        <Form.Select
                            value={selectedRecipe}
                            onChange={(e) => setSelectedRecipe(e.target.value)}
                            required
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
                        <Form.Label>Meal Type</Form.Label>
                        <Form.Select
                            value={mealType}
                            onChange={(e) => setMealType(e.target.value)}
                            required
                        >
                            <option value="breakfast">Breakfast</option>
                            <option value="lunch">Lunch</option>
                            <option value="dinner">Dinner</option>
                            <option value="snack">Snack</option>
                        </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Servings</Form.Label>
                        <Form.Control
                            type="number"
                            min="1"
                            value={servings}
                            onChange={(e) => setServings(parseInt(e.target.value))}
                            required
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Notes</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={2}
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
                    Add Recipe
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default MealSlotModal;

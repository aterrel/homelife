import React from 'react';
import { Modal, Button, ListGroup } from 'react-bootstrap';
import '../styles/Recipe.css';

const RecipeModal = ({ show, handleClose, recipe, onEdit, onDelete }) => {
    if (!recipe) return null;

    // Format ingredient with quantity, unit, and notes
    const formatIngredient = (ingredient) => {
        const quantity = parseFloat(ingredient.quantity);
        const formattedQuantity = Number.isInteger(quantity) ? quantity.toString() : quantity.toFixed(2);
        let text = `${formattedQuantity} ${ingredient.unit} ${ingredient.ingredient.name}`;
        if (ingredient.notes) {
            text += ` (${ingredient.notes})`;
        }
        return text;
    };

    return (
        <Modal show={show} onHide={handleClose} size="lg">
            <Modal.Header closeButton>
                <Modal.Title>{recipe.name}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div className="recipe-details mb-4">
                    {recipe.description && (
                        <p className="text-muted mb-3">{recipe.description}</p>
                    )}
                    <div className="d-flex justify-content-between mb-3">
                        <span>
                            <strong>Prep Time:</strong> {recipe.prep_time} minutes
                        </span>
                        <span>
                            <strong>Cook Time:</strong> {recipe.cook_time} minutes
                        </span>
                        <span>
                            <strong>Servings:</strong> {recipe.servings}
                        </span>
                    </div>
                </div>

                <h5 className="mb-3">Ingredients</h5>
                <ListGroup className="mb-4">
                    {recipe.ingredients?.map((ingredient, index) => (
                        <ListGroup.Item key={index}>
                            {formatIngredient(ingredient)}
                        </ListGroup.Item>
                    ))}
                </ListGroup>
                
                <h5 className="mb-3">Instructions</h5>
                <pre className="recipe-text mb-4 instructions">
                    {recipe.instructions}
                </pre>

                <small className="text-muted">
                    Last updated: {new Date(recipe.updated_at).toLocaleDateString()}
                </small>
            </Modal.Body>
            <Modal.Footer>
                <div className="d-flex justify-content-between w-100">
                    <div>
                        <Button
                            variant="outline-danger"
                            onClick={() => onDelete(recipe.id)}
                            className="me-2"
                        >
                            Delete Recipe
                        </Button>
                        <Button
                            variant="outline-primary"
                            onClick={() => onEdit(recipe)}
                        >
                            Edit Recipe
                        </Button>
                    </div>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                </div>
            </Modal.Footer>
        </Modal>
    );
};

export default RecipeModal;

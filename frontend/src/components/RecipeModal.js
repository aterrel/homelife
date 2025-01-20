import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const RecipeModal = ({ show, handleClose, recipe }) => {
    if (!recipe) return null;

    return (
        <Modal show={show} onHide={handleClose} size="lg">
            <Modal.Header closeButton>
                <Modal.Title>{recipe.name}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <h5 className="mb-3">Ingredients</h5>
                <pre className="recipe-text mb-4">
                    {recipe.ingredients}
                </pre>
                
                <h5 className="mb-3">Instructions</h5>
                <pre className="recipe-text mb-4">
                    {recipe.instructions}
                </pre>

                <small className="text-muted">
                    Last updated: {new Date(recipe.updated_at).toLocaleDateString()}
                </small>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default RecipeModal;

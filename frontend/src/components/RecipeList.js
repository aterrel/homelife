import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Button, InputGroup } from 'react-bootstrap';
import { recipeApi } from '../services/api';
import RecipeModal from './RecipeModal';
import RecipeEditModal from './RecipeEditModal';
import '../styles/Recipe.css';

const RecipeList = () => {
    const [recipes, setRecipes] = useState([]);
    const [filteredRecipes, setFilteredRecipes] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [showViewModal, setShowViewModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [editingRecipe, setEditingRecipe] = useState(null);

    useEffect(() => {
        fetchRecipes();
    }, []);

    useEffect(() => {
        const filtered = recipes.filter(recipe =>
            recipe.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            recipe.ingredients?.some(ri => 
                ri.ingredient.name.toLowerCase().includes(searchTerm.toLowerCase())
            ) ||
            recipe.instructions?.toLowerCase().includes(searchTerm.toLowerCase())
        );
        setFilteredRecipes(filtered);
    }, [searchTerm, recipes]);

    const fetchRecipes = async () => {
        try {
            setLoading(true);
            const response = await recipeApi.getAll();
            setRecipes(response.data);
            setError(null);
        } catch (err) {
            setError('Failed to fetch recipes. Please try again later.');
            console.error('Error fetching recipes:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleViewRecipe = (recipe) => {
        setSelectedRecipe(recipe);
        setShowViewModal(true);
    };

    const handleAddRecipe = () => {
        setEditingRecipe(null);
        setShowEditModal(true);
    };

    const handleEditRecipe = (recipe) => {
        setEditingRecipe(recipe);
        setShowEditModal(true);
    };

    const handleSaveRecipe = async (savedRecipe) => {
        await fetchRecipes(); // Refresh the recipe list
    };

    const handleDeleteRecipe = async (recipeId) => {
        if (window.confirm('Are you sure you want to delete this recipe?')) {
            try {
                await recipeApi.delete(recipeId);
                await fetchRecipes(); // Refresh the recipe list
            } catch (error) {
                console.error('Error deleting recipe:', error);
                // TODO: Add error handling UI
            }
        }
    };

    const truncateText = (text, lines = 3) => {
        if (!text) return '';
        const splitText = text.split('\n');
        if (splitText.length > lines) {
            return splitText.slice(0, lines).join('\n') + '\n...';
        }
        return text;
    };

    if (loading) {
        return <div>Loading recipes...</div>;
    }

    if (error) {
        return <div className="text-danger">{error}</div>;
    }

    return (
        <Container>
            <div className="d-flex justify-content-between align-items-center mb-4">
                <InputGroup>
                    <Form.Control
                        type="text"
                        placeholder="Search recipes..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-50"
                    />
                    {searchTerm && (
                        <Button 
                            variant="outline-secondary"
                            onClick={() => setSearchTerm('')}
                        >
                            Clear
                        </Button>
                    )}
                </InputGroup>
                <Button variant="primary" onClick={handleAddRecipe}>
                    Add New Recipe
                </Button>
            </div>

            <Row xs={1} md={2} lg={3} className="g-4">
                {filteredRecipes.map((recipe) => (
                    <Col key={recipe.id}>
                        <Card className="h-100">
                            <Card.Body>
                                <Card.Title>{recipe.name}</Card.Title>
                                {recipe.description && (
                                    <Card.Text className="text-muted small">
                                        {truncateText(recipe.description, 2)}
                                    </Card.Text>
                                )}
                                <div className="mt-2 small">
                                    <div><strong>Prep:</strong> {recipe.prep_time} min</div>
                                    <div><strong>Cook:</strong> {recipe.cook_time} min</div>
                                    <div><strong>Servings:</strong> {recipe.servings}</div>
                                </div>
                                <div className="d-flex justify-content-between">
                                    <Button
                                        variant="outline-primary"
                                        onClick={() => handleViewRecipe(recipe)}
                                    >
                                        View
                                    </Button>
                                    <div>
                                        <Button
                                            variant="outline-secondary"
                                            onClick={() => handleEditRecipe(recipe)}
                                            className="me-2"
                                        >
                                            Edit
                                        </Button>
                                        <Button
                                            variant="outline-danger"
                                            onClick={() => handleDeleteRecipe(recipe.id)}
                                        >
                                            Delete
                                        </Button>
                                    </div>
                                </div>
                            </Card.Body>
                            <Card.Footer className="text-muted">
                                <small>Click to view full recipe</small>
                            </Card.Footer>
                        </Card>
                    </Col>
                ))}
            </Row>

            <RecipeModal
                show={showViewModal}
                handleClose={() => setShowViewModal(false)}
                recipe={selectedRecipe}
            />

            <RecipeEditModal
                show={showEditModal}
                handleClose={() => setShowEditModal(false)}
                recipe={editingRecipe}
                onSave={handleSaveRecipe}
            />
        </Container>
    );
};

export default RecipeList;

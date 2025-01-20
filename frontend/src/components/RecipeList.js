import React, { useState, useEffect } from 'react';
import { Card, Form, InputGroup, Row, Col, Button } from 'react-bootstrap';
import RecipeModal from './RecipeModal';
import { recipeApi } from '../services/api';

const RecipeList = () => {
    const [recipes, setRecipes] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredRecipes, setFilteredRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchRecipes = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await recipeApi.getAll();
            setRecipes(response.data);
            setFilteredRecipes(response.data);
        } catch (error) {
            console.error('Error fetching recipes:', error);
            setError('Failed to load recipes. Please try again later.');
            setRecipes([]);
            setFilteredRecipes([]);
        } finally {
            setLoading(false);
        }
    };

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

    const truncateText = (text, lines = 3) => {
        if (!text) return '';
        const splitText = text.split('\n');
        if (splitText.length > lines) {
            return splitText.slice(0, lines).join('\n') + '\n...';
        }
        return text;
    };

    const handleRecipeClick = async (recipe) => {
        try {
            setLoading(true);
            const response = await recipeApi.get(recipe.id);
            setSelectedRecipe(response.data);
            setShowModal(true);
        } catch (error) {
            console.error('Error fetching recipe details:', error);
            setError('Failed to load recipe details. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setSelectedRecipe(null);
    };

    if (loading && recipes.length === 0) {
        return (
            <div className="container mt-4 text-center">
                <p>Loading recipes...</p>
            </div>
        );
    }

    if (error && recipes.length === 0) {
        return (
            <div className="container mt-4">
                <div className="alert alert-danger" role="alert">
                    {error}
                </div>
            </div>
        );
    }

    return (
        <div className="container mt-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2>Recipe Collection</h2>
            </div>

            <Form className="mb-4">
                <InputGroup>
                    <Form.Control
                        type="text"
                        placeholder="Search recipes..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
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
            </Form>

            {filteredRecipes.length === 0 ? (
                <div className="text-center mt-4">
                    <p>No recipes found. Try adjusting your search.</p>
                </div>
            ) : (
                <Row xs={1} md={2} lg={3} className="g-4">
                    {filteredRecipes.map((recipe) => (
                        <Col key={recipe.id}>
                            <Card 
                                className="h-100 recipe-card" 
                                onClick={() => handleRecipeClick(recipe)}
                                style={{ cursor: 'pointer' }}
                            >
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
                                </Card.Body>
                                <Card.Footer className="text-muted">
                                    <small>Click to view full recipe</small>
                                </Card.Footer>
                            </Card>
                        </Col>
                    ))}
                </Row>
            )}

            <RecipeModal
                show={showModal}
                handleClose={handleCloseModal}
                recipe={selectedRecipe}
            />
        </div>
    );
};

export default RecipeList;

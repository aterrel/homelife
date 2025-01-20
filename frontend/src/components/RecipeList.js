import React, { useState, useEffect } from 'react';
import { Card, Form, InputGroup, Row, Col, Button } from 'react-bootstrap';
import axios from 'axios';
import RecipeModal from './RecipeModal';

const RecipeList = ({ isLoggedIn }) => {
    const [recipes, setRecipes] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredRecipes, setFilteredRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [showModal, setShowModal] = useState(false);

    const fetchRecipes = async () => {
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.get('/api/recipes/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            setRecipes(response.data);
            setFilteredRecipes(response.data);
        } catch (error) {
            console.error('Error fetching recipes:', error);
            setRecipes([]);
            setFilteredRecipes([]);
        }
    };

    useEffect(() => {
        if (isLoggedIn) {
            fetchRecipes();
        } else {
            setRecipes([]);
            setFilteredRecipes([]);
        }
    }, [isLoggedIn]);

    useEffect(() => {
        const filtered = recipes.filter(recipe =>
            recipe.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            recipe.ingredients.toLowerCase().includes(searchTerm.toLowerCase()) ||
            recipe.instructions.toLowerCase().includes(searchTerm.toLowerCase())
        );
        setFilteredRecipes(filtered);
    }, [searchTerm, recipes]);

    const truncateText = (text, lines = 3) => {
        const splitText = text.split('\n');
        if (splitText.length > lines) {
            return splitText.slice(0, lines).join('\n') + '\n...';
        }
        return text;
    };

    const handleCardClick = (recipe) => {
        setSelectedRecipe(recipe);
        setShowModal(true);
    };

    if (!isLoggedIn) {
        return (
            <Card className="text-center">
                <Card.Body>
                    <Card.Title>Recipe Collection</Card.Title>
                    <Card.Text>
                        Please log in to view and manage your recipes.
                    </Card.Text>
                </Card.Body>
            </Card>
        );
    }

    return (
        <div>
            <h2 className="mb-4">Recipe Collection</h2>
            
            <InputGroup className="mb-4">
                <Form.Control
                    placeholder="Search recipes by name, ingredients, or instructions..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Button 
                    variant="outline-secondary"
                    onClick={() => setSearchTerm('')}
                >
                    Clear
                </Button>
            </InputGroup>

            <Row xs={1} md={2} lg={3} className="g-4">
                {filteredRecipes.map(recipe => (
                    <Col key={recipe.id}>
                        <Card 
                            className="h-100 recipe-card" 
                            onClick={() => handleCardClick(recipe)}
                            style={{ cursor: 'pointer' }}
                        >
                            <Card.Body>
                                <Card.Title>{recipe.name}</Card.Title>
                                <Card.Subtitle className="mb-2 text-muted">Ingredients</Card.Subtitle>
                                <Card.Text style={{ whiteSpace: 'pre-line' }}>
                                    {truncateText(recipe.ingredients)}
                                </Card.Text>
                                <Card.Subtitle className="mb-2 text-muted">Instructions</Card.Subtitle>
                                <Card.Text style={{ whiteSpace: 'pre-line' }}>
                                    {truncateText(recipe.instructions)}
                                </Card.Text>
                            </Card.Body>
                            <Card.Footer className="text-muted">
                                <small>Click to view full recipe</small>
                            </Card.Footer>
                        </Card>
                    </Col>
                ))}
            </Row>

            {filteredRecipes.length === 0 && (
                <Card className="text-center mt-4">
                    <Card.Body>
                        <Card.Text>
                            {searchTerm ? 'No recipes match your search.' : 'No recipes available.'}
                        </Card.Text>
                    </Card.Body>
                </Card>
            )}

            <RecipeModal
                show={showModal}
                handleClose={() => setShowModal(false)}
                recipe={selectedRecipe}
            />
        </div>
    );
};

export default RecipeList;

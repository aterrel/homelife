import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Card, Row, Col, Button, Form } from 'react-bootstrap';
import { getRecipes } from '../services/api';

const RecipeList = () => {
  const [recipes, setRecipes] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const data = await getRecipes();
        setRecipes(data);
      } catch (error) {
        console.error('Error fetching recipes:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, []);

  const filteredRecipes = recipes.filter(recipe =>
    recipe.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div>Loading recipes...</div>;
  }

  return (
    <div className="recipe-list">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Recipes</h2>
        <Link to="/recipes/new">
          <Button variant="primary">Add New Recipe</Button>
        </Link>
      </div>

      <Form.Group className="mb-4">
        <Form.Control
          type="text"
          placeholder="Search recipes..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </Form.Group>

      <Row xs={1} md={2} lg={3} className="g-4">
        {filteredRecipes.map(recipe => (
          <Col key={recipe.id}>
            <Card className="h-100">
              <Card.Body>
                <Card.Title>{recipe.name}</Card.Title>
                <Card.Text>
                  <small className="text-muted">
                    Prep: {recipe.prep_time} | Cook: {recipe.cook_time}
                  </small>
                  <br />
                  <small className="text-muted">
                    Servings: {recipe.servings}
                  </small>
                </Card.Text>
                <Link to={`/recipes/${recipe.id}`}>
                  <Button variant="outline-primary">View Recipe</Button>
                </Link>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">
                  Categories: {recipe.categories.map(c => c.name).join(', ')}
                </small>
              </Card.Footer>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default RecipeList;

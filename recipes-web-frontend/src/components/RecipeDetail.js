import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Button, ListGroup, Row, Col } from 'react-bootstrap';
import { getRecipe, deleteRecipe } from '../services/api';

const RecipeDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        const data = await getRecipe(id);
        setRecipe(data);
      } catch (error) {
        console.error('Error fetching recipe:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipe();
  }, [id]);

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this recipe?')) {
      try {
        await deleteRecipe(id);
        navigate('/recipes');
      } catch (error) {
        console.error('Error deleting recipe:', error);
      }
    }
  };

  if (loading) {
    return <div>Loading recipe...</div>;
  }

  if (!recipe) {
    return <div>Recipe not found</div>;
  }

  return (
    <div className="recipe-detail">
      <Card>
        <Card.Body>
          <div className="d-flex justify-content-between align-items-start mb-4">
            <div>
              <Card.Title className="h2">{recipe.name}</Card.Title>
              <Card.Subtitle className="mb-2 text-muted">
                Prep Time: {recipe.prep_time} | Cook Time: {recipe.cook_time} | Servings: {recipe.servings}
              </Card.Subtitle>
            </div>
            <div>
              <Button
                variant="outline-primary"
                className="me-2"
                onClick={() => navigate(`/recipes/${id}/edit`)}
              >
                Edit
              </Button>
              <Button variant="outline-danger" onClick={handleDelete}>
                Delete
              </Button>
            </div>
          </div>

          <Row>
            <Col md={6}>
              <h4>Ingredients</h4>
              <ListGroup variant="flush">
                {recipe.recipe_ingredients.map((ingredient, index) => (
                  <ListGroup.Item key={index}>
                    {ingredient.quantity} {ingredient.units} {ingredient.ingredient.name}
                    {ingredient.notes && <small className="text-muted"> ({ingredient.notes})</small>}
                  </ListGroup.Item>
                ))}
              </ListGroup>
            </Col>

            <Col md={6}>
              <h4>Instructions</h4>
              <div className="instructions">
                {recipe.instructions.split('\n').map((instruction, index) => (
                  <p key={index}>{instruction}</p>
                ))}
              </div>
            </Col>
          </Row>

          <div className="mt-4">
            <h5>Categories</h5>
            <div className="mb-2">
              {recipe.categories.map(category => (
                <span key={category.id} className="badge bg-secondary me-1">
                  {category.name}
                </span>
              ))}
            </div>

            <h5>Tags</h5>
            <div>
              {recipe.tags.map(tag => (
                <span key={tag.id} className="badge bg-info me-1">
                  {tag.name}
                </span>
              ))}
            </div>
          </div>

          {recipe.url && (
            <div className="mt-4">
              <a href={recipe.url} target="_blank" rel="noopener noreferrer">
                Original Recipe Link
              </a>
            </div>
          )}
        </Card.Body>
      </Card>
    </div>
  );
};

export default RecipeDetail;

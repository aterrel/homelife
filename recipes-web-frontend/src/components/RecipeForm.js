import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { getRecipe, createRecipe, updateRecipe, getCategories, getTags, getIngredients } from '../services/api';

const RecipeForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditing = !!id;

  const [formData, setFormData] = useState({
    name: '',
    prep_time: '',
    cook_time: '',
    servings: '',
    instructions: '',
    url: '',
    categories: [],
    tags: [],
    recipe_ingredients: [{ ingredient: '', quantity: '', units: '', notes: '', order: 0 }]
  });

  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState([]);
  const [ingredients, setIngredients] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [categoriesData, tagsData, ingredientsData] = await Promise.all([
          getCategories(),
          getTags(),
          getIngredients()
        ]);

        setCategories(categoriesData);
        setTags(tagsData);
        setIngredients(ingredientsData);

        if (isEditing) {
          const recipeData = await getRecipe(id);
          setFormData({
            ...recipeData,
            categories: recipeData.categories.map(c => c.id),
            tags: recipeData.tags.map(t => t.id),
            recipe_ingredients: recipeData.recipe_ingredients.map(ri => ({
              ingredient: ri.ingredient.id,
              quantity: ri.quantity,
              units: ri.units,
              notes: ri.notes || '',
              order: ri.order
            }))
          });
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id, isEditing]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleIngredientChange = (index, field, value) => {
    setFormData(prev => {
      const newIngredients = [...prev.recipe_ingredients];
      newIngredients[index] = {
        ...newIngredients[index],
        [field]: value,
        order: index
      };
      return {
        ...prev,
        recipe_ingredients: newIngredients
      };
    });
  };

  const addIngredient = () => {
    setFormData(prev => ({
      ...prev,
      recipe_ingredients: [
        ...prev.recipe_ingredients,
        { ingredient: '', quantity: '', units: '', notes: '', order: prev.recipe_ingredients.length }
      ]
    }));
  };

  const removeIngredient = (index) => {
    setFormData(prev => ({
      ...prev,
      recipe_ingredients: prev.recipe_ingredients.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isEditing) {
        await updateRecipe(id, formData);
      } else {
        await createRecipe(formData);
      }
      navigate('/recipes');
    } catch (error) {
      console.error('Error saving recipe:', error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Form onSubmit={handleSubmit}>
      <h2>{isEditing ? 'Edit Recipe' : 'New Recipe'}</h2>

      <Form.Group className="mb-3">
        <Form.Label>Recipe Name</Form.Label>
        <Form.Control
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </Form.Group>

      <Row>
        <Col md={4}>
          <Form.Group className="mb-3">
            <Form.Label>Prep Time (minutes)</Form.Label>
            <Form.Control
              type="number"
              name="prep_time"
              value={formData.prep_time}
              onChange={handleChange}
              required
            />
          </Form.Group>
        </Col>
        <Col md={4}>
          <Form.Group className="mb-3">
            <Form.Label>Cook Time (minutes)</Form.Label>
            <Form.Control
              type="number"
              name="cook_time"
              value={formData.cook_time}
              onChange={handleChange}
              required
            />
          </Form.Group>
        </Col>
        <Col md={4}>
          <Form.Group className="mb-3">
            <Form.Label>Servings</Form.Label>
            <Form.Control
              type="number"
              name="servings"
              value={formData.servings}
              onChange={handleChange}
              required
            />
          </Form.Group>
        </Col>
      </Row>

      <Form.Group className="mb-3">
        <Form.Label>Ingredients</Form.Label>
        {formData.recipe_ingredients.map((ingredient, index) => (
          <Row key={index} className="mb-2">
            <Col md={3}>
              <Form.Select
                value={ingredient.ingredient}
                onChange={(e) => handleIngredientChange(index, 'ingredient', e.target.value)}
                required
              >
                <option value="">Select Ingredient</option>
                {ingredients.map(ing => (
                  <option key={ing.id} value={ing.id}>{ing.name}</option>
                ))}
              </Form.Select>
            </Col>
            <Col md={2}>
              <Form.Control
                type="number"
                placeholder="Quantity"
                value={ingredient.quantity}
                onChange={(e) => handleIngredientChange(index, 'quantity', e.target.value)}
                required
              />
            </Col>
            <Col md={2}>
              <Form.Select
                value={ingredient.units}
                onChange={(e) => handleIngredientChange(index, 'units', e.target.value)}
                required
              >
                <option value="">Units</option>
                <option value="cup">Cup</option>
                <option value="tbsp">Tablespoon</option>
                <option value="tsp">Teaspoon</option>
                <option value="oz">Ounce</option>
                <option value="lb">Pound</option>
                <option value="g">Gram</option>
                <option value="kg">Kilogram</option>
                <option value="ml">Milliliter</option>
                <option value="l">Liter</option>
                <option value="pinch">Pinch</option>
                <option value="piece">Piece</option>
                <option value="whole">Whole</option>
                <option value="pkg">Package</option>
                <option value="slice">Slice</option>
              </Form.Select>
            </Col>
            <Col md={4}>
              <Form.Control
                type="text"
                placeholder="Notes"
                value={ingredient.notes}
                onChange={(e) => handleIngredientChange(index, 'notes', e.target.value)}
              />
            </Col>
            <Col md={1}>
              <Button
                variant="outline-danger"
                onClick={() => removeIngredient(index)}
                disabled={formData.recipe_ingredients.length === 1}
              >
                ×
              </Button>
            </Col>
          </Row>
        ))}
        <Button
          variant="outline-secondary"
          onClick={addIngredient}
          className="mt-2"
        >
          Add Ingredient
        </Button>
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Instructions</Form.Label>
        <Form.Control
          as="textarea"
          rows={5}
          name="instructions"
          value={formData.instructions}
          onChange={handleChange}
          required
        />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Categories</Form.Label>
        <div>
          {categories.map(category => (
            <Form.Check
              key={category.id}
              inline
              type="checkbox"
              label={category.name}
              checked={formData.categories.includes(category.id)}
              onChange={(e) => {
                const categoryId = category.id;
                setFormData(prev => ({
                  ...prev,
                  categories: e.target.checked
                    ? [...prev.categories, categoryId]
                    : prev.categories.filter(id => id !== categoryId)
                }));
              }}
            />
          ))}
        </div>
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Tags</Form.Label>
        <div>
          {tags.map(tag => (
            <Form.Check
              key={tag.id}
              inline
              type="checkbox"
              label={tag.name}
              checked={formData.tags.includes(tag.id)}
              onChange={(e) => {
                const tagId = tag.id;
                setFormData(prev => ({
                  ...prev,
                  tags: e.target.checked
                    ? [...prev.tags, tagId]
                    : prev.tags.filter(id => id !== tagId)
                }));
              }}
            />
          ))}
        </div>
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Recipe URL (optional)</Form.Label>
        <Form.Control
          type="url"
          name="url"
          value={formData.url}
          onChange={handleChange}
        />
      </Form.Group>

      <div className="d-flex justify-content-between">
        <Button variant="secondary" onClick={() => navigate('/recipes')}>
          Cancel
        </Button>
        <Button variant="primary" type="submit">
          {isEditing ? 'Update Recipe' : 'Create Recipe'}
        </Button>
      </div>
    </Form>
  );
};

export default RecipeForm;

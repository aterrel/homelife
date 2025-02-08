import React, { useState, useEffect } from 'react';
import { Card, Button, ListGroup, Badge } from 'react-bootstrap';
import { mealPlanApi } from '../services/api';
import MealSlotModal from './MealSlotModal';

const MealPlanView = ({ mealPlan: initialMealPlan }) => {
    const [mealPlan, setMealPlan] = useState(initialMealPlan);
    const [showAddSlotModal, setShowAddSlotModal] = useState(false);

    const fetchMealPlan = async () => {
        try {
            const response = await mealPlanApi.get(mealPlan.id);
            setMealPlan(response.data);
        } catch (error) {
            console.error('Error fetching meal plan:', error);
        }
    };

    const handleMealSlotAdded = () => {
        fetchMealPlan();
    };

    // Group meal slots by date
    const mealSlotsByDate = mealPlan.meal_slots.reduce((acc, slot) => {
        if (!acc[slot.date]) {
            acc[slot.date] = [];
        }
        acc[slot.date].push(slot);
        return acc;
    }, {});

    // Sort dates
    const sortedDates = Object.keys(mealSlotsByDate).sort();

    return (
        <Card className="mb-4">
            <Card.Header className="d-flex justify-content-between align-items-center">
                <div>
                    <h4 className="mb-0">{mealPlan.name}</h4>
                    <small className="text-muted">Start Date: {mealPlan.start_date}</small>
                </div>
                <Button 
                    variant="primary" 
                    size="sm"
                    onClick={() => setShowAddSlotModal(true)}
                >
                    Add Recipe
                </Button>
            </Card.Header>
            <Card.Body>
                {mealPlan.notes && (
                    <Card.Text className="mb-3">{mealPlan.notes}</Card.Text>
                )}
                {sortedDates.map(date => (
                    <div key={date} className="mb-4">
                        <h5>{date}</h5>
                        <ListGroup>
                            {mealSlotsByDate[date]
                                .sort((a, b) => a.meal_type_order - b.meal_type_order)
                                .map(slot => (
                                    <ListGroup.Item 
                                        key={slot.id}
                                        className="d-flex justify-content-between align-items-center"
                                    >
                                        <div>
                                            <Badge bg="info" className="me-2">
                                                {slot.meal_type.charAt(0).toUpperCase() + slot.meal_type.slice(1)}
                                            </Badge>
                                            {slot.recipe ? slot.recipe.name : 'No recipe selected'}
                                            {slot.servings > 1 && (
                                                <small className="text-muted ms-2">
                                                    ({slot.servings} servings)
                                                </small>
                                            )}
                                        </div>
                                        {slot.notes && (
                                            <small className="text-muted">{slot.notes}</small>
                                        )}
                                    </ListGroup.Item>
                                ))}
                        </ListGroup>
                    </div>
                ))}
            </Card.Body>
            <MealSlotModal
                show={showAddSlotModal}
                onHide={() => setShowAddSlotModal(false)}
                mealPlan={mealPlan}
                onMealSlotAdded={handleMealSlotAdded}
            />
        </Card>
    );
};

export default MealPlanView;

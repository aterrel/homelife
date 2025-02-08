import React, { useState, useEffect } from 'react';
import { Container, Button, Row, Col } from 'react-bootstrap';
import MealPlanModal from '../components/MealPlanModal';
import MealPlanView from '../components/MealPlanView';
import { mealPlanApi } from '../services/api';

const Meals = ({ isLoggedIn }) => {
    const [mealPlans, setMealPlans] = useState([]);
    const [showMealPlanModal, setShowMealPlanModal] = useState(false);

    const fetchMealPlans = async () => {
        try {
            const response = await mealPlanApi.getAll();
            setMealPlans(response.data);
        } catch (error) {
            console.error('Error fetching meal plans:', error);
            if (error.response?.status === 401) {
                setMealPlans([]);
            }
        }
    };

    useEffect(() => {
        if (isLoggedIn) {
            fetchMealPlans();
        } else {
            setMealPlans([]);
        }
    }, [isLoggedIn]);

    const handleMealPlanAdded = () => {
        fetchMealPlans();
    };

    if (!isLoggedIn) {
        return (
            <Container>
                <div className="text-center mt-5">
                    <h2>Please log in to view and manage meal plans</h2>
                </div>
            </Container>
        );
    }

    return (
        <Container>
            <Row className="mb-4">
                <Col>
                    <div className="d-flex justify-content-between align-items-center">
                        <h1>Meal Plans</h1>
                        <Button 
                            variant="success" 
                            onClick={() => setShowMealPlanModal(true)}
                        >
                            Create Meal Plan
                        </Button>
                    </div>
                </Col>
            </Row>
            <Row>
                <Col>
                    {mealPlans.length === 0 ? (
                        <div className="text-center mt-5">
                            <h3>No meal plans yet</h3>
                            <p>Create your first meal plan to get started!</p>
                        </div>
                    ) : (
                        mealPlans.map(mealPlan => (
                            <MealPlanView 
                                key={mealPlan.id} 
                                mealPlan={mealPlan}
                            />
                        ))
                    )}
                </Col>
            </Row>
            <MealPlanModal
                show={showMealPlanModal}
                onHide={() => setShowMealPlanModal(false)}
                onMealPlanAdded={handleMealPlanAdded}
            />
        </Container>
    );
};

export default Meals;

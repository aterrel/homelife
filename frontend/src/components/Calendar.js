import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { Card, Button, ButtonGroup } from 'react-bootstrap';

import EventModal from './EventModal';
import MealPlanModal from './MealPlanModal';
import MealSlotModal from './MealSlotModal';
import LoginModal from './LoginModal';
import { eventApi, mealPlanApi } from '../services/api';

// Set up the localizer for the calendar using Moment.js
const localizer = momentLocalizer(moment);

const MyCalendar = ({ isLoggedIn, onLogin }) => {
    const [events, setEvents] = useState([]);
    const [mealSlots, setMealSlots] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [selectedMealSlot, setSelectedMealSlot] = useState(null);
    const [showEventModal, setShowEventModal] = useState(false);
    const [showMealPlanModal, setShowMealPlanModal] = useState(false);
    const [showMealSlotModal, setShowMealSlotModal] = useState(false);
    const [showLoginModal, setShowLoginModal] = useState(false);

    // Fetch events and meal slots from the backend API
    const fetchEvents = async () => {
        try {
            const response = await eventApi.getAll();
            const formattedEvents = response.data.map(event => ({
                id: event.id,
                title: event.title,
                start: new Date(`${event.date}T${event.time || '00:00:00'}`),
                end: new Date(`${event.date}T${event.time || '00:00:00'}`),
                date: event.date,
                time: event.time,
                type: 'event'
            }));
            setEvents(formattedEvents);
        } catch (error) {
            console.error('Error fetching events:', error);
            if (error.response?.status === 401) {
                setEvents([]);
            }
        }
    };

    const fetchMealSlots = async () => {
        try {
            const response = await mealPlanApi.getAllSlots();
            const formattedSlots = response.data.map(slot => ({
                id: slot.id,
                title: `${slot.meal_type.charAt(0).toUpperCase() + slot.meal_type.slice(1)}: ${slot.recipe.name}`,
                start: new Date(`${slot.date}T00:00:00`),
                end: new Date(`${slot.date}T00:00:00`),
                type: 'meal',
                originalSlot: slot
            }));
            setMealSlots(formattedSlots);
        } catch (error) {
            console.error('Error fetching meal slots:', error);
            if (error.response?.status === 401) {
                setMealSlots([]);
            }
        }
    };

    // Fetch data when logged in status changes
    useEffect(() => {
        if (isLoggedIn) {
            fetchEvents();
            fetchMealSlots();
        } else {
            setEvents([]);
            setMealSlots([]);
        }
    }, [isLoggedIn]);

    const handleEventClick = (event) => {
        if (!isLoggedIn) {
            setShowLoginModal(true);
            return;
        }
        if (event.type === 'meal') {
            setSelectedMealSlot(event.originalSlot);
            setShowMealSlotModal(true);
        } else {
            setSelectedEvent(event);
            setShowEventModal(true);
        }
    };

    const handleMealSlotSave = async (updatedSlot) => {
        try {
            await mealPlanApi.updateSlot(selectedMealSlot.id, updatedSlot);
            fetchMealSlots();
            setShowMealSlotModal(false);
            setSelectedMealSlot(null);
        } catch (error) {
            console.error('Error updating meal slot:', error);
        }
    };

    const handleMealSlotDelete = async () => {
        try {
            await mealPlanApi.deleteSlot(selectedMealSlot.id);
            fetchMealSlots();
            setShowMealSlotModal(false);
            setSelectedMealSlot(null);
        } catch (error) {
            console.error('Error deleting meal slot:', error);
        }
    };

    const handleEventAdded = () => {
        fetchEvents();
    };

    const handleMealPlanAdded = () => {
        fetchMealSlots();
    };

    const handleLogin = (userData) => {
        onLogin(userData);
        setShowLoginModal(false);
    };

    if (!isLoggedIn) {
        return (
            <div style={{ margin: '20px' }}>
                <Card className="text-center">
                    <Card.Body>
                        <Card.Title>Welcome to Family Calendar</Card.Title>
                        <Card.Text>
                            Please log in to view and manage your family calendar.
                        </Card.Text>
                        <Button variant="primary" onClick={() => setShowLoginModal(true)}>
                            Log In
                        </Button>
                    </Card.Body>
                </Card>
                <LoginModal
                    show={showLoginModal}
                    onHide={() => setShowLoginModal(false)}
                    onLogin={handleLogin}
                />
            </div>
        );
    }

    // Combine events and meal slots for display
    const allEvents = [...events, ...mealSlots];

    return (
        <div style={{ margin: '20px' }}>
            <h2>Family Calendar</h2>
            <ButtonGroup className="mb-3">
                <Button 
                    variant="primary" 
                    onClick={() => setShowEventModal(true)}
                >
                    Add Event
                </Button>
                <Button 
                    variant="success" 
                    onClick={() => setShowMealPlanModal(true)}
                >
                    Create Meal Plan
                </Button>
            </ButtonGroup>
            <Calendar
                localizer={localizer}
                events={allEvents}
                startAccessor="start"
                endAccessor="end"
                style={{ height: 500 }}
                onSelectEvent={handleEventClick}
                eventPropGetter={(event) => ({
                    className: event.type === 'meal' ? 'rbc-event-meal' : 'rbc-event-regular',
                    style: {
                        backgroundColor: event.type === 'meal' ? '#28a745' : '#007bff'
                    }
                })}
            />
            <EventModal
                show={showEventModal}
                onHide={() => setShowEventModal(false)}
                event={selectedEvent}
                onEventAdded={handleEventAdded}
                onEventUpdated={handleEventAdded}
                onEventDeleted={handleEventAdded}
            />
            <MealPlanModal
                show={showMealPlanModal}
                onHide={() => setShowMealPlanModal(false)}
                onMealPlanAdded={handleMealPlanAdded}
            />
            <MealSlotModal
                show={showMealSlotModal}
                onHide={() => {
                    setShowMealSlotModal(false);
                    setSelectedMealSlot(null);
                }}
                mealSlot={selectedMealSlot}
                onSave={handleMealSlotSave}
                onDelete={handleMealSlotDelete}
            />
            <LoginModal
                show={showLoginModal}
                onHide={() => setShowLoginModal(false)}
                onLogin={handleLogin}
            />
        </div>
    );
};

export default MyCalendar;

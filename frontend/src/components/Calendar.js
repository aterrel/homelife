import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { Card, Button } from 'react-bootstrap';

import EventModal from './EventModal';
import LoginModal from './LoginModal';
import { eventApi } from '../services/api';

// Set up the localizer for the calendar using Moment.js
const localizer = momentLocalizer(moment);

const MyCalendar = ({ isLoggedIn, onLogin }) => {
    const [events, setEvents] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [showEventModal, setShowEventModal] = useState(false);
    const [showLoginModal, setShowLoginModal] = useState(false);

    // Fetch events from the backend API
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
            }));
            setEvents(formattedEvents);
        } catch (error) {
            console.error('Error fetching events:', error);
            if (error.response?.status === 401) {
                setEvents([]);
            }
        }
    };

    // Fetch events when logged in status changes
    useEffect(() => {
        if (isLoggedIn) {
            fetchEvents();
        } else {
            setEvents([]);
        }
    }, [isLoggedIn]);

    const handleEventClick = (event) => {
        if (!isLoggedIn) {
            setShowLoginModal(true);
            return;
        }
        setSelectedEvent(event);
        setShowEventModal(true);
    };

    const handleEventAdded = () => {
        fetchEvents();
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

    return (
        <div style={{ margin: '20px' }}>
            <h2>Family Calendar</h2>
            <Button 
                variant="primary" 
                className="mb-3"
                onClick={() => setShowEventModal(true)}
            >
                Add Event
            </Button>
            <Calendar
                localizer={localizer}
                events={events}
                startAccessor="start"
                endAccessor="end"
                style={{ height: 500 }}
                onSelectEvent={handleEventClick}
            />
            <EventModal
                show={showEventModal}
                onHide={() => setShowEventModal(false)}
                event={selectedEvent}
                onEventAdded={handleEventAdded}
                onEventUpdated={handleEventAdded}
                onEventDeleted={handleEventAdded}
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

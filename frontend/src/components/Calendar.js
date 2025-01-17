import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';

import EventModal from './EventModal';

// Set up the localizer for the calendar using Moment.js
const localizer = momentLocalizer(moment);

const MyCalendar = () => {
    const [events, setEvents] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [showModal, setShowModal] = useState(false);

    // Fetch events from the backend API
    const fetchEvents = async () => {
        try {
            const response = await axios.get('/api/events/');
            const formattedEvents = response.data.map(event => ({
                id: event.id,
                title: event.title,
                start: new Date(`${event.date}T${event.time}`),
                end: new Date(`${event.date}T${event.time}`),
                date: event.date,
                time: event.time,
            }));
            setEvents(formattedEvents);
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    };

    // Fetch events from the backend API
    useEffect(() => {
        fetchEvents();
    }, []);

    const handleEventClick = (event) => {
        setSelectedEvent(event);
        setShowModal(true);
    }

    const handleEventAdded = (newEvent) => {
        fetchEvents();
    };

    return (
        <div style={{ margin: '20px' }}>
            <h2>Family Calendar</h2>
            <button
                className="btn btn-primary mb-3"
                onClick={() => setShowModal(true)}
            >
                Add New Event
            </button>
            <Calendar
                localizer={localizer}
                events={events}
                startAccessor="start"
                endAccessor="end"
                style={{ height: 500 }}
                onSelectEvent={handleEventClick}
            />
            <EventModal
                show={showModal}
                handleClose={() => setShowModal(false)}
                event={selectedEvent}
                onEventAdded={handleEventAdded}
            />
        </div>
    );
};

export default MyCalendar;

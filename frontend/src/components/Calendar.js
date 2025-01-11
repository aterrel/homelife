import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';

import AddEventForm from './AddEventForm';

// Set up the localizer for the calendar using Moment.js
const localizer = momentLocalizer(moment);

const MyCalendar = () => {
    const [events, setEvents] = useState([]);

    // Fetch events from the backend API
    const fetchEvents = async () => {
        try {
            const response = await axios.get('/api/events/');
            const formattedEvents = response.data.map(event => ({
                title: event.title,
                start: new Date(`${event.date}T${event.time}`),
                end: new Date(`${event.date}T${event.time}`),
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

    const handleEventAdded = (newEvent) => {
        fetchEvents();
    };

    return (
        <div style={{ height: '80vh', margin: '20px' }}>
            <h2>Family Calendar</h2>
            <AddEventForm onEventAdded={handleEventAdded} />
            <Calendar
                localizer={localizer}
                events={events}
                startAccessor="start"
                endAccessor="end"
                style={{ height: 500 }}
            />
        </div>
    );
};

export default MyCalendar;

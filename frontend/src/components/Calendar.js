import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';

// Set up the localizer for the calendar using Moment.js
const localizer = momentLocalizer(moment);

const MyCalendar = () => {
    const [events, setEvents] = useState([]);

    // Fetch events from the backend API
    useEffect(() => {
        axios.get('/api/events/')
            .then(response => {
                // Map backend data to react-big-calendar's format
                const formattedEvents = response.data.map(event => ({
                    title: event.title,
                    start: new Date(`${event.date}T${event.time}`),
                    end: new Date(`${event.date}T${event.time}`),
                }));
                setEvents(formattedEvents);
            })
            .catch(error => {
                console.error("Error fetching events:", error);
            });
    }, []);

    return (
        <div style={{ height: '80vh', margin: '20px' }}>
            <h2>Family Calendar</h2>
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

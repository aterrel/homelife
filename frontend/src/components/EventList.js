import React, { useEffect, useState } from 'react';
import axios from 'axios';

const EventList = () => {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        axios.get('/events').then((response) => { setEvents(response.data) });
    }, []);

    return (
        <div>
            <h1>Events</h1>
            <ul>
                {events.map((event) => (
                    <li key={event.id}>{event.title} - {event.date}</li>
                ))}
            </ul>
        </div>
    );
};

export default EventList;

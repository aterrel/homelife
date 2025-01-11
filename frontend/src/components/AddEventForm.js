import React, { useState } from 'react';
import axios from 'axios';

const AddEventForm = ({ onEventAdded }) => {
    const [title, setTitle] = useState('');
    const [date, setDate] = useState('');
    const [time, setTime] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        const newEvent = {
            title,
            date,
            time,
        };

        try {
            // Send POST request to the API to create a new event
            const response = await axios.post('/api/events/', newEvent);
            alert('Event added successfully!');
            onEventAdded(response.data); // Notify parent about the new event
            setTitle('');
            setDate('');
            setTime('');
        } catch (error) {
            console.error('Error adding event:', error);
            alert('Failed to add event. Please try again.');
        }
    };

    return (
        <div style={{ marginBottom: '20px' }}>
            <h3>Add New Event</h3>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Title:</label>
                    <input
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Date:</label>
                    <input
                        type="date"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Time:</label>
                    <input
                        type="time"
                        value={time}
                        onChange={(e) => setTime(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Add Event</button>
            </form>
        </div>
    );
};

export default AddEventForm;

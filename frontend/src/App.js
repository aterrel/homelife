import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

import EventList from './components/EventList';
import MyCalendar from './components/Calendar';

function App() {
  return (
    <div>
      <header>
        <h1>Homelife</h1>
      </header>
      <main>
        <MyCalendar />
        <EventList />
      </main>
    </div>
  );
}

export default App;
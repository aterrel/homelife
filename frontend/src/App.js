import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Navbar from './components/Navbar';
import EventList from './components/EventList';
import MyCalendar from './components/Calendar';

function App() {
  return (
    <div className="App">
      <Navbar />
      <main className="app-content">
        <header>
          <h1>Homelife</h1>
        </header>
        <MyCalendar />
        <EventList />
      </main>
    </div>
  );
}

export default App;
import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import LoginPage from './LoginPage';
import MyCalendar from './Calendar';
import RoomReservationSelector from './RoomReservationSelector';
import RoomReservationAttendeeInput from './RoomReservationAttendeeInput';
import RoomReservationSubmit from './RoomReservationSubmit';
import Socket from './Socket';

export default function ReservationOverview(props) {
    const { name } = props;
    const [attendeeCount, setAttendeeCount] = useState(0);
    const [attendees, setAttendees] = useState([]);

    function logout(event) {
        ReactDOM.render(<LoginPage />, document.getElementById('content'));
    }

    return (
        <div id='contentContainer'>
            <h1>Breakout Room Breakdown</h1>
            <p id='welcomeText'> Welcome {name} </p>
            <form id='logoutForm' onClick={logout}>
                <button>Logout</button>
            </form>
            <MyCalendar />
            <div id='reservationForm'>
                <RoomReservationSelector setAttendeeCount={setAttendeeCount} />
                <RoomReservationAttendeeInput
                    attendeeCount={attendeeCount}
                    setAttendees={setAttendees}
                />
                <RoomReservationSubmit />
            </div>
        </div>
    );
}
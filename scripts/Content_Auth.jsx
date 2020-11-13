import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import MyCalendar from './Calendar';
import RoomReservationSelector from './RoomReservationSelector';
import RoomReservationAttendeeInput from './RoomReservationAttendeeInput';
import RoomReservationSubmit from './RoomReservationSubmit';
import Socket from './Socket';

export default function Content_Auth(props) {
    const { name } = props;
    const [attendeeCount, setAttendeeCount] = useState(0);
    const [attendees, setAttendees] = useState([]);

    function logout(event) {
        ReactDOM.render(<Content />, document.getElementById('Content'));
    }

    return (
        <div id='contentContainer'>
            <h1>Breakout Room Breakdown</h1>
            <p> Welcome {name} </p>

            <form onClick={logout}>
                <button>Logout</button>
            </form>
            <MyCalendar />
            <RoomReservationSelector setAttendeeCount={setAttendeeCount} />
            <RoomReservationAttendeeInput 
                attendeeCount={attendeeCount}
                setAttendees={setAttendees}
            />
            <RoomReservationSubmit />
        </div>
    );
}
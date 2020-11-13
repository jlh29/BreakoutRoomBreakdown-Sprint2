import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import LoginPage from './LoginPage';
import MyCalendar from './Calendar';
import RoomReservationSelector from './RoomReservationSelector';
import RoomReservationAttendeeInput from './RoomReservationAttendeeInput';
import RoomReservationSubmit from './RoomReservationSubmit';
import RoomReservationTimeInfo from './RoomReservationTimeInfo';
import Socket from './Socket';

export default function ReservationOverview(props) {
    const { name } = props;
    const [attendeeCount, setAttendeeCount] = useState(0);
    const [attendees, setAttendees] = useState([]);
    const [date, setDate] = useState(new Date());
    const [time, setTime] = useState("");
    const [dateChanged, setDateChanged] = useState(false);
    const [timeChanged, setTimeChanged] = useState(false);

    function updateDate(newDate) {
        setDate(newDate);
        if (!dateChanged) {
            setDateChanged(true);
        }
    }

    function updateTime(newTime) {
        setTime(newTime);
        if (!timeChanged) {
            setTimeChanged(true);
        }
    }

    function handleReservationSubmit() {
        // TODO: jlh29, actually send the info to the server
    }

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
            <MyCalendar
                date={date}
                setDate={updateDate}
                time={time}
                setTime={updateTime}
            />
            <div id='reservationForm'>
                <RoomReservationTimeInfo
                    selectedDate={dateChanged ? date : null}
                    selectedTime={timeChanged ? time : null}
                />
                <RoomReservationSelector setAttendeeCount={setAttendeeCount} />
                <RoomReservationAttendeeInput
                    attendeeCount={attendeeCount}
                    setAttendees={setAttendees}
                />
                <RoomReservationSubmit handleSubmit={handleReservationSubmit} />
            </div>
        </div>
    );
}
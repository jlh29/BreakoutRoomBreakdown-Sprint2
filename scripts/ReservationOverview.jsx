import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import LoginPage from './LoginPage';
import MyCalendar from './Calendar';
import ReservationConfirmation from './ReservationConfirmation';
import RoomReservationSelector from './RoomReservationSelector';
import RoomReservationAttendeeInput from './RoomReservationAttendeeInput';
import RoomReservationSubmit from './RoomReservationSubmit';
import RoomReservationTimeInfo from './RoomReservationTimeInfo';
import Socket from './Socket';

export default function ReservationOverview(props) {
    const { name } = props;
    const [attendeeCount, setAttendeeCount] = useState(0);
    const [attendees, setAttendees] = useState([]);
    const [availableDates, setAvailableDates] = useState([]);
    const [allTimes, setAllTimes] = useState([]);
    const [date, setDate] = useState(new Date());
    const [time, setTime] = useState("");
    const [dateChanged, setDateChanged] = useState(false);
    const [timeChanged, setTimeChanged] = useState(false);

    function getDateString(inputDate) {
        return inputDate.toLocaleDateString(
            'en-US',
            {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
            },
        );
    }

    function getTimesForSelectedDate(){
        console.log(`User selected the date "${date}"`);
        Socket.emit('time availability request', {date: getDateString(date)});
    }

    function getAvailableDates() {
        let today = new Date();
        console.log(`User requesting available dates near ${today}`);
        Socket.emit('date availability request', {date: getDateString(today)});
    }

    function updateAllTimes(data) {
        setAllTimes(data.times);
    }

    function updateAvailableDates(data) {
        let constructedDates = [];
        for (let dateTimestamp of data.dates) {
            constructedDates.push(new Date(dateTimestamp));
        }
        setAvailableDates(constructedDates);
    }

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
        // TODO: Make sure that the rooms can accommodate the number of users
        if (!timeChanged || !dateChanged) {
            return;
        }
        if (attendees.length == 0) {
            return;
        }
        let selectedDateTimestamp = date.getTime();
        Socket.emit(
            'reservation submit',
            {date: selectedDateTimestamp, time, attendees},
        );
    }

    function handleReservationResponse(data) {
        if (data.successful) {
            ReactDOM.render(
                <ReservationConfirmation
                    reservation={data.reservation}
                    checkInCode={data.code}
                />,
                document.getElementById('content'),
            );
        }
    }

    function logout(event) {
        ReactDOM.render(<LoginPage />, document.getElementById('content'));
    }

    function listenToServer() {
        useEffect(() => {
            Socket.on('time availability response', updateAllTimes);
            Socket.on('date availability response', updateAvailableDates);
            Socket.on('reservation response', handleReservationResponse);
            return () => {
                Socket.off('time availability response', updateAllTimes);
                Socket.off('date availability response', updateAvailableDates);
                Socket.off('reservation response', handleReservationResponse);
            };
        });
    }

    useEffect(() => {
        if (dateChanged) {
            getTimesForSelectedDate();
        }
    }, [date, dateChanged]);

    useEffect(() => {
        getAvailableDates();
    }, []);

    listenToServer();

    return (
        <div id='contentContainer' className='flexColumn'>
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
                allTimes={allTimes}
                availableDates={availableDates}
            />
            <div id='reservationForm' className='flexColumn'>
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
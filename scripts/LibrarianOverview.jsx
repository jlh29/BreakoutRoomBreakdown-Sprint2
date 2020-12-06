import React, { useEffect, useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import ConnectingBanner from './ConnectingBanner';
import LibrarianCheckIn from './LibrarianCheckIn';
import LibrarianAppointmentsOverview from './LibrarianAppointmentsOverview';
import LibrarianUsersOverview from './LibrarianUsersOverview';
import LibrarianRoomsOverview from './LibrarianRoomsOverview';
import LibrarianDateInput from './LibrarianDateInput';
import LibrarianDisableButton from './LibrarianDisableButton';
import Socket from './Socket';

export default function LibrarianOverview() {
  const [connected, setConnected] = useState(false);
  const [appointments, setAppointments] = useState([]);
  const [selectedAppointment, setSelectedAppointment] = useState({});
  const [users, setUsers] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [unavailableDates, setUnavailableDates] = useState([]);
  const [checkInSuccess, setCheckInSuccess] = useState(true);
  const [showCheckInResult, setShowCheckInResult] = useState(false);
  const checkInResultDisplayTime = 5000;
  const checkInRef = React.createRef();
  const [checkInResultTimeoutId, setCheckInResultTimeoutId] = useState(-1);

  function getDateString(date) {
    return date.toLocaleDateString(
      'en-US',
      {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      },
    );
  }

  function isUnavailableDate({ activeStartDate, date, view }) {
    if (view == 'month' && date.getDay() % 6 == 0) {
      return true;
    }
    for (const unavailableDate of unavailableDates) {
      if (date.getDate() == unavailableDate.getDate()
                    && date.getMonth() == unavailableDate.getMonth()
                    && date.getFullYear() == unavailableDate.getFullYear()) {
        return true;
      }
    }
    return false;
  }

  function requestAllData() {
    Socket.emit('overview request', { date: getDateString(selectedDate) });
    Socket.emit('date availability request', { date: getDateString(new Date()) });
  }

  function requestAppointmentsForDate(date) {
    Socket.emit('appointments request', { date: getDateString(date) });
  }

  function onMonthChanged({ activeStartDate, value, view }) {
    setSelectedAppointment({});
    Socket.emit(
      'date availability request',
      { date: getDateString(activeStartDate) },
    );
  }

  function onCalendarChanged(newDate) {
    setSelectedDate((oldDate) => newDate);
    setSelectedAppointment({});
    requestAppointmentsForDate(newDate);
  }

  function establishConnection() {
    // TODO: jlh29, use this to ensure that the connecting client has the
    // correct role first
    requestAllData();
  }

  function updateCheckInSuccess(data) {
    console.log(data.successful);
    setCheckInSuccess(data.successful);
    setShowCheckInResult(true);
    if (checkInResultTimeoutId >= 0) {
      clearTimeout(checkInResultTimeoutId);
    }
    setCheckInResultTimeoutId(
      setTimeout(
        () => setShowCheckInResult(false),
        checkInResultDisplayTime,
      ),
    );
  }

  function onCheckInSubmitClicked() {
    const checkInID = checkInRef.current.value.trim();
    if (checkInID.length > 0) {
      Socket.emit('check in', { code: checkInID });
    }
    checkInRef.current.value = '';
  }

  function updateStateArray(stateSet, dataKey, data) {
    // TODO: jlh29, update this for when items can be removed from the array
    stateSet(
      (oldValues) => {
        const updatedValues = [];
        for (const newValue of data[dataKey]) {
          let isNew = true;
          for (const index in updatedValues) {
            if (updatedValues[index].id == newValue.id) {
              updatedValues[index] = newValue;
              isNew = false;
              break;
            }
          }
          if (isNew) {
            updatedValues.push(newValue);
          }
        }
        return updatedValues;
      },
    );
  }

  function updateAppointments(data) {
    console.log('Updating appointments...');
    if (!connected) {
      setConnected(true);
    }
    setAppointments(data.appointments);
  }

  function updateUnavailableDates(data) {
    if (!connected) {
      setConnected(true);
    }
    const newDates = [];
    for (const date of data.dates) {
      const currDate = new Date(date);
      newDates.push(currDate);
    }
    setUnavailableDates(newDates);
  }

  function updateUsers(data) {
    if (!connected) {
      setConnected(true);
    }
    updateStateArray(setUsers, 'users', data);
  }

  function updateRooms(data) {
    if (!connected) {
      setConnected(true);
    }
    updateStateArray(setRooms, 'rooms', data);
  }

  function listenToServer() {
    useEffect(() => {
      Socket.on('connect', establishConnection);
      Socket.on('appointments response', updateAppointments);
      Socket.on('users response', updateUsers);
      Socket.on('rooms response', updateRooms);
      Socket.on('unavailable dates response', updateUnavailableDates);
      Socket.on('check in response', updateCheckInSuccess);
      return () => {
        Socket.off('connect', establishConnection);
        Socket.off('appointments response', updateAppointments);
        Socket.off('users response', updateUsers);
        Socket.off('rooms response', updateRooms);
        Socket.off('unavailable dates response', updateUnavailableDates);
        Socket.off('check in response', updateCheckInSuccess);
      };
    });
  }

  listenToServer();

  useEffect(() => {
    if (!connected) {
      establishConnection();
    }
    return () => {};
  }, [connected]);

  return (
    <div id="librarianOverviewContainer" className="flexColumn">
      {!connected ? <ConnectingBanner /> : null}
      <h1 id="reservationsBanner">Reservations</h1>
      <div id="appointmentsAndCalendarContainer">
        <Calendar
          onChange={onCalendarChanged}
          value={selectedDate}
          tileDisabled={isUnavailableDate}
          onActiveStartDateChange={onMonthChanged}
          showNeighboringMonth={false}
          calendarType="US"
          className="appointmentsCalendar"
        />
        <LibrarianAppointmentsOverview
          appointments={appointments}
          selectedAppointment={selectedAppointment}
          setSelectedAppointment={setSelectedAppointment}
        />
      </div>
      <h1 id="checkInBanner">Check-in</h1>
      <LibrarianCheckIn
        inputRef={checkInRef}
        submitClick={onCheckInSubmitClicked}
        showResult={showCheckInResult}
        isSuccess={checkInSuccess}
      />
      
      <h1 id="calendarMarking">Calendar Markings</h1>
      <LibrarianDateInput />
      
      <h1 id="usersBanner">Users</h1>
      <LibrarianUsersOverview users={users} />
      <h1 id="roomsBanner">Rooms</h1>
      <LibrarianRoomsOverview rooms={rooms} />
    </div>
  );
}

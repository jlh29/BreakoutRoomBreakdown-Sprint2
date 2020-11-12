import React, { useEffect, useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import LibrarianCheckIn from './LibrarianCheckIn';
import LibrarianAppointmentsOverview from './LibrarianAppointmentsOverview';
import LibrarianUsersOverview from './LibrarianUsersOverview';
import LibrarianRoomsOverview from './LibrarianRoomsOverview';
import Socket from './Socket';

export default function LibrarianOverview() {
    const [appointments, setAppointments] = useState([]);
    const [users, setUsers] = useState([]);
    const [rooms, setRooms] = useState([]);
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [unavailableDates, setUnavailableDates] = useState([]);
    const [checkInSuccess, setCheckInSuccess] = useState(true);
    const [showCheckInResult, setShowCheckInResult] = useState(false);
    const checkInResultDisplayTime = 5000;
    const checkInRef = React.createRef();

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

    function isUnavailableDate({activeStartDate, date, view}) {
        for (let unavailableDate of unavailableDates) {
            if (date.getDate() == unavailableDate.getDate()
                    && date.getMonth() == unavailableDate.getMonth()
                    && date.getFullYear() == unavailableDate.getFullYear()) {
                return true;
            }
        }
        return false;
    }

    function requestAllData() {
        Socket.emit('overview request', {date: getDateString(selectedDate)});
        Socket.emit('unavailable dates request', {date: getDateString(new Date())});
    }

    function requestAppointmentsForDate(date) {
        Socket.emit('appointments request', {date: getDateString(date)});
    }
    
    function onMonthChanged({activeStartDate, value, view}) {
        Socket.emit(
            'unavailable dates request',
            {date: getDateString(activeStartDate)},
        );
    }

    function onCalendarChanged(newDate) {
        setSelectedDate(oldDate => newDate);
        requestAppointmentsForDate(newDate);
    }

    function establishConnection() {
        // TODO: jlh29, use this to ensure that the connecting client has the
        // correct role first
        requestAllData();
    }

    function updateCheckInSuccess(success) {
        setCheckInSuccess(success);
        setShowCheckInResult(true);
        setTimeout(() => setShowCheckInResult(false), checkInResultDisplayTime);
    }

    function onCheckInSubmitClicked() {
        let checkInID = checkInRef.current.value.trim();
        if (checkInID.length > 0) {
            Socket.emit('check in', {checkInID}, updateCheckInSuccess);
        }
        checkInRef.current.value = '';
    }

    function updateStateArray(stateSet, dataKey, data) {
        // TODO: jlh29, update this for when items can be removed from the array
        stateSet(
            oldValues => {
                let updatedValues = [];
                for (let newValue of data[dataKey]) {
                    let isNew = true;
                    for (let index in updatedValues) {
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
            }
        );
    }

    function updateAppointments(data) {
        setAppointments(data.appointments);
    }

    function updateUnavailableDates(data) {
        let newDates = [];
        for (let date of data.dates) {
            let currDate = new Date(date);
            newDates.push(currDate);
        }
        setUnavailableDates(newDates);
    }

    function updateUsers(data) {
        updateStateArray(setUsers, 'users', data);
    }

    function updateRooms(data) {
        updateStateArray(setRooms, 'rooms', data);
    }

    function listenToServer() {
        useEffect(() => {
            Socket.on('connect', establishConnection);
            Socket.on('appointments response', updateAppointments);
            Socket.on('users response', updateUsers);
            Socket.on('rooms response', updateRooms);
            Socket.on('unavailable dates response', updateUnavailableDates);
            return () => {
                Socket.off('connect', establishConnection);
                Socket.off('appointments response', updateAppointments);
                Socket.off('users response', updateUsers);
                Socket.off('rooms response', updateRooms);
                Socket.off('unavailable dates response', updateUnavailableDates);
            };
        });
    }

    listenToServer();

    return (
        <div>
            <Calendar 
                onChange={onCalendarChanged}
                value={selectedDate}
                tileDisabled={isUnavailableDate}
                onActiveStartDateChange={onMonthChanged}
                showNeighboringMonth={false}
            />
            <LibrarianAppointmentsOverview appointments={appointments} />
            <LibrarianCheckIn
                inputRef={checkInRef}
                submitClick={onCheckInSubmitClicked}
                showResult={showCheckInResult}
                isSuccess={checkInSuccess}
            />
            <LibrarianUsersOverview users={users} />
            <LibrarianRoomsOverview rooms={rooms} />
        </div>
    );
}

import React, { useEffect, useState } from 'react';
import LibrarianCheckIn from './LibrarianCheckIn';
import LibrarianAppointmentsOverview from './LibrarianAppointmentsOverview';
import Socket from './Socket';

export default function LibrarianOverview() {
    const [appointments, setAppointments] = useState([]);
    const [checkInSuccess, setCheckInSuccess] = useState(true);
    const [showCheckInResult, setShowCheckInResult] = useState(false);
    const checkInResultDisplayTime = 5000;
    const checkInRef = React.createRef();

    function requestAllData() {
        Socket.emit('overview request', {});
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
    
    function updateAppointments(data) {
        setAppointments(
            oldAppointments => {
                let updatedAppointments = [];
                updatedAppointments.concat(oldAppointments);
                for (let newAppointment of data.appointments) {
                    let isNew = true;
                    for (let index in updatedAppointments) {
                        if (updatedAppointments[index].id == newAppointment.id) {
                            updatedAppointments[index] = newAppointment;
                            isNew = false;
                            break;
                        }
                    }
                    if (isNew) {
                        updatedAppointments.push(newAppointment);
                    }
                }
                return updatedAppointments;
            }
        );
    } 

    function listenToServer() {
        useEffect(() => {
            Socket.on('connect', establishConnection);
            Socket.on('appointments response', updateAppointments);
            return () => {
                Socket.off('connect', establishConnection);
                Socket.off('appointments response', updateAppointments);
            }
        });
    }

    listenToServer();

    return (
        <div>
            <LibrarianAppointmentsOverview appointments={appointments} />
            <h1>View/Edit Rooms: TODO</h1>
            <LibrarianCheckIn
                inputRef={checkInRef}
                submitClick={onCheckInSubmitClicked}
                showResult={showCheckInResult}
                isSuccess={checkInSuccess}
            />
            <h1>View/Edit Professor List: TODO</h1>
            <h1>View/Edit Calendar</h1>
        </div>
    );
}

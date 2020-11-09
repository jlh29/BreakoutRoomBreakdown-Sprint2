import React, { useState } from 'react';
import LibrarianCheckIn from './LibrarianCheckIn';
import Socket from './Socket';

export default function LibrarianOverview() {
    const [checkInSuccess, setCheckInSuccess] = useState(true);
    const [showCheckInResult, setShowCheckInResult] = useState(false);
    const checkInResultDisplayTime = 5000;
    const checkInRef = React.createRef();

    function updateCheckInSuccess(success) {
        setCheckInSuccess(success);
        setShowCheckInResult(true);
        setTimeout(() => setShowCheckInResult(false), checkInResultDisplayTime);
    }

    function onCheckInSubmitClicked() {
        let checkInID = checkInRef.current.value.strip();
        if (checkInID.length > 0) {
            Socket.emit('check in', {checkInID}, updateCheckInSuccess);
        }
        checkInRef.current.value = '';
    }

    return (
        <div>
            <h1>View/Edit Appointments: TODO</h1>
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

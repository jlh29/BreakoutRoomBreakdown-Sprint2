import React, { useState } from 'react';
import RoomReservationSelector from './RoomReservationSelector';
import RoomReservationAttendeeInput from './RoomReservationAttendeeInput';
import RoomReservationSubmit from './RoomReservationSubmit';

export function Content() {
    const [attendeeCount, setAttendeeCount] = useState(0);
    const [attendees, setAttendees] = useState([]);

    return (
        <div>
<<<<<<< HEAD
            <h1>Webauth Authentication Service</h1>
            <GoogleButton />
=======
>>>>>>> f1bc40127746f9e6a507187becbc2485b20d99ee
            <RoomReservationSelector setAttendeeCount={setAttendeeCount} />
            <RoomReservationAttendeeInput 
                attendeeCount={attendeeCount}
                setAttendees={setAttendees}
            />
            <RoomReservationSubmit />
        </div>
    );
}

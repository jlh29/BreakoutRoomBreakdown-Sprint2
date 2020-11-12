import React, { useState } from 'react';
import RoomReservationSelector from './RoomReservationSelector';
import RoomReservationAttendeeInput from './RoomReservationAttendeeInput';
import RoomReservationSubmit from './RoomReservationSubmit';

export function Content() {
    const [attendeeCount, setAttendeeCount] = useState(0);
    const [attendees, setAttendees] = useState([]);

    return (
        <div>
            <RoomReservationSelector setAttendeeCount={setAttendeeCount} />
            <RoomReservationAttendeeInput 
                attendeeCount={attendeeCount}
                setAttendees={setAttendees}
            />
            <RoomReservationSubmit />
        </div>
    );
}

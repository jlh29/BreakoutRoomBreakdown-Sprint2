import * as React from 'react';
import RoomReservation from './RoomReservation';
import RoomReservationSubmit from './RoomReservationSubmit';

export function Content() {
    return (
        <div>
            <h1>Webauth Authentication Service</h1>
            <GoogleButton />
            <RoomReservation />
            <RoomReservationSubmit />
        </div>
    );
}

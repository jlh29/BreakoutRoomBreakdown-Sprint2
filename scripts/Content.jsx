import * as React from 'react';
import RoomReservationSelector from './RoomReservationSelector';
import RoomReservationSubmit from './RoomReservationSubmit';

export function Content() {
    return (
        <div>
            <h1>Webauth Authentication Service</h1>
            <GoogleButton />
            <RoomReservationSelector />
            <RoomReservationSubmit />
        </div>
    );
}

import * as React from 'react';
import RoomReservation from './RoomReservation';
import RoomReservationSubmit from './RoomReservationSubmit';

export function Content() {
    return (
        <div>
            <RoomReservation />
            <RoomReservationSubmit />
        </div>
    );
}

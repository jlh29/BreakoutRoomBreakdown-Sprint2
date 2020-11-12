import * as React from 'react';
import RoomReservationSelector from './RoomReservationSelector';
import RoomReservationSubmit from './RoomReservationSubmit';

export function Content() {
    return (
        <div>
            <RoomReservationSelector />
            <RoomReservationSubmit />
        </div>
    );
}

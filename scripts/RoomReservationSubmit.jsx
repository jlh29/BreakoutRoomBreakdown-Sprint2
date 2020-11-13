import * as React from 'react';

export default function RoomReservationSubmit() {
    function handleSubmit(event) {
        event.preventDefault();
    }

    return (
        <button onClick={handleSubmit}>Submit</button>
    );
}

import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';

export default function ReservationConfirmation(props) {
    const { reservation, checkInCode } = props;
    const start_time = new Date(reservation.start_time);
    const end_time = new Date(reservation.end_time);

    function getTimeString(date) {
        return date.toLocaleTimeString(
            'en-US',
            {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: 'numeric',
                minute: '2-digit',
                second: '2-digit',
            },
        );
    }

    return (
        <div className='flexColumn'>
            <div id='reservationConfirmationContainer' className='flexColumn'>
                <h1>Reservation Details:</h1>
                <h3>Room: {reservation.room.room_number}</h3>
                <h3>Start Time: {getTimeString(start_time)}</h3>
                <h3>End Time: {getTimeString(end_time)}</h3>
                <h3>Attendees: {
                    reservation.attendees 
                    ? reservation.attendees.map(attendee => attendee.ucid).join(', ')
                    : 'None'}
                </h3>
                <h3>Check-in Code: {checkInCode}</h3>
            </div>
        </div>
    );
}

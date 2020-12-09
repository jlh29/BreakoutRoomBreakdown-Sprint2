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
    <div className="flexColumn">
      <div id="reservationConfirmationContainer" className="flexColumn">
        <img id="reservation-banner" src="./static/registration.png"/>
        <div id="reservation-summary">Reservation Summary</div>
        <p id="successBook">You have successfully completed your appointment!</p>
        <div>
          Room:
          <strong> {reservation.room.room_number}</strong>
        </div>
        <div>
          Start Time: 
          <strong> {getTimeString(start_time)}</strong>
        </div>
        <div>
          End Time: 
          <strong> {getTimeString(end_time)}</strong>
        </div>
        <div>
          Attendees:
          <strong>
           {
          reservation.attendees
            ? reservation.attendees.map((attendee) => attendee.ucid).join(', ')
            : 'None'
          }
          </strong>
        </div>
        <div>
          Check-in Code: 
          <strong> {checkInCode}</strong>
        </div>
        
        <p id="confirmText">You'll receive a confirmation email shortly.</p>
      </div>
    </div>
  );
}

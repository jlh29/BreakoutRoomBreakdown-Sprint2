import React, { useEffect } from 'react';

export default function RoomReservationTimeInfo(props) {
  const { selectedDate, selectedTime } = props;

  return (
    <div id="roomReservationTimeInfoContainer" className="flexColumn">
      <p id="roomReservationDateInfo">
        Reservation on
        {' '}
        <span id="reservationTime">{selectedDate ? selectedDate.toLocaleDateString('en-US') : '...'}</span>
      </p>
      <p id="roomReservationTimeInfo">
        at
        {' '}
        <span id="reservationDate">{selectedTime || '...'}</span>
      </p>
    </div>
  );
}

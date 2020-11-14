import React, { useEffect } from 'react';

export default function RoomReservationTimeInfo(props) {
  const { selectedDate, selectedTime } = props;

  return (
    <div id="roomReservationTimeInfoContainer" className="flexColumn">
      <p id="roomReservationDateInfo">
        Reservation
        on
        {' '}
        {selectedDate ? selectedDate.toLocaleDateString('en-US') : '...'}
      </p>
      <br />
      <p id="roomReservationTimeInfo">
        at
        {' '}
        {selectedTime || '...'}
      </p>
    </div>
  );
}

import * as React from 'react';

export default function RoomReservationSubmit(props) {
  const { handleSubmit } = props;

  return (
    <button onClick={handleSubmit} id="reservationSubmit">Submit</button>
  );
}

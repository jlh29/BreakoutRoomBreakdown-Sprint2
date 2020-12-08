import React from 'react';

export default function Slot(props) {
  const {
    isAvailable, setTime, timeslot, availableRooms,
  } = props;

  function handleClick() {
    setTime(timeslot);
  }

  if (isAvailable) {
    return (
      <button
        className="timeslot-btn"
        type="button"
        onClick={handleClick}
      >
        {timeslot}
        {' '}
        (
        {availableRooms}
        )
      </button>
    );
  }

  return (
    <button
      className="timeslot-btn"
      type="button"
      disabled
    >
      {timeslot}
      {' '}
      (
      {availableRooms}
      )
    </button>
  );
}

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

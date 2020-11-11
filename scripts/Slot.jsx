import React from 'react';

export function Slot(props) {
  const [time, setTime] = React.useState();

  function handleClick(event) {
    setTime(props.timeslot);
  }
  
  console.log(time);

  return (
    <button type="button" onClick={handleClick} timeslot={time}>{props.timeslot}</button>
  );
}

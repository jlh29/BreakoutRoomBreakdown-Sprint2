import React from 'react';

export default function Slot(props) {
  const { isAvailable, setTime, timeslot } = props;

  function handleClick() {
    setTime(timeslot);
  }

  if (isAvailable){
    return <button type="button" onClick={handleClick}>{timeslot}</button>;
  }
  else{
    return <button type="button" onClick={handleClick} disabled>{timeslot}</button>;
  }
}

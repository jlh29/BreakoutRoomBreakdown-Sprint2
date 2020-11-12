import React from 'react';
import Socket from './Socket';

export function Slot(props) {
  const [time, setTime] = React.useState();
  const [isAvailable, setIsAvailable] = React.useState(false);
  
  // if date is available, display the timeslot
  function dateStatus() {
    React.useEffect(() => {
      Socket.on('date status', (data) => {
            setIsAvailable(data['is_available']);
        });
    });
  }
  
  // console.log(time);
  
  function handleClick(event) {
    setTime(props.timeslot);
  }
  
  dateStatus();

    
  if (isAvailable){
    return <button type="button" onClick={handleClick} timeslot={time}>{props.timeslot}</button>;
  }
  else{
    return <button type="button" onClick={handleClick} timeslot={time} disabled>{props.timeslot}</button>;
  }

}

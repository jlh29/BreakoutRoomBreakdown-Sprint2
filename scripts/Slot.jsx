import React from 'react';
import Socket from './Socket';

export function Slot(props) {
  const [time, setTime] = React.useState();
  const [isAvailable, setIsAvailable] = React.useState(false);
  
  function dateStatus() {
      React.useEffect(() => {
        Socket.on('date status', (data) => {
              setIsAvailable(data['is_available']);
          });
      });
  }
  
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

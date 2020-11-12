import React from 'react';
import Socket from './Socket';

export function Slot(props) {
  const [time, setTime] = React.useState();
  const [isAvailable, setIsAvailable] = React.useState(false);
  const [timeAvailable, setTimeAvailable] = React.useState("");
  const [send, setSend] = React.useState(false);
  
  // if date is available, display the timeslot
  function dateStatus() {
    React.useEffect(() => {
      Socket.on('date status', (data) => {
            setIsAvailable(data['is_available']);
            setTimeAvailable(data['time available']);
        });
    });
  }
  
  dateStatus();
  
  // send clicked time
  function sendTime(){
    console.log(`User selected the time "${time}"`);

    Socket.emit('time availability', { 
        'time': time
    });
    
    console.log(`Sent the date "${time}" to the server`);  
  }
  
  function handleClick() {
    setTime(props.timeslot);
    setSend(true);
  }
  
  if (send)
    sendTime();
  

  if (isAvailable){
      return <button type="button" onClick={handleClick} timeslot={time}>{props.timeslot}</button>;
    }
  else{
      return <button type="button" onClick={handleClick} timeslot={time} disabled>{props.timeslot}</button>;
    }
}

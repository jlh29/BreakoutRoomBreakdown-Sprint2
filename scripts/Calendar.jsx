import React from 'react';
import Socket from './Socket';
import Calendar from 'react-calendar';
import { Slot } from './Slot';

export function MyCalendar() {
    const [date, setDate] = React.useState(new Date());
    
    function sendDate(){
        console.log(`User selected the date "${date}"`);
    
        Socket.emit('date availability', { 
            'date': date
        });
        
        console.log(`Sent the date "${date}" to the server`);  
    }
  
    function handleClickDay(event){
        setDate(event);
    }
    
    sendDate();
    
    function handleDisable(){
       ({activeStartDate, date, view }) => date.getDay() === 6;
    }

    return (
        <div>
          <Calendar
            tileDisabled={handleDisable}
            onClickDay={handleClickDay}
            value={date}
          />
          <Slot timeslot="9:00-11:00"></Slot>
          <Slot timeslot="11:00-1:00"></Slot>
          <Slot timeslot="1:00-3:00"></Slot>
          <Slot timeslot="3:00-5:00"></Slot>
        </div>
      );
}
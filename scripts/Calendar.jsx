import React, { useState } from 'react';
import Socket from './Socket';
import Calendar from 'react-calendar';
import Slot from './Slot';

export default function MyCalendar() {
    const [date, setDate] = useState(new Date());
    
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
    
    function handleDisable({activeStartDate, date, view }){
        let disableDate = false;
        let today = new Date();
        
        if (date.getDay() === 0 || date.getDay() === 6)
            disableDate = true;
            
        if (date.getDate() === 24)
            disableDate = true;
            
        // date.getDate() !== today.getDate() 
        if (date.getDate() !== today.getDate() + 1
            && date.getDate() !== today.getDate() + 2)
            disableDate = true;
            
        return disableDate;
    }
    

    return (
        <div>
            <Calendar
                onClickDay={handleClickDay}
                value={date}
                tileDisabled={handleDisable}
            />
            <Slot timeslot="9:00-11:00"></Slot>
            <Slot timeslot="11:00-1:00"></Slot>
            <Slot timeslot="1:00-3:00"></Slot>
            <Slot timeslot="3:00-5:00"></Slot>
        </div>
      );
}
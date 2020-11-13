import React, { useState } from 'react';
import Socket from './Socket';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import Slot from './Slot';

export default function MyCalendar(props) {
    const { date, setDate } = props;
    const { time, setTime } = props;
    
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
            <Slot timeslot="9:00-11:00" time={time} setTime={setTime}></Slot>
            <Slot timeslot="11:00-1:00" time={time} setTime={setTime}></Slot>
            <Slot timeslot="1:00-3:00" time={time} setTime={setTime}></Slot>
            <Slot timeslot="3:00-5:00" time={time} setTime={setTime}></Slot>
        </div>
      );
}
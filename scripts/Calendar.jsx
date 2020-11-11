import React from 'react';
import Calendar from 'react-calendar';
import { Slot } from './Slot';

export function MyCalendar() {
    const [date, setDate] = React.useState(new Date());
  
    function handleClickDay(event){
        setDate(event);
    }
    console.log(date);

    return (
        <div>
          <Calendar
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
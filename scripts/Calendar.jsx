import React from 'react';
import Calendar from 'react-calendar';

export function MyCalendar() {
    const [date, setDate] = React.useState(new Date());
  
    function handleChange(event){
        setDate(event);
    }
    console.log(date);

    return (
        <div>
          <Calendar
            onClickDay={handleChange}
            value={date}
          />
        </div>
      );
}
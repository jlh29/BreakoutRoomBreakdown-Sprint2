import React, { useState } from 'react';
import Calendar from 'react-calendar';
import Socket from './Socket';
import 'react-calendar/dist/Calendar.css';
import Slot from './Slot';

import { differenceInCalendarDays } from 'date-fns';
import { isWithinInterval } from "date-fns";

export default function MyCalendar(props) {
  const {
    date, setDate, time, setTime, allTimes, availableDates,
  } = props;
  
  let x = new Date("2020-12-18");
  let y = new Date("2020-12-2");
  let z = new Date("2020-12-3");
  
  let a = new Date("2020-12-18");
  let b = new Date("2020-12-2");
  let c = new Date("2020-12-5");
  let d = new Date("2020-12-29");
  
  const disabledDates = [x];
  const disabledRanges = [
    [y,z],
  ];
  
  const markDates = [a,d];
  const markRanges = [
    [b,c], 
  ];

  function handleClickDay(event) {
    setDate(event);
  }
  
  function isSameDay(a, b) {
    return differenceInCalendarDays(a, b) === 0;
  }
  
  function isWithinRange(date, range) {
    return isWithinInterval(date, { start: range[0], end: range[1] });
  }
  
  function isWithinRanges(date, ranges) {
    return ranges.some(range => isWithinRange(date, range));
  }

  function handleDisable({ activeStartDate, date, view }) {
    let disableDate = false;
    const today = new Date();
    
    for (const available of availableDates) {
      if (date.getUTCDate() == available.getUTCDate()
                    && date.getUTCMonth() == available.getUTCMonth()
                    && date.getUTCFullYear() == available.getUTCFullYear()) {
        disableDate = false;
        break;
      }
    }
   
    if (date.getDay() === 0 || date.getDay() === 6) {
      disableDate = true;
    }

    if (date.getUTCDate() < today.getUTCDate()) {
      disableDate = true;
    }
    
  if (date.getUTCDate() - today.getUTCDate() > 2) {
      disableDate = true;
    }
    
    if (view === 'month' && isWithinRanges(date, disabledRanges)){
      disableDate = true;
    }
    
    if (view === 'month' && disabledDates.find(dDate => isSameDay(dDate, date))) {
      disableDate = true;
    }
    
    return disableDate;
    
  }
  
  function handleContent({ activeStartDate, date, view }){
    
    if (isWithinRanges(date, markRanges)) {
      return <p>Long weekend</p>;
    }
    
    if (markDates.find(dDate => isSameDay(dDate, date))){
      return <p>X</p>;
    }
    
  }

  return (
    <div id="calendar" className="flexColumn">
      <Calendar
        onClickDay={handleClickDay}
        value={date}
        tileDisabled={handleDisable}
        tileContent={handleContent}
      />
      <div id="timeButtonsContainer">
        {
                    allTimes.map(
                      (time) => (
                        <Slot
                          timeslot={time.timeslot}
                          setTime={setTime}
                          isAvailable={time.isAvailable}
                          availableRooms={time.availableRooms}
                          key={time.timeslot}
                        />
                      ),
                    )
                }
      </div>
    </div>
  );
}

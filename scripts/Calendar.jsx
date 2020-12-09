import React, { useState } from 'react';
import Calendar from 'react-calendar';
import Socket from './Socket';
import 'react-calendar/dist/Calendar.css';
import Slot from './Slot';

import { isWithinInterval } from "date-fns";

export default function MyCalendar(props) {
  const {
    date, setDate, time, setTime, allTimes, availableDates,
  } = props;
  const [disabledDates, setDisabledDates] = useState([]);
  const [notes, setNotes] = useState([]);
  let newDateRange = [];
  
  function getNewDates() {
    React.useEffect(() => {
      Socket.on('disable channel', (data) => {
          console.log("Received dates from server: " + data['date range']);
          console.log("Received notes from server: " + data['note']);
  
          setDisabledDates(data['date range']);
          setNotes(data['note']);
      });
    });
  }
  
  function getDateRange(){
    for (let i=0; i<disabledDates.length; i++){
      newDateRange.push([new Date(disabledDates[i][0]), new Date(disabledDates[i][1])]);
    }
  }

  getNewDates();
  
  if (disabledDates.length !== 0){
    getDateRange();
  }

  function handleClickDay(event) {
    setDate(event);
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
    
    if (view === 'month' && isWithinRanges(date, newDateRange)){
      disableDate = true;
    }
    
    return disableDate;
  }

  function handleContent({ date, view }){
    for (let i=0; i<disabledDates.length; i++){
      if (isWithinRange(date, newDateRange[i])) {
        return <p>{notes[i]}</p>;
      }
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

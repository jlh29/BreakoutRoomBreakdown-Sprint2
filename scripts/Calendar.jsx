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
  
  function updateDisabledDates(data) {
    const disabled = [];
    Object.values(data.dates).forEach(
      (dateObj) => {
        disabled.push({
          date: new Date(dateObj.date),
          note: dateObj.note,
        });
      },
    );
    setDisabledDates(disabled);
  }

  function getNewDates() {
    React.useEffect(() => {
      Socket.on('disable channel', updateDisabledDates);
      return () => {
        Socket.off('disable channel', updateDisabledDates);
      }
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
    let disableDate = true;
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
    
    return disableDate;
  }

  function handleContent({ date, view }){
    for (let i=0; i<disabledDates.length; i++){
      let disabled = disabledDates[i];
      if (date.getUTCDate() == disabled.date.getUTCDate()
                    && date.getUTCMonth() == disabled.date.getUTCMonth()
                    && date.getUTCFullYear() == disabled.date.getUTCFullYear()) {
        return <p>{disabled.note}</p>;
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
        <p id="availableTimesText">Available Times</p>
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

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
  const [disabledDates, setDisabledDates] = useState([]);
  const [markDates, setMarkDates] = useState([]);
  
  const [startDates, setStartDates] = useState([]);
  const [endDates, setEndDates] = useState([]);
  const [notes, setNotes] = useState([]);
  
  // let x = new Date("2020-12-18");
  // let y = new Date("2020-12-2");
  // let z = new Date("2020-12-3");
  
  // let a = new Date("2020-12-2");
  // let b = new Date("2020-12-3");
  // let c = new Date("2020-12-5");
  // let d = new Date("2020-12-7");
  
  // let lst1 = ['a', 'b', 'c'];
  // let lst2 = ['x', 'y', 'z'];
  
  // let arr = [];
  for (let i=0; i<startDates.length; i++)
    setMarkDates([startDates[i], endDates[i]]);
  
  console.log(markDates)
  
  // const disabledDates = [x];
  // const disabledRanges = [[z,z]];
  
  // const markDates = [a];
  // const markRanges = [
  //   [a,b], [c,d]
  // ];
  

  
  function getNewDates() {
    console.log("GET NEW DATES")
    React.useEffect(() => {
      Socket.on('disable channel', (data) => {
          console.log("Received addresses from server: " + data['start date']);
          console.log("Received addresses from server: " + data['end date']);
          console.log("Received addresses from server: " + data['note']);
          setStartDates(data['start date']);
          setEndDates(data['end date']);
          setNotes(data['note']);
      });
    });
  }

  getNewDates();

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
    
    if (view === 'month' && isWithinRanges(date, disabledDates)){
      disableDate = true;
    }
    
    return disableDate;
  }
  
  // let q = new Date("2020-12-15");
  // let w = new Date("2020-12-17");
  // let markings = ['TEST4', 'TEST5'];
  // let marking = "TEST2";
  // const mk = [
  //   [q,w]
  // ];
  
  // let t =  [q,w]
  
  function handleContent({ date, view }){
    for (let i=0; i<startDates.length; i++){
      if (isWithinRange(date, markDates[i])) {
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

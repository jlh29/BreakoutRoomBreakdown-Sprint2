import React, { useState } from 'react';
import Calendar from 'react-calendar';
import Socket from './Socket';
import 'react-calendar/dist/Calendar.css';
import Slot from './Slot';

export default function MyCalendar(props) {
  const {
    date, setDate, time, setTime, allTimes, availableDates,
  } = props;

  function handleClickDay(event) {
    setDate(event);
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

  return (
    <div id="calendar" className="flexColumn">
      <Calendar
        onClickDay={handleClickDay}
        value={date}
        tileDisabled={handleDisable}
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

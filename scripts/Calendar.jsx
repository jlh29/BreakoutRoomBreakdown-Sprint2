import React, { useState } from 'react';
import Socket from './Socket';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import Slot from './Slot';

export default function MyCalendar(props) {
    const { date, setDate, time, setTime, allTimes, availableDates } = props;
  
    function handleClickDay(event){
        setDate(event);
    }

    function handleDisable({activeStartDate, date, view }){
        let disableDate = true;
        let today = new Date();
        for (let available of availableDates) {
            if (date.getDate() == available.getDate()
                    && date.getMonth() == available.getMonth()
                    && date.getFullYear() == available.getFullYear()) {
                disableDate = false;
                break;
            }
        }

        if (date.getDay() === 0 || date.getDay() === 6) {
            disableDate = true;
        }

        if (date.getDate() < today.getDate()) {
            disableDate = true;
        }

        if (date.getDate() - today.getDate() > 2) {
            disableDate = true;
        }

        return disableDate;
    }

    return (
        <div>
            <Calendar
                onClickDay={handleClickDay}
                value={date}
                tileDisabled={handleDisable}
            />
            {
                allTimes.map(
                    time => {
                        return <Slot
                            timeslot={time.timeslot}
                            setTime={setTime}
                            isAvailable={time.isAvailable}
                        />;
                    }
                )
            }
        </div>
      );
}
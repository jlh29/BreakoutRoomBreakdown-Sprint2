import React, { useEffect } from 'react';

export default function RoomReservationAttendeeInput(props) {
    const { attendeeCount, setAttendees } = props;

    function updateAttendees() {
        let allInputs = document.getElementsByClassName('attendeeInput');
        let allAttendees = [];
        for (let input of allInputs) {
            let trimmedInput = input.value.trim();
            if (trimmedInput.length > 0) {
                // TODO: jlh29, don't add duplicates, but for MVP it's okay
                allAttendees.push(trimmedInput);
            }
        }
        setAttendees(allAttendees);
    }

    useEffect(() => updateAttendees(), [attendeeCount]);

    return (
        <div id='attendeeInputContainer'>
            {
                attendeeCount > 0 ?
                    [...Array(attendeeCount - 1).keys()].map(
                        index => {
                            return (
                                <input
                                    type='text'
                                    placeholder='Attendee UCID'
                                    key={index}
                                    className='attendeeInput'
                                    onChange={updateAttendees}
                                ></input>
                            );
                        }
                    )
                :
                null
            }
        </div>
    );
}

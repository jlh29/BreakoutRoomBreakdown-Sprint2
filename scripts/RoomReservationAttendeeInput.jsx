import React, { useEffect } from 'react';

export default function RoomReservationAttendeeInput(props) {
  const { attendeeCount, setAttendees } = props;

  function updateAttendees() {
    const allInputs = document.getElementsByClassName('attendeeInput');
    const allAttendees = [];
    for (const input of allInputs) {
      const trimmedInput = input.value.trim();
      if (trimmedInput.length > 0) {
        // TODO: jlh29, don't add duplicates, but for MVP it's okay
        allAttendees.push(trimmedInput);
      }
    }
    setAttendees(allAttendees);
  }

  useEffect(() => updateAttendees(), [attendeeCount]);

  return (
    <div id="attendeeInputContainer" className="flexColumn">
      {
                attendeeCount > 0
                  ? [...Array(attendeeCount - 1).keys()].map(
                    (index) => (
                      <input
                        type="text"
                        placeholder="Attendee UCID"
                        key={index}
                        className="attendeeInput"
                        onChange={updateAttendees}
                      />
                    ),
                  )
                  : null
            }
    </div>
  );
}

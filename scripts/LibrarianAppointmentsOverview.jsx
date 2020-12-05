import React, { useState } from 'react';
import LibrarianAppointmentsOverviewItem from './LibrarianAppointmentsOverviewItem';
import LibrarianEditButtonBar from './LibrarianEditButtonBar';

export default function LibrarianAppointmentsOverview(props) {
  const { appointments, selectedAppointment, setSelectedAppointment } = props;
  const [isEditing, setIsEditing] = useState(false);

  function enableEditing() {
      setIsEditing(true);
  }

  function disableEditing() {
      setIsEditing(false);
  }

  function changeSelectedAppointment(newAppointment) {
    setSelectedAppointment(newAppointment);
    disableEditing();
  }

  return (
    <div id="appointmentsContainer" className="menuContainer">
      <div id="appointmentsSelector" className="menuSelector">
        {
                    appointments.map(
                      (appointment) => (
                        <button
                          className="menuSelectorButton"
                          type="button"
                          onClick={() => changeSelectedAppointment(appointment)}
                          key={appointment.id}
                        >
                          Room:
                          {' '}
                          {appointment.room.room_number}
                        </button>
                      ),
                    )
                }
      </div>
      <div id="appointmentDetails" className="menuContents">
        {('id' in selectedAppointment)
          ? (
            <div>
              <LibrarianAppointmentsOverviewItem
                appointment={selectedAppointment}
                isEditing={isEditing}
              />
              <LibrarianEditButtonBar
                isEditing={isEditing}
                enableEditing={enableEditing}
                disableEditing={disableEditing}
              />
            </div>
          )
          : null}
      </div>
    </div>
  );
}

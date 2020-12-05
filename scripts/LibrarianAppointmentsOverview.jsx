import React, { useState } from 'react';
import PropTypes from 'prop-types';
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

  function onConfirmClick() {
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
        {(selectedAppointment.id > 1)
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
                onConfirmClick={onConfirmClick}
              />
            </div>
          )
          : null}
      </div>
    </div>
  );
}

LibrarianAppointmentsOverview.propTypes = {
  appointments: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      organizer: PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        ucid: PropTypes.string.isRequired,
        role: PropTypes.string.isRequired,
      }).isRequired,
      attendees: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.number.isRequired,
          ucid: PropTypes.string.isRequired,
        }),
      ).isRequired,
      room: PropTypes.shape({
        id: PropTypes.number.isRequired,
        room_number: PropTypes.oneOfType([
          PropTypes.string,
          PropTypes.number,
        ]).isRequired,
        size: PropTypes.string.isRequired,
        capacity: PropTypes.number.isRequired,
      }).isRequired,
      start_time: PropTypes.number.isRequired,
      end_time: PropTypes.number.isRequired,
      status: PropTypes.string.isRequired,
    }),
  ).isRequired,
  selectedAppointment: PropTypes.oneOfType([
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      organizer: PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        ucid: PropTypes.string.isRequired,
        role: PropTypes.string.isRequired,
      }).isRequired,
      attendees: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.number.isRequired,
          ucid: PropTypes.string.isRequired,
        }),
      ).isRequired,
      room: PropTypes.shape({
        id: PropTypes.number.isRequired,
        room_number: PropTypes.oneOfType([
          PropTypes.string,
          PropTypes.number,
        ]).isRequired,
        size: PropTypes.string.isRequired,
        capacity: PropTypes.number.isRequired,
      }).isRequired,
      start_time: PropTypes.number.isRequired,
      end_time: PropTypes.number.isRequired,
      status: PropTypes.string.isRequired,
    }),
    PropTypes.shape({}),
  ]).isRequired,
  setSelectedAppointment: PropTypes.func.isRequired,
};

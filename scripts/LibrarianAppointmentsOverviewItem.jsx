import * as React from 'react';
import PropTypes from 'prop-types';

export default function LibrarianAppointmentsOverviewItem(props) {
  const { appointment, isEditing } = props;

  function getDateString(timestamp) {
    const utcTs = new Date(timestamp);
    return utcTs.toLocaleDateString(
      'en-US',
      { hour: 'numeric', minute: '2-digit' },
    );
  }

  return (
    <div className="appointment">
      <p>
        Status:
        {' '}
        {appointment.status}
      </p>
      <p>
        Organizer:
        {' '}
        {appointment.organizer.name}
        {' '}
        (
        {appointment.organizer.ucid}
        )
      </p>

      <p>
        Attendees:
        {' '}
        {
                appointment.attendees
                  ? `\n\t${
                    appointment.attendees.map(
                      (attendee) => `${attendee.ucid}`,
                    ).join('\n\t')}`
                  : 'None'
            }
      </p>
      <p>
        Room Number:
        {' '}
        {appointment.room.room_number}
      </p>
      <p>
        Start Time:
        {' '}
        {getDateString(appointment.start_time)}
      </p>
      <p>
        End Time:
        {' '}
        {getDateString(appointment.end_time)}
      </p>
    </div>
  );
}

LibrarianAppointmentsOverviewItem.propTypes = {
  appointment: PropTypes.shape({
    id: PropTypes.number.isRequired,
    organizer: PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      ucid: PropTypes.string.isRequired,
      role: PropTypes.string.isRequired,
    }).isRequired,
    attendees: PropTypes.arrayOf(PropTypes.string).isRequired,
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
  }).isRequired,
  isEditing: PropTypes.bool.isRequired,
};

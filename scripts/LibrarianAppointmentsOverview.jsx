import React, { useState } from 'react';
import LibrarianAppointmentsOverviewItem from './LibrarianAppointmentsOverviewItem';

export default function LibrarianAppointmentsOverview(props) {
    const { appointments } = props;
    const [selectedAppointment, setSelectedAppointment] = useState({});

    return (
        <div id='appointmentsContainer'>
            <div id='appointmentsSelector'>
                { 
                    appointments.map(
                        appointment => (
                            <button 
                                className='appointmentSelectorButton'
                                type='button'
                                onClick={() => setSelectedAppointment(appointment)}
                                key={appointment.id}
                            >
                                Room: {appointment.room.room_number}
                            </button>
                        )
                    )
                }
            </div>
            <div id='appointmentDetails'>
                {('id' in selectedAppointment) ? 
                    <LibrarianAppointmentsOverviewItem
                        appointment={selectedAppointment}
                    />
                    :
                    null
                }
            </div>
        </div>
    );
}

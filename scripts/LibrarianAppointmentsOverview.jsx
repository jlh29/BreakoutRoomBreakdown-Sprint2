import * as React from 'react';
import LibrarianAppointmentsOverviewItem from './LibrarianAppointmentsOverviewItem';

export default function LibrarianAppointmentsOverview(props) {
    const { appointments } = props;
    return (
        <div id='appointmentsContainer'>
            <ul id='appointmentsList'>
                {
                    appointments.map(
                        appointment => <LibrarianAppointmentsOverviewItem
                            appointment={appointment}
                            key={appointment.id}
                        />
                    )
                }
            </ul>
        </div>
    );
}

import * as React from 'react';

export default function RoomReservationSelector() {
    const minAttendeeCount = 2;
    const maxAttendeeCount = 12;

    return (
        <div>
            <label htmlFor="studentCount">How Many Students (Including You)?</label>
            <select name="studentCount" id="studentCount" defaultValue="-">
                <option disabled hidden value="0"> - </option>
                {
                    [...Array(maxAttendeeCount - minAttendeeCount + 1).keys()].map(
                        index => {
                            let value = index + minAttendeeCount;
                            return <option value={value}>{value}</option>;
                        }
                    )
                }
            </select>
        </div>
    );
}

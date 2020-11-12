import * as React from 'react';

export default function RoomReservationSelector() {
    const minReservationCount = 2;
    const maxReservationCount = 12;

    return (
        <div>
            <label htmlFor="studentCount">How Many Students (Including You)?</label>
            <select name="studentCount" id="studentCount" defaultValue="-">
                <option disabled hidden value="-"> - </option>
                {
                    [...Array(maxReservationCount-minReservationCount+1).keys()].map(
                        index => {
                            let value = index + minReservationCount;
                            return <option value={value}>{value}</option>;
                        }
                    )
                }
            </select>
        </div>
    );
}

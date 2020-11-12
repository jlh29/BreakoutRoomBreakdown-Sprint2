import * as React from 'react';

export default function RoomReservationSelector(props) {
    const minAttendeeCount = 2;
    const maxAttendeeCount = 12;
    const { setAttendeeCount } = props;

    function updateAttendeeCount(event) {
        setAttendeeCount(parseInt(event.target.value));
    }

    return (
        <div>
            <label htmlFor="studentCount">How Many Students (Including You)?</label>
            <select
                name="studentCount"
                id="studentCount"
                defaultValue="0"
                onChange={updateAttendeeCount}
            >
                <option disabled hidden value="0"> - </option>
                {
                    [...Array(maxAttendeeCount - minAttendeeCount + 1).keys()].map(
                        index => {
                            let value = index + minAttendeeCount;
                            return <option value={value} key={value}>{value}</option>;
                        }
                    )
                }
            </select>
        </div>
    );
}

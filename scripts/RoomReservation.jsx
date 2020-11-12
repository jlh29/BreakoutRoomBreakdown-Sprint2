import * as React from 'react';
import Socket from './Socket';

export function RoomReservation() {
    function getStudentCount() {
        React.useEffect(() => {
            });
    }
    
    
    return (
        <div>
            <label htmlFor="studentCount">How Many Students (Including You)?</label>
            <select name="studentCount" id="studentCount">
                <option selected disabled hidden value> - </option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
                <option value="11">11</option>
                <option value="12">12</option>
            </select>
        </div>
    );
}

import * as React from 'react';

export default function ReservationUsersNumber(props) {

    return(
        <div>
            <label>Mobile number: </label>
            <input 
            type="tel" 
            id="mobileNumber"
            name="number"
            placeholder="2014448888"
            maxLength="10"
            pattern="[0-9]{3}[0-9]{3}[0-9]{4}"
            required/>
        </div>
    );
}
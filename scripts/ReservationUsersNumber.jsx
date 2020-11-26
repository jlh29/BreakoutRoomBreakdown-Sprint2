import * as React from 'react';

export default function ReservationUsersNumber() {
    const [number, setNumber] = React.useState();
    
    function handleChange(event){
        setNumber(event.target.value);
    }
    
    return(
        <div>
            <label>Mobile number: </label>
            <input 
            type="tel" 
            id="number"
            name="number"
            placeholder="2012345678"
            maxlength="10"
            pattern="[0-9]{3}[0-9]{3}[0-9]{4}"
            onChange={handleChange}
            required/>
        </div>
    );
}
import * as React from 'react';
import Socket from './Socket';

export function Submit() {
    function handleSubmit(event) {
        
        event.preventDefault();
    }

    return (
        <button onClick={handleSubmit}>Submit</button>
    );
}

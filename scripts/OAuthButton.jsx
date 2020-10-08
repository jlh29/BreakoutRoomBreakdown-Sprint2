import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let newAddress = document.getElementById("address_input");
    Socket.emit('new address input', {
        'address': newAddress.value,
    });
    
    console.log('Sent the address ' + newAddress.value + ' to server!');
    newAddress.value = ''
    
    event.preventDefault();
}

export function OAuthButton() {
    return (
            <button>Replace me!</button>
    );
}

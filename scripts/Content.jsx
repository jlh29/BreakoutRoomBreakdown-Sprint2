import * as React from 'react';
import Parser from 'html-react-parser';

import { RoomReservation } from './RoomReservation';
import { Submit } from './Submit';

export function Content() {
    return (
        <div>
            <h1>Webauth Authentication Service</h1>
            <GoogleButton />
            <RoomReservation />
            <Submit />
        </div>
    );
}

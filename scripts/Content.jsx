import * as React from 'react';
import Parser from 'html-react-parser';

import { GoogleButton } from './GoogleButton';
import { RoomReservation } from './RoomReservation';
import { Submit } from './Submit';

export function Content() {
    return (
        <div>
            <RoomReservation />
            <Submit />
        </div>
    );
}

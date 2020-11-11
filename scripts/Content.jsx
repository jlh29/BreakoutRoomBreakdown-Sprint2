import * as React from 'react';

import { GoogleButton } from './GoogleButton';
import { MyCalendar } from './Calendar';

export function Content() {
    return (
        <div>
            <h1>Log in with OAuth!</h1>
            <MyCalendar />
        </div>
    );
}

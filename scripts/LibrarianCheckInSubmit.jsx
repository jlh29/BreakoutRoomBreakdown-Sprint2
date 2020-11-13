import * as React from 'react';

export default function LibrarianCheckInSubmit(props) {
    const { submitClick } = props;
    return <button type='text' onClick={submitClick}>Check-in</button>;
}

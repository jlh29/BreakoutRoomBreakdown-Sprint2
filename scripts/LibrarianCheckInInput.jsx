import * as React from 'react';

export default function LibrarianCheckInInput(props) {
    const { inputRef } = props;
    return <input type='text' ref={inputRef}>Check-in ID:</input>;
}

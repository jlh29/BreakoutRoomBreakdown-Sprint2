import * as React from 'react';
import LibrarianCheckInInput from './LibrarianCheckInInput';
import LibrarianCheckInSubmit from './LibrarianCheckInSubmit';

export default function LibrarianCheckIn(props) {
    const { inputRef, submitClick } = props;
    return (
        <div>
            <LibrarianCheckInInput inputRef={inputRef} />
            <LibrarianCheckInSubmit submitClick={submitClick} />
        </div>
    );
}

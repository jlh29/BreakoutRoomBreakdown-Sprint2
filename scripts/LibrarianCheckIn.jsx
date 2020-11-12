import * as React from 'react';
import LibrarianCheckInInput from './LibrarianCheckInInput';
import LibrarianCheckInSubmit from './LibrarianCheckInSubmit';
import LibrarianCheckInResult from './LibrarianCheckInResult';

export default function LibrarianCheckIn(props) {
    const { inputRef, submitClick, showResult, isSuccess } = props;
    return (
        <div id='librarianCheckInContainer'>
            <LibrarianCheckInInput inputRef={inputRef} />
            <LibrarianCheckInSubmit submitClick={submitClick} />
            {showResult ? <LibrarianCheckInResult isSuccess={isSuccess} /> : null}
        </div>
    );
}

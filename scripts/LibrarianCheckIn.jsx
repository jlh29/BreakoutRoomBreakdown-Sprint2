import * as React from 'react';
import LibrarianCheckInInput from './LibrarianCheckInInput';
import LibrarianCheckInSubmit from './LibrarianCheckInSubmit';
import LibrarianCheckInResult from './LibrarianCheckInResult';

export default function LibrarianCheckIn(props) {
    const { inputRef, submitClick, showResult, isSuccess } = props;
    return (
        <div id='librarianCheckInContainer'  className='flexColumn'>
            <div id='librarianCheckInInputContainer'>
                <LibrarianCheckInInput inputRef={inputRef} />
                <LibrarianCheckInSubmit submitClick={submitClick} />
            </div>
            <div id='librarianCheckInOutput'>
                {showResult ? <LibrarianCheckInResult isSuccess={isSuccess} /> : null}
            </div>
        </div>
    );
}

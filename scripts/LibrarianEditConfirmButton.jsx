import React, { useState } from 'react';

export default function LibrarianEditConfirmButton(props) {
    const { onConfirmClick } = props;
    const [mustConfirm, setMustConfirm] = useState(true);
    
    function updateMustConfirm() {
        setMustConfirm(true);
    }
    
    if (mustConfirm) {
        return (
            <button
                type='button'
                className='librarianEditSaveButton'
                onClick={updateMustConfirm}
            >Save Changes</button>
        );
    } else {
        return (
            <button
                type='button'
                className='librarianEditConfirmButton'
                onClick={onConfirmClick}
            >Confirm Changes</button>
        );
    }
}
import React, { useState } from 'react';

export default function LibrarianEditCancelButton(props) {
    const { onCancelClick } = props;
    
    return (
        <button
            type='button'
            className='librarianEditCancelButton'
            onClick={onCancelClick}
        >Discard Changes</button>
    );
}
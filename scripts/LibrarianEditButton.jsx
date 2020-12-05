import React from 'react';

export default function LibrarianEditButton(props) {
    const { onEditClick } = props;
    
    return (
        <button
            type='button'
            className='librarianEditButton'
            onClick={onEditClick}
        >Edit</button>
    );
}
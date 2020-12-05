import React, { useState } from 'react';
import LibrarianEditConfirmButton from './LibrarianEditConfirmButton';
import LibrarianEditCancelButton from './LibrarianEditCancelButton';
import LibrarianEditButton from './LibrarianEditButton';

export default function LibrarianEditButtonBar(props) {
    const {
        onConfirmClick,
        onCancelClick,
        isEditing,
        enableEditing,
        disableEditing,
    } = props;
    
    if (isEditing) {
        return (
            <div className='librarianEditButtonBar'>
                <LibrarianEditConfirmButton onConfirmClick={onConfirmClick} />
                <LibrarianEditCancelButton onCancelClick={disableEditing} />
            </div>
        );
    } else {
        return (
            <div className='librarianEditButtonBar'>
                <LibrarianEditButton onEditClick={enableEditing} />
            </div>
        );
    }
}
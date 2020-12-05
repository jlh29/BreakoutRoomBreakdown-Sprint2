import React from 'react';
import PropTypes from 'prop-types';
import LibrarianEditConfirmButton from './LibrarianEditConfirmButton';
import LibrarianEditCancelButton from './LibrarianEditCancelButton';
import LibrarianEditButton from './LibrarianEditButton';

export default function LibrarianEditButtonBar(props) {
  const {
    onConfirmClick,
    isEditing,
    enableEditing,
    disableEditing,
  } = props;

  if (isEditing) {
    return (
      <div className="librarianEditButtonBar">
        <LibrarianEditConfirmButton onConfirmClick={onConfirmClick} />
        <LibrarianEditCancelButton onCancelClick={disableEditing} />
      </div>
    );
  }
  return (
    <div className="librarianEditButtonBar">
      <LibrarianEditButton onEditClick={enableEditing} />
    </div>
  );
}

LibrarianEditButtonBar.propTypes = {
  onConfirmClick: PropTypes.func.isRequired,
  isEditing: PropTypes.bool.isRequired,
  enableEditing: PropTypes.func.isRequired,
  disableEditing: PropTypes.func.isRequired,
};

import React from 'react';
import PropTypes from 'prop-types';

export default function LibrarianEditCancelButton(props) {
  const { onCancelClick } = props;

  return (
    <button
      type="button"
      className="librarianEditCancelButton"
      onClick={onCancelClick}
    >
      Discard Changes
    </button>
  );
}

LibrarianEditCancelButton.propTypes = {
  onCancelClick: PropTypes.func.isRequired,
};

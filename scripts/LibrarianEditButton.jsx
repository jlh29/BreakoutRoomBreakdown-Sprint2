import React from 'react';
import PropTypes from 'prop-types';

export default function LibrarianEditButton(props) {
  const { onEditClick } = props;

  return (
    <button
      type="button"
      className="librarianEditButton"
      onClick={onEditClick}
    >
      Edit
    </button>
  );
}

LibrarianEditButton.propTypes = {
  onEditClick: PropTypes.func.isRequired,
};

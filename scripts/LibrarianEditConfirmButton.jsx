import React, { useState } from 'react';
import PropTypes from 'prop-types';

export default function LibrarianEditConfirmButton(props) {
  const { onConfirmClick } = props;
  const [mustConfirm, setMustConfirm] = useState(true);

  function updateMustConfirm() {
    setMustConfirm(false);
  }

  if (mustConfirm) {
    return (
      <button
        type="button"
        className="librarianEditSaveButton"
        onClick={updateMustConfirm}
      >
        Save Changes
      </button>
    );
  }
  return (
    <button
      type="button"
      className="librarianEditConfirmButton"
      onClick={onConfirmClick}
    >
      Confirm Changes
    </button>
  );
}

LibrarianEditConfirmButton.propTypes = {
  onConfirmClick: PropTypes.func.isRequired,
};

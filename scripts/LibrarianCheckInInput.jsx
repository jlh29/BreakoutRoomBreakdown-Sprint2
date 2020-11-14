import * as React from 'react';

export default function LibrarianCheckInInput(props) {
  const { inputRef } = props;
  return (
    <input
      id="librarianCheckInInput"
      type="text"
      ref={inputRef}
      placeholder="Check-in ID:"
    />
  );
}

import * as React from 'react';

export default function LibrarianCheckInResult(props) {
  const { isSuccess } = props;
  if (isSuccess) {
    return (
      <p id="librarianCheckInResult">
        This reservation has been successfully checked in!
      </p>
    );
  }
  return (
    <p id="librarianCheckInResult">
      Sorry, this code could not be validated. Please try again.
    </p>
  );
}

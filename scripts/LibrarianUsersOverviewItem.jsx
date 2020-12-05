import React from 'react';

export default function LibrarianUsersOverviewItem(props) {
  const { user, isEditing } = props;

  if (isEditing) {
    return (
      <div className='user'>
        <p>
          Name: {user.name}
        </p>
        <p>
          UCID: {user.ucid}
        </p>
        <div
          className='librarianEditFieldContainer'
        >
          <p
            className='librarianEditFieldLabel'
          >Role:</p>
          <select
            id='userRoleField'
            className='librarianEditField'
            defaultValue={user.role.toUpperCase()}
          >
            <option value='STUDENT'>Student</option>
            <option value='PROFESSOR'>Professor</option>
            <option value='LIBRARIAN'>Librarian</option>
          </select>
        </div>
      </div>
    );
  } else {
    return (
      <div className='user'>
        <p>
          Name: {user.name}
        </p>
        <p>
          UCID: {user.ucid}
        </p>
        <p>
          Role: {user.role}
        </p>
      </div>
    );
  }
}

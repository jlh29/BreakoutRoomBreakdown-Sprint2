import React, { useState } from 'react';
import LibrarianUsersOverviewItem from './LibrarianUsersOverviewItem';
import LibrarianEditButtonBar from './LibrarianEditButtonBar';

export default function LibrarianUsersOverview(props) {
  const { users } = props;
  const [selectedUser, setSelectedUser] = useState({});
  const [isEditing, setIsEditing] = useState(false);

  function enableEditing() {
      setIsEditing(true);
  }

  function disableEditing() {
      setIsEditing(false);
  }

  function changeSelectedUser(newUser) {
    setSelectedUser(newUser);
    disableEditing();
  }

  return (
    <div id="usersContainer" className="menuContainer">
      <div id="usersSelector" className="menuSelector">
        {
                    users.map(
                      (user) => (
                        <button
                          className="menuSelectorButton"
                          type="button"
                          onClick={() => changeSelectedUser(user)}
                          key={user.id}
                        >
                          {user.name}
                        </button>
                      ),
                    )
                }
      </div>
      <div id="userDetails" className="menuContents">
        {('id' in selectedUser)
          ? (
            <div>
              <LibrarianUsersOverviewItem
                user={selectedUser}
                isEditing={isEditing}
              />
              <LibrarianEditButtonBar
                isEditing={isEditing}
                enableEditing={enableEditing}
                disableEditing={disableEditing}
              />
            </div>
          )
          : null}
      </div>
    </div>
  );
}

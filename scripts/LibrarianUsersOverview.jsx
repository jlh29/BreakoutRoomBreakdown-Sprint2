import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import LibrarianUsersOverviewItem from './LibrarianUsersOverviewItem';
import LibrarianEditButtonBar from './LibrarianEditButtonBar';
import Socket from './Socket';

export default function LibrarianUsersOverview(props) {
  const { users, redrawSelectedUser, setRedrawSelectedUser } = props;
  const [selectedUser, setSelectedUser] = useState({});
  const [isEditing, setIsEditing] = useState(false);
  const roleRef = React.createRef();

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

  function onConfirmClick() {
    disableEditing();
    if (selectedUser.id === undefined) {
      return;
    }
    Socket.emit('update user', {
      id: selectedUser.id,
      role: roleRef.current.value,
    });
  }

  function redrawSelectedRoomOnUpdate() {
    useEffect(() => {
      if (redrawSelectedUser) {
        if (selectedUser.id !== undefined) {
          let newSelectedUser = {};
          for (const user of users) {
            if (selectedUser.id === user.id) {
              newSelectedUser = user;
              break;
            }
          }
          setSelectedUser(newSelectedUser);
        }
        setRedrawSelectedUser(false);
      }
    }, [redrawSelectedUser]);
  }

  redrawSelectedRoomOnUpdate();

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
                roleRef={roleRef}
              />
              <LibrarianEditButtonBar
                isEditing={isEditing}
                enableEditing={enableEditing}
                disableEditing={disableEditing}
                onConfirmClick={onConfirmClick}
              />
            </div>
          )
          : null}
      </div>
    </div>
  );
}

LibrarianUsersOverview.propTypes = {
  users: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      ucid: PropTypes.string.isRequired,
      role: PropTypes.string.isRequired,
    }),
  ).isRequired,
  redrawSelectedUser: PropTypes.bool.isRequired,
  setRedrawSelectedUser: PropTypes.func.isRequired,
};

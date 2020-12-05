import React, { useState } from 'react';
import LibrarianRoomsOverviewItem from './LibrarianRoomsOverviewItem';
import LibrarianEditButtonBar from './LibrarianEditButtonBar';

export default function LibrarianRoomsOverview(props) {
  const { rooms } = props;
  const [selectedRoom, setSelectedRoom] = useState({});
  const [isEditing, setIsEditing] = useState(false);

  function enableEditing() {
      setIsEditing(true);
  }

  function disableEditing() {
      setIsEditing(false);
  }

  function changeSelectedRoom(newRoom) {
    setSelectedRoom(newRoom);
    disableEditing();
  }

  return (
    <div id="roomsContainer" className="menuContainer">
      <div id="roomsSelector" className="menuSelector">
        {
                    rooms.map(
                      (room) => (
                        <button
                          className="menuSelectorButton"
                          type="button"
                          onClick={() => changeSelectedRoom(room)}
                          key={room.id}
                        >
                          Room
                          {' '}
                          {room.room_number}
                        </button>
                      ),
                    )
                }
      </div>
      <div id="roomDetails" className="menuContents">
        {('id' in selectedRoom)
          ? (
            <div>
              <LibrarianRoomsOverviewItem
                room={selectedRoom}
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

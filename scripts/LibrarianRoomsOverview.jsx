import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import LibrarianRoomsOverviewItem from './LibrarianRoomsOverviewItem';
import LibrarianEditButtonBar from './LibrarianEditButtonBar';
import Socket from './Socket';

export default function LibrarianRoomsOverview(props) {
  const { rooms, redrawSelectedRoom, setRedrawSelectedRoom } = props;
  const [selectedRoom, setSelectedRoom] = useState({});
  const [isEditing, setIsEditing] = useState(false);
  const roomNumberRef = React.createRef();
  const roomSizeRef = React.createRef();
  const roomCapacityRef = React.createRef();

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

  function onConfirmClick() {
    disableEditing();
    if (selectedRoom.id === undefined) {
      return;
    }
    Socket.emit('update room', {
      id: selectedRoom.id,
      room_number: roomNumberRef.current.value,
      size: roomSizeRef.current.value,
      capacity: roomCapacityRef.current.value,
    });
  }

  function redrawSelectedRoomOnUpdate() {
    useEffect(() => {
      if (redrawSelectedRoom) {
        if (selectedRoom.id !== undefined) {
          let newSelectedRoom = {};
          for (const room of rooms) {
            if (selectedRoom.id === room.id) {
              newSelectedRoom = room;
              break;
            }
          }
          setSelectedRoom(newSelectedRoom);
        }
        setRedrawSelectedRoom(false);
      }
    }, [redrawSelectedRoom]);
  }

  redrawSelectedRoomOnUpdate();

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
                roomNumberRef={roomNumberRef}
                roomSizeRef={roomSizeRef}
                roomCapacityRef={roomCapacityRef}
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

LibrarianRoomsOverview.propTypes = {
  rooms: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      room_number: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.number,
      ]).isRequired,
      size: PropTypes.string.isRequired,
      capacity: PropTypes.number.isRequired,
    }),
  ).isRequired,
  redrawSelectedRoom: PropTypes.bool.isRequired,
  setRedrawSelectedRoom: PropTypes.func.isRequired,
};

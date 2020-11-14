import React, { useState } from 'react';
import LibrarianRoomsOverviewItem from './LibrarianRoomsOverviewItem';

export default function LibrarianRoomsOverview(props) {
  const { rooms } = props;
  const [selectedRoom, setSelectedRoom] = useState({});
  return (
    <div id="roomsContainer" className="menuContainer">
      <div id="roomsSelector" className="menuSelector">
        {
                    rooms.map(
                      (room) => (
                        <button
                          className="menuSelectorButton"
                          type="button"
                          onClick={() => setSelectedRoom(room)}
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
            <LibrarianRoomsOverviewItem
              room={selectedRoom}
            />
          )
          : null}
      </div>
    </div>
  );
}

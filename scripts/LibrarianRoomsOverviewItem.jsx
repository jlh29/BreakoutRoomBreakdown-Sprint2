import * as React from 'react';

export default function LibrarianRoomsOverviewItem(props) {
  const { room } = props;

  return (
    <div className="room">
      <p>
        Room Number:
        {room.room_number}
      </p>
      <p>
        Size:
        {room.size.toUpperCase()}
      </p>
      <p>
        Capacity:
        {room.capacity}
      </p>
    </div>
  );
}

import * as React from 'react';
import PropTypes from 'prop-types';

export default function LibrarianRoomsOverviewItem(props) {
  const {
    room, isEditing, roomNumberRef, roomSizeRef, roomCapacityRef,
  } = props;

  if (isEditing) {
    return (
      <div className="room">
        <div
          className="librarianEditFieldContainer"
        >
          <p
            className="librarianEditFieldLabel"
          >
            Room Number:
          </p>
          <input
            type="number"
            id="roomNumberField"
            className="librarianEditField"
            defaultValue={room.room_number}
            ref={roomNumberRef}
          />
        </div>

        <div
          className="librarianEditFieldContainer"
        >
          <p
            className="librarianEditFieldLabel"
          >
            Room Size:
          </p>
          <select
            id="roomSizeField"
            className="librarianEditField"
            defaultValue={room.size.toUpperCase()}
            ref={roomSizeRef}
          >
            <option value="S">S</option>
            <option value="M">M</option>
            <option value="L">L</option>
            <option value="XL">XL</option>
          </select>
        </div>

        <div
          className="librarianEditFieldContainer"
        >
          <p
            className="librarianEditFieldLabel"
          >
            Capacity:
          </p>
          <input
            type="number"
            id="roomCapacityField"
            className="librarianEditField"
            defaultValue={room.capacity}
            ref={roomCapacityRef}
            min="2"
            max="20"
          />
        </div>
      </div>
    );
  }
  return (
    <div className="room">
      <p>
        Room Number:
        {' '}
        {room.room_number}
      </p>
      <p>
        Size:
        {' '}
        {room.size.toUpperCase()}
      </p>
      <p>
        Capacity:
        {' '}
        {room.capacity}
      </p>
    </div>
  );
}

LibrarianRoomsOverviewItem.propTypes = {
  room: PropTypes.shape({
    id: PropTypes.number.isRequired,
    room_number: PropTypes.oneOfType([
      PropTypes.string,
      PropTypes.number,
    ]).isRequired,
    size: PropTypes.string.isRequired,
    capacity: PropTypes.number.isRequired,
  }).isRequired,
  isEditing: PropTypes.bool.isRequired,
  roomNumberRef: PropTypes.oneOfType([
    PropTypes.func,
    PropTypes.shape({ current: PropTypes.element }),
  ]).isRequired,
  roomSizeRef: PropTypes.oneOfType([
    PropTypes.func,
    PropTypes.shape({ current: PropTypes.element }),
  ]).isRequired,
  roomCapacityRef: PropTypes.oneOfType([
    PropTypes.func,
    PropTypes.shape({ current: PropTypes.element }),
  ]).isRequired,
};

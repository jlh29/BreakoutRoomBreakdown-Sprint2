import * as React from 'react';

export default function LibrarianRoomsOverviewItem(props) {
  const { room, isEditing } = props;

  if (isEditing) {
    return (
      <div className='room'>
        <div
          className='librarianEditFieldContainer'
        >
          <p
            className='librarianEditFieldLabel'
          >Room Number:</p>
          <input
            type='number'
            id='roomNumberField'
            className='librarianEditField'
            defaultValue={room.room_number}
          ></input>
        </div>

        <div
          className='librarianEditFieldContainer'
        >
          <p
            className='librarianEditFieldLabel'
          >Room Size:</p>
          <select
            id='roomSizeField'
            className='librarianEditField'
            defaultValue={room.size.toUpperCase()}
          >
            <option value='S'>S</option>
            <option value='M'>M</option>
            <option value='L'>L</option>
            <option value='XL'>XL</option>
          </select>
        </div>

        <div
          className='librarianEditFieldContainer'
        >
          <p
            className='librarianEditFieldLabel'
          >Capacity:</p>
          <input
            type='number'
            id='roomCapacityField'
            className='librarianEditField'
            defaultValue={room.capacity}
            min='2'
            max='20'
          ></input>
        </div>
      </div>
    );
  } else {
    return (
      <div className='room'>
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
}

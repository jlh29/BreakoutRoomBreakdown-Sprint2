import * as React from 'react';

export default function LibrarianRoomsOverviewItem(props) {
    const { room } = props;
    
    return (
        <li className='roomsItem'>
            <div className='room'>
                <p>Room Number: {room.room_number}</p>
                <p>Capacity: {room.capacity}</p>
            </div>
        </li>
    );
}

import * as React from 'react';
import LibrarianRoomsOverviewItem from './LibrarianRoomsOverviewItem';

export default function LibrarianRoomsOverview(props) {
    const { rooms } = props;
    return (
        <div id='roomsContainer'>
            <ul id='roomsList'>
                {
                    rooms.map(
                        room => <LibrarianRoomsOverviewItem
                            room={room}
                            key={room.id}
                        />
                    )
                }
            </ul>
        </div>
    );
}

import React, { useState } from 'react';
import LibrarianUsersOverviewItem from './LibrarianUsersOverviewItem';

export default function LibrarianUsersOverview(props) {
    const { users } = props;
    const [selectedUser, setSelectedUser] = useState({});
    return (
        <div id='usersContainer' className='menuContainer'>
            <div id='usersSelector' className='menuSelector'>
                {
                    users.map(
                        user => (
                            <button
                                className='menuSelectorButton'
                                type='button'
                                onClick={() => setSelectedUser(user)}
                                key={user.id}
                            >
                                {user.name}
                            </button>
                        )
                    )
                }
            </div>
            <div id='userDetails' className='menuContents'>
                {('id' in selectedUser) ?
                    <LibrarianUsersOverviewItem
                        user={selectedUser}
                    />
                    :
                    null
                }
            </div>
        </div>
    );
}

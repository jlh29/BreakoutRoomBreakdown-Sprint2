import * as React from 'react';

export default function LibrarianUsersOverviewItem(props) {
    const { user } = props;
    
    return (
        <li className='usersItem'>
            <div className='user'>
                <p>Name: {user.name}</p>
                <p>UCID: {user.ucid}</p>
                <p>Role: {user.role}</p>
            </div>
        </li>
    );
}

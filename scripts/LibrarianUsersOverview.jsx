import * as React from 'react';
import LibrarianUsersOverviewItem from './LibrarianUsersOverviewItem';

export default function LibrarianUsersOverview(props) {
    const { users } = props;
    return (
        <div id='usersContainer'>
            <ul id='usersList'>
                {
                    users.map(
                        user => <LibrarianUsersOverviewItem
                            user={user}
                            key={user.id}
                        />
                    )
                }
            </ul>
        </div>
    );
}

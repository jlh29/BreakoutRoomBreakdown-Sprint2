    
import * as React from 'react';


import { OAuthButton } from './OAuthButton';
import { Socket } from './Socket';

export function Content() {
    const [accounts, setAccounts] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('accounts received', (data) => {
                let allAccounts = data['allAccounts'];
                console.log("Received accounts from server: " + allAccounts);
                setAccounts(allAccounts);
            })
        });
    }
    
    getNewAddresses();

    return (
        <div>
            <h1>Log in with Google!</h1>
            <OAuthButton />
        </div>
    );
}

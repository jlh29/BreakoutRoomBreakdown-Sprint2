    
import * as React from 'react';


import { OAuthButton } from './OAuthButton';
import { Socket } from './Socket';

export function Content() {
    const [accounts, setAccounts] = React.useState([]);
    
    function getAllAccounts() {
        React.useEffect(() => {
            Socket.on('accounts received', (data) => {
                let allAccounts = data['allAccounts'];
                console.log("Received accounts from server: " + allAccounts);
                setAccounts(allAccounts);
            })
        });
    }
    
    getAllAccounts();
    
    // TODO use these accounts for something
    
    return (
        <div>
            <h1>Log in with Google!</h1>
            <OAuthButton />
        </div>
    );
}

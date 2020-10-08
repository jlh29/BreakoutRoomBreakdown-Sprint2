    
import * as React from 'react';


import { GithubButton } from './GithubButton';
import { FacebookButton } from './FacebookButton';
import { InstagramButton } from './InstagramButton';
import { GoogleButton } from './GoogleButton';
import { TwitterButton } from './TwitterButton';
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
            <h1>Log in with OAuth!</h1>
            <GithubButton />
            <FacebookButton />
            <InstagramButton />
            <GoogleButton />
            <TwitterButton />
        </div>
    );
}

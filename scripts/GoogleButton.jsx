import * as React from 'react';
import Socket from './Socket';
import GoogleLogin from 'react-google-login';

export default function GoogleButton() {
    function handleSuccess(response) {
        if (!('profileObj' in response)) {
            handleFailure(response);
            return;
        }
        let { name, email } = response.profileObj;
        if (!email.toLowerCase().endsWith('@njit.edu')) {
            handleFailure(response);
            return;
        }
        Socket.emit('new login', {name, email});
        console.log(`Sent the name ${name} and email ${email} to server!`);
    }
    
    function handleFailure(response) {
        // TODO: show some sort of error message
        console.log('Encountered an error while signing in.');
        console.log(response);
    }

    return <GoogleLogin
        className="gbutton"
        clientId="791154624378-g41rhk0tetto6ueot7mcjffts9g294e7.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={handleSuccess}
        onFailure={handleFailure}
        cookiePolicy={'single_host_origin'}
    />;
}
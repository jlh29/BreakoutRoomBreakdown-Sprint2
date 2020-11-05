import * as React from 'react';
import Socket from './Socket';

export function GoogleButton() {
    function handleSuccessfulGoogleLogin(event) {
        // TODO
    }
    
    function handleFailedGoogleLogin(event) {
        // TODO
    }

    return (
        <form name='loginForm' method='post'>
            <GoogleLogin
                className="googleButton"
                clientId='TODO'
                buttonText='Login with Google'
                onSuccess={handleSuccessfulGoogleLogin}
                onFailure={handleFailedGoogleLogin}
                type='submit'
            />
        </form>
    );
}

import React, { useEffect } from 'react';
import GoogleLogin from 'react-google-login';
import Socket from './Socket';

export default function GoogleButton() {
  function handleSuccess(response) {
    /*global gapi*/
    const auth = gapi.auth2.getAuthInstance();
    const user = auth.currentUser.get();
    let idToken;
    if (user.isSignedIn()) {
      idToken = user.getAuthResponse().id_token;
    } else {
      handleFailure(response);
      return;
    }
    Socket.emit('new login', { idToken });
  }

  function handleFailure(response) {
    // TODO: show some sort of error message
    console.log('Encountered an error while signing in.');
    console.log(response);
  }

  function listenToServer() {
    useEffect(() => {
      Socket.on('failed login', handleFailure);
      return () => {
        Socket.off('failed login', handleFailure);
      };
    });
  }

  listenToServer();

  return (
    <GoogleLogin
      className="gbutton"
      clientId="836600659281-eeutvpmf60kb2f2jfhcju5kfnebbsuu2.apps.googleusercontent.com"
      buttonText="Login"
      onSuccess={handleSuccess}
      onFailure={handleFailure}
      cookiePolicy="single_host_origin"
    />
  );
}

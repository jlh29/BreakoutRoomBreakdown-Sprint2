import React, { useEffect } from 'react';
import GoogleLogin from 'react-google-login';
import Socket from './Socket';

export default function GoogleButton() {
  var txt;
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
    console.log('Encountered an error while signing in.');
    console.log(response);
    if (!confirm("Please use your NJIT email!")) {
    txt = "OK";
  } else {
      txt = "Cancel"
    }
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
      clientId="650589780426-q6cu2s43su3mba4u4948bk0gcdsaht39.apps.googleusercontent.com"
      buttonText="Login"
      onSuccess={handleSuccess}
      onFailure={handleFailure}
      cookiePolicy="single_host_origin"
    />
  );
}

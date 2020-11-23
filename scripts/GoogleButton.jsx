import * as React from 'react';
import GoogleLogin from 'react-google-login';
import Socket from './Socket';

export default function GoogleButton() {
  function handleSuccess(response) {
    if (!('profileObj' in response)) {
      handleFailure(response);
      return;
    }
    const { name, email } = response.profileObj;
    if (!email.toLowerCase().endsWith('@njit.edu')) {
      handleFailure(response);
      return;
    }
    Socket.emit('new login', { name, email });
    console.log(`Sent the name ${name} and email ${email} to server!`);
  }

  function handleFailure(response) {
    // TODO: show some sort of error message
    console.log('Encountered an error while signing in.');
    console.log(response);
  }

  return (
    <GoogleLogin
      className="gbutton"
      clientId="75378465237-d53v2fhub86gdal5v8bpp992uqcgeuoc.apps.googleusercontent.com"
      buttonText="Login"
      onSuccess={handleSuccess}
      onFailure={handleFailure}
      cookiePolicy="single_host_origin"
    />
  );
}

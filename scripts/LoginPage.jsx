import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import LibrarianOverview from './LibrarianOverview';
import ReservationOverview from './ReservationOverview';
import GoogleButton from './GoogleButton';
import Socket from './Socket';

export default function LoginPage() {
  function onSuccessfulLogin(data) {
    if (data.role.toLowerCase().trim() == 'librarian') {
      ReactDOM.render(
        <LibrarianOverview />,
        document.getElementById('content'),
      );
    } else {
      ReactDOM.render(
        <ReservationOverview name={data.name} />,
        document.getElementById('content'),
      );
    }
  }

  function listenToServer() {
    useEffect(() => {
      Socket.on('successful login', onSuccessfulLogin);
      return () => {
        Socket.off('successful login', onSuccessfulLogin);
      };
    });
  }

  listenToServer();

  return (
    <div id="loginContainer" className="flexColumn">
      <h1>Webauth Authentication Service</h1>
      <GoogleButton />
    </div>
  );
}

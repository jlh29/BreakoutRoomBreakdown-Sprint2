import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import Content_Auth from './Content_Auth';
import GoogleButton from './GoogleButton';
import Socket from './Socket';

export function Content() {
    function onSuccessfulLogin(data) {
        ReactDOM.render(
            <Content_Auth name={data.name} />,
            document.getElementById('content')
        );
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
        <div id='loginContainer'>
            <h1>Webauth Authentication Service</h1>
            <GoogleButton />
        </div>
    );
}

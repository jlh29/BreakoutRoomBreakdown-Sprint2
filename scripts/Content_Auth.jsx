import * as React from 'react';
import { Socket } from './Socket';
import ReactDOM from 'react-dom';
import { MyCalendar } from './Calendar';

export function Content_Auth() {
    const [name, setName] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('username', (data) => {
                 console.log("Received addresses from server: " + data['names']);
                 setName(data['names']);
            })
        });
    }
    getNewAddresses();
    
    function logout(event) {
        ReactDOM.render(<Content />, document.getElementById('Content'));
    }

    return (
        <div>
          <h1>Breakout Room Breakdown</h1>
          <p> Welcome {name} </p>
          <form onClick={logout}>
          <button>Logout</button></form>
          
          <MyCalendar />
        </div>
    );
}
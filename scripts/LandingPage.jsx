import * as React from 'react';
import ReactDOM from 'react-dom';
import { ReservationOverview } from './ReservationOverview';

function goBack(){
        ReactDOM.render(<ReservationOverview />, document.getElementById('content'));
    }

export function LandingPage() {


  return (
      <div className="all">
      <form id="back" onClick={goBack}>
        <button>Back to BNB</button>
      </form>
      <p1>Team Members:</p1>
      </div>);
}
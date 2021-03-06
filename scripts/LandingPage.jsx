import * as React from 'react';
import ReactDOM from 'react-dom';
import ReservationOverview from './ReservationOverview';

function goBack() {
  ReactDOM.render(<ReservationOverview />, document.getElementById('content'));
}

export default function LandingPage() {
  return (
    <div className="all">
      <form id="back">
        <button type="button" onClick={goBack}>Back to BNB</button>
      </form>
      <h3>Breakout Room Breakdown</h3>

      <div className="goal">
        <p>
          Our mission - A browser-based booking appointment app
          for easy scheduling of breakout rooms. We aim to deliver
          a more technological and modern approach to NJIT breakout
          rooms used for study groups or similar.
        </p>
      </div>

      <div className="tech">
        <p>
          Technologies Used:
          <br />
          Python
          <br />
          Flask
          <br />
          React/JS
          <br />
          PostgreSQL
          <br />
          CircleCI
          <br />
          AWS
          <br />
          Heroku
          <br />
          Twilio
          <br />
          SendGrid
        </p>
      </div>

      <div className="url">
        <h4>Try BRB</h4>
        <a
          href="https://breakoutroombreakdown.herokuapp.com/"
        >
          Visit Breakout Room Breakdown!
        </a>
      </div>

      <div className="team">
        <p>
          We are not just four different individuals, but we are
          known for the Teamwork of BRB.
        </p>
        <h5>Meet our team</h5>
      </div>

      <div className="dipam">
        <h4>Dipam Patel</h4>
        <p1>Worked on Front-End</p1>
        <br />
        <a
          href="https://www.linkedin.com/in/dipam-patel-b0b278201/"
        >
          LinkedIn!
        </a>
      </div>

      <div className="Binarynelle">
        <h4>Binarynelle Sune</h4>
        <p1>Worked on Front-End/Back-End</p1>
        <br />
        <a
          href="https://www.linkedin.com/in/dipam-patel-b0b278201/"
        >
          LinkedIn!
        </a>
      </div>

      <div className="Jacob Haynie">
        <h4>Jacob Haynie</h4>
        <p1>Worked on Back-End/Front End</p1>
        <br />
        <a
          href="https://www.linkedin.com/in/dipam-patel-b0b278201/"
        >
          LinkedIn!
        </a>
      </div>

      <div className="Timothy">
        <h4>Timothy Schutte</h4>
        <p1>Worked on Back-End</p1>
        <br />
        <a
          href="https://www.linkedin.com/in/dipam-patel-b0b278201/"
        >
          LinkedIn!
        </a>
      </div>

    </div>
  );
}

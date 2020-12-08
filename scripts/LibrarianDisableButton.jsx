import * as React from 'react';
import { Socket } from './Socket';

export default function LibrarianDisableButton(props) {
    const {startDate} = props;
    const {endDate} = props;
    const {note} = props;
  
  function handleSubmit(){
    console.log(`User added a ${startDate} and ${endDate}, ${note}`);
    
    Socket.emit('disable date', { 
        'startDate': startDate,
        'endDate': endDate,
        'note': note,
    });
    
    console.log(`Sent ${startDate} and ${endDate}, ${note} to the server`);
  }
  
  return (
      <button 
      startDate={startDate}
      endDate={endDate}
      note={note}
      type="text" 
      onClick={handleSubmit}>
      Disable Date
      </button>
      );
}

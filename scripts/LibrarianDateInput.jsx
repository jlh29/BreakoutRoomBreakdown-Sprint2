import * as React from 'react';
import LibrarianDisableButton from './LibrarianDisableButton';

export default function LibrarianDateInput(props) {
  const [startDate, setStartDate] = React.useState("");
  const [endDate, setEndDate] = React.useState("");
  const [note, setNote] = React.useState("");
  
  const handleStart = ({ target }) => {
    const newText = target.value;
    setStartDate(newText);
  };
  
  const handleEnd = ({ target }) => {
    const newText = target.value;
    setEndDate(newText);
   
  };
  
  const handleNote = ({ target }) => {
    const newText = target.value;
    setNote(newText);
  };
 
  return (
    <div>
        <label for="librarianStartDate">Start date:</label>
        <input
          id="librarianStartDate"
          type="date"
          value={startDate.toString("yyyy-MM-dd")}
          onChange={handleStart}
        />
        
        <label for="librarianEndDate">End date:</label>
        <input
          id="librarianEndDate"
          type="date"
          value={endDate.toString("yyyy-MM-dd")}
          onChange={handleEnd}
        />
        
        <label for="librarianEndDate">Note:</label>
        <input
          id="librarianNote"
          type="text"
          value={note}
          onChange={handleNote}
        />
        
        <LibrarianDisableButton startDate={startDate} endDate={endDate} note={note}/>
    </div>
  );
}

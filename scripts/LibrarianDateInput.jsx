import * as React from 'react';

export default function LibrarianDateInput(props) {
 
  return (
    <div>
        <label for="librarianStartDate">Start date:</label>
        <input
          id="librarianStartDate"
          type="date"
          name="startDate"
        />
        
        <label for="librarianEndDate">End date:</label>
        <input
          id="librarianEndDate"
          type="date"
          name="endDate"
        />
    </div>
  );
}

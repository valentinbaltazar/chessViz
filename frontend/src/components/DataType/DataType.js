import React, { useState } from 'react';

function DataType({ onSubmit }) {
  const [selectedOption, setSelectedOption] = useState('test');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({selectedOption});
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="options">Select an option:</label>
          <select
            id="options"
            value={selectedOption}
            onChange={(e) => setSelectedOption(e.target.value)}
          >
            <option value="Option 1">Elo Rating</option>
            <option value="Option 2">Match Wins</option>
            <option value="Option 3">Openings</option>
          </select>
        </div>
        <button type="submit">Make Plot</button>
      </form>
    
    </div>
  );
}

export default DataType;

import React, { useState } from 'react';
import DataType from '../DataType/DataType';
import DataPlot from '../DataPlot/DataPlot';
import Toolbar from '../ToolBar/ToolBar';

function TopHalf() {
  const [submittedData, setSubmittedData] = useState('');

  const handleFormSubmit = (data) => {
    setSubmittedData(data);
  };

  return (
    <div className="top-section">
        <div className="toolbar">
            <h1>Menu</h1>
            <Toolbar/>
            <DataType onSubmit={handleFormSubmit} />
        </div>
        <div className="plot-area">
            <h1>Analysis</h1>
            <DataPlot plotData={submittedData} />
        </div>
    </div>
  );
}

export default TopHalf;

import React, { useState } from 'react';
import DataType from '../DataType/DataType';
import DataPlot from '../DataPlot/DataPlot';
import Toolbar from '../ToolBar/ToolBar';
import DashBoard from '../DashBoard/DashBoard';

function TopHalf() {
  const [submittedData, setSubmittedData] = useState('');

  const handleFormSubmit = (data) => {
    setSubmittedData(data);
  };

  return (
    <div className="App">
        <div className="top-section">
            <div className="toolbar">
                <h1>Menu</h1>
                <Toolbar/>
                <div>
                <h1>Choose Data to Plot</h1>

                <DataType onSubmit={handleFormSubmit} />
                </div>
            </div>
            <div className="plot-area">
                <h1>Analysis</h1>
                <DataPlot plotData={submittedData} />
            </div>
        </div>
        <DashBoard plotData={submittedData}/>
    </div>
  );
}

export default TopHalf;

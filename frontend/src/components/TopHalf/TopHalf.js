import React, { useState, useCallback } from 'react';
import DataType from '../DataType/DataType';
import DataPlot from '../DataPlot/DataPlot';
import Toolbar from '../ToolBar/ToolBar';
import DashBoard from '../DashBoard/DashBoard';
import config from '../../config';

function TopHalf() {
  // User state
  const [currentUser, setCurrentUser] = useState(config.DEFAULT_USERNAME);
  const [userLoaded, setUserLoaded] = useState(true); // Default user is pre-loaded

  // Plot selection state
  const [selectedPlot, setSelectedPlot] = useState(null);

  // Filter state
  const [filters, setFilters] = useState({
    timeClass: config.DEFAULT_TIME_CLASS,
    timeControl: config.DEFAULT_TIME_CONTROL,
    playerColor: 'white',
  });

  const handleUserChange = useCallback((username, loaded) => {
    setCurrentUser(username);
    setUserLoaded(loaded);
    // Reset plot when user changes
    if (loaded) {
      setSelectedPlot(null);
    }
  }, []);

  const handlePlotSelect = useCallback((plotType) => {
    setSelectedPlot(plotType);
  }, []);

  const handleFilterChange = useCallback((newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  }, []);

  return (
    <div className="App">
      <div className="top-section">
        <div className="toolbar">
          <h1>Menu</h1>
          <Toolbar
            onUserChange={handleUserChange}
            currentUser={currentUser}
          />
          <div>
            <h1>Choose Data to Plot</h1>
            <DataType
              onSubmit={handlePlotSelect}
              onFilterChange={handleFilterChange}
              filters={filters}
              disabled={!userLoaded}
            />
          </div>
        </div>
        <div className="plot-area">
          <h1>Analysis</h1>
          <DataPlot
            plotType={selectedPlot}
            username={currentUser}
            filters={filters}
            userLoaded={userLoaded}
          />
        </div>
      </div>
      <DashBoard
        plotType={selectedPlot}
        username={currentUser}
      />
    </div>
  );
}

export default TopHalf;

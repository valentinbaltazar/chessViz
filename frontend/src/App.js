import React from 'react';
import './App.css';  // Import the CSS file for styling

import Toolbar from './components/ToolBar/ToolBar';
import TopHalf from './components/TopHalf/TopHalf';

function App() {
  return (
    <div className="App">
      
      <TopHalf/>

      <div className="dashboard">
        <h1>DashBoard</h1>
      </div>

    </div>
  );
}

export default App;

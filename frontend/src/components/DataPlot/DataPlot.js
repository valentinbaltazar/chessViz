import React, { useEffect, useState } from 'react';
import TreeDisplay from '../TreePlot/TreePlot';

function DataPlot({ plotData }) {
  const [option, setOption] = useState('')

  const url = `http://127.0.0.1:8000/get-plot?option=${encodeURIComponent(plotData.selectedOption)}`

  useEffect(() => {
    setOption(plotData.selectedOption)
  }, [plotData]);

  return (
    <div>
      {option === 'Option 1' ? (<img src={url} alt='Plot Area'></img>):
        option === 'Option 2' ? (<img src={url} alt='Plot Area'></img>):
        option === 'Option 3' ? <TreeDisplay plotData={plotData}/>:
      (<div>
      <h2>Choose data to plot...</h2>
      </div>)
      }

    </div>
  );
}

export default DataPlot;

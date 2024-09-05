import React, { useEffect, useState } from "react";

function TreeDisplay({plotData}) {
  const [tree, setTree] = useState("");

  const url = `http://127.0.0.1:8000/get-plot?option=${encodeURIComponent(plotData.selectedOption)}`;

  useEffect(() => {

    fetch(url)  // FastAPI URL
      .then((response) => response.json())
      .then((data) => setTree(data.tree))
      .catch((error) => console.error("Error fetching tree:", error));
  }, [plotData]);

  return (
    <div>
      <h1>Tree Structure</h1>
      <pre>{tree}</pre> {/* pre tag preserves formatting */}
    </div>
  );
};

export default TreeDisplay;

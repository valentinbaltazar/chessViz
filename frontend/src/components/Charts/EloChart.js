import React from 'react';
import Plot from 'react-plotly.js';
import config from '../../config';

function EloChart({ data }) {
  if (!data || !data.dates || data.dates.length === 0) {
    return <div className="chart-empty">No ELO data available for these filters.</div>;
  }

  const plotData = [
    {
      x: data.dates,
      y: data.elos,
      type: 'scatter',
      mode: 'lines+markers',
      name: 'ELO Rating',
      line: { color: config.COLORS.primary, width: 2 },
      marker: { size: 4 },
      hovertemplate:
        '<b>Date:</b> %{x}<br>' +
        '<b>ELO:</b> %{y}<br>' +
        '<b>vs:</b> %{customdata[0]} (%{customdata[1]})<br>' +
        '<b>Result:</b> %{customdata[2]}<extra></extra>',
      customdata: data.dates.map((_, i) => [
        data.opponents[i],
        data.opponent_elos[i],
        data.results[i],
      ]),
    },
  ];

  const layout = {
    title: {
      text: `ELO Progression - ${data.username} (${data.total_games} games)`,
      font: { color: config.COLORS.text },
    },
    xaxis: {
      title: 'Date',
      color: config.COLORS.text,
      gridcolor: 'rgba(255,255,255,0.1)',
    },
    yaxis: {
      title: 'ELO Rating',
      color: config.COLORS.text,
      gridcolor: 'rgba(255,255,255,0.1)',
    },
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { color: config.COLORS.text },
    hovermode: 'closest',
    margin: { t: 50, r: 30, b: 50, l: 60 },
  };

  return (
    <Plot
      data={plotData}
      layout={layout}
      config={{ responsive: true, displayModeBar: true }}
      style={{ width: '100%', height: '400px' }}
    />
  );
}

export default EloChart;

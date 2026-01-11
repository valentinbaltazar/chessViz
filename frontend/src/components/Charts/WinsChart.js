import React from 'react';
import Plot from 'react-plotly.js';
import config from '../../config';

function WinsChart({ data }) {
  if (!data || !data.months || data.months.length === 0) {
    return <div className="chart-empty">No wins data available.</div>;
  }

  const plotData = [
    {
      x: data.months,
      y: data.wins_white,
      type: 'bar',
      name: 'Wins as White',
      marker: { color: config.COLORS.white },
      hovertemplate: '<b>%{x}</b><br>Wins as White: %{y}<extra></extra>',
    },
    {
      x: data.months,
      y: data.wins_black,
      type: 'bar',
      name: 'Wins as Black',
      marker: { color: config.COLORS.black },
      hovertemplate: '<b>%{x}</b><br>Wins as Black: %{y}<extra></extra>',
    },
  ];

  const layout = {
    title: {
      text: `Monthly Wins by Color - ${data.username}`,
      font: { color: config.COLORS.text },
    },
    xaxis: {
      title: 'Month',
      color: config.COLORS.text,
      gridcolor: 'rgba(255,255,255,0.1)',
      tickangle: -45,
    },
    yaxis: {
      title: 'Number of Wins',
      color: config.COLORS.text,
      gridcolor: 'rgba(255,255,255,0.1)',
    },
    barmode: 'group',
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { color: config.COLORS.text },
    legend: {
      orientation: 'h',
      y: -0.2,
    },
    margin: { t: 50, r: 30, b: 80, l: 60 },
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

export default WinsChart;

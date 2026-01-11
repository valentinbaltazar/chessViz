import React from 'react';
import Plot from 'react-plotly.js';
import config from '../../config';

function OpeningStatsChart({ data }) {
  if (!data || !data.openings || data.openings.length === 0) {
    return <div className="chart-empty">No opening statistics available. Play more games with these filters!</div>;
  }

  const plotData = [
    {
      y: data.openings,
      x: data.wins,
      type: 'bar',
      name: 'Wins',
      orientation: 'h',
      marker: { color: config.COLORS.win },
      hovertemplate: '<b>%{y}</b><br>Wins: %{x}<extra></extra>',
    },
    {
      y: data.openings,
      x: data.losses,
      type: 'bar',
      name: 'Losses',
      orientation: 'h',
      marker: { color: config.COLORS.loss },
      hovertemplate: '<b>%{y}</b><br>Losses: %{x}<extra></extra>',
    },
    {
      y: data.openings,
      x: data.draws,
      type: 'bar',
      name: 'Draws',
      orientation: 'h',
      marker: { color: config.COLORS.draw },
      hovertemplate: '<b>%{y}</b><br>Draws: %{x}<extra></extra>',
    },
  ];

  // Add win rate annotations
  const annotations = data.openings.map((opening, i) => ({
    x: data.totals[i] + 1,
    y: opening,
    text: `${data.win_rates[i]}%`,
    showarrow: false,
    font: { color: config.COLORS.text, size: 10 },
    xanchor: 'left',
  }));

  const layout = {
    title: {
      text: `Opening Performance (as ${data.player_color}) - ${data.username}`,
      font: { color: config.COLORS.text },
    },
    xaxis: {
      title: 'Number of Games',
      color: config.COLORS.text,
      gridcolor: 'rgba(255,255,255,0.1)',
    },
    yaxis: {
      color: config.COLORS.text,
      automargin: true,
    },
    barmode: 'stack',
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { color: config.COLORS.text },
    legend: {
      orientation: 'h',
      y: -0.15,
    },
    annotations,
    margin: { t: 50, r: 50, b: 60, l: 150 },
  };

  return (
    <Plot
      data={plotData}
      layout={layout}
      config={{ responsive: true, displayModeBar: true }}
      style={{ width: '100%', height: '500px' }}
    />
  );
}

export default OpeningStatsChart;

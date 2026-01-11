import React from 'react';
import Plot from 'react-plotly.js';
import config from '../../config';

function TimeAnalysisChart({ data }) {
  if (!data || !data.hours) {
    return <div className="chart-empty">No time analysis data available.</div>;
  }

  // Format hours for display
  const hourLabels = data.hours.map(h => {
    if (h === 0) return '12 AM';
    if (h === 12) return '12 PM';
    return h < 12 ? `${h} AM` : `${h - 12} PM`;
  });

  const plotData = [
    // Hourly win rate as line
    {
      x: hourLabels,
      y: data.hourly_win_rates,
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Win Rate by Hour',
      yaxis: 'y',
      line: { color: config.COLORS.primary, width: 2 },
      marker: { size: 6 },
      hovertemplate: '<b>%{x}</b><br>Win Rate: %{y}%<br>Games: %{customdata}<extra></extra>',
      customdata: data.hourly_games,
    },
    // Games played as bars
    {
      x: hourLabels,
      y: data.hourly_games,
      type: 'bar',
      name: 'Games Played',
      yaxis: 'y2',
      marker: { color: 'rgba(33, 150, 243, 0.3)' },
      hovertemplate: '<b>%{x}</b><br>Games: %{y}<extra></extra>',
    },
  ];

  const layout = {
    title: {
      text: `Performance by Hour - ${data.username}`,
      font: { color: config.COLORS.text },
    },
    xaxis: {
      title: 'Hour of Day',
      color: config.COLORS.text,
      gridcolor: 'rgba(255,255,255,0.1)',
      tickangle: -45,
    },
    yaxis: {
      title: 'Win Rate (%)',
      color: config.COLORS.text,
      gridcolor: 'rgba(255,255,255,0.1)',
      range: [0, 100],
      side: 'left',
    },
    yaxis2: {
      title: 'Games Played',
      color: config.COLORS.secondary,
      overlaying: 'y',
      side: 'right',
    },
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { color: config.COLORS.text },
    legend: {
      orientation: 'h',
      y: -0.25,
    },
    margin: { t: 50, r: 60, b: 80, l: 60 },
    showlegend: true,
  };

  // Daily performance bar chart
  const dailyData = [
    {
      x: data.days,
      y: data.daily_win_rates,
      type: 'bar',
      name: 'Win Rate',
      marker: {
        color: data.daily_win_rates.map(rate =>
          rate >= 50 ? config.COLORS.win : config.COLORS.loss
        ),
      },
      text: data.daily_win_rates.map(r => `${r}%`),
      textposition: 'outside',
      hovertemplate: '<b>%{x}</b><br>Win Rate: %{y}%<br>Games: %{customdata}<extra></extra>',
      customdata: data.daily_games,
    },
  ];

  const dailyLayout = {
    title: {
      text: `Performance by Day of Week - ${data.username}`,
      font: { color: config.COLORS.text },
    },
    xaxis: {
      color: config.COLORS.text,
    },
    yaxis: {
      title: 'Win Rate (%)',
      color: config.COLORS.text,
      gridcolor: 'rgba(255,255,255,0.1)',
      range: [0, Math.max(...data.daily_win_rates) + 10],
    },
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { color: config.COLORS.text },
    showlegend: false,
    margin: { t: 50, r: 30, b: 50, l: 60 },
  };

  return (
    <div className="time-analysis-charts">
      <Plot
        data={plotData}
        layout={layout}
        config={{ responsive: true, displayModeBar: true }}
        style={{ width: '100%', height: '350px' }}
      />
      <Plot
        data={dailyData}
        layout={dailyLayout}
        config={{ responsive: true, displayModeBar: true }}
        style={{ width: '100%', height: '300px' }}
      />
    </div>
  );
}

export default TimeAnalysisChart;

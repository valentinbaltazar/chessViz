import React from 'react';
import './DashBoard.css';

const PLOT_DESCRIPTIONS = {
  elo: {
    title: 'ELO Progression',
    description: `This interactive chart shows your ELO rating progression over time. Hover over data points to see details about each game including your opponent and the result. The trend line helps you visualize your overall improvement trajectory. Look for patterns in your rating - stable plateaus often indicate you've mastered certain concepts, while upward trends show active improvement.`,
  },
  wins: {
    title: 'Wins by Color',
    description: `This chart breaks down your monthly wins by color. In theory, a balanced player should have similar win rates as white and black, but most players have a preference. If you're winning significantly more as one color, consider studying your weaker side's openings. The grouped bars make it easy to spot months where you were particularly strong or weak.`,
  },
  openings: {
    title: 'Opening Performance',
    description: `Analyze your win rate across different openings. The stacked bars show wins, losses, and draws for each opening you've played multiple times. The percentage on the right shows your overall success rate. Use this to identify which openings are working for you and which might need more study. Focus on openings with high game counts but low win rates for the biggest improvement potential.`,
  },
  time: {
    title: 'Time Analysis',
    description: `Discover when you play your best chess! The top chart shows your win rate by hour of day - you might be surprised to find you play better at certain times. The bottom chart shows performance by day of week. Use these insights to schedule your important games during your peak performance windows.`,
  },
  tree: {
    title: 'Opening Repertoire Tree',
    description: `This tree visualization shows the opening moves you play most frequently. Each branch represents a move sequence, with numbers at the end showing how often you've played that line. Use this to understand your opening tendencies and identify gaps in your repertoire. If you always play the same lines, opponents can prepare against you!`,
  },
};

function DashBoard({ plotType, username }) {
  const info = PLOT_DESCRIPTIONS[plotType];

  if (!info) {
    return (
      <div className="dashboard">
        <h1>Welcome to ChessViz</h1>
        <p>
          Analyze your Chess.com games with interactive visualizations. Enter your Chess.com username
          in the menu to get started, or explore the pre-loaded data for the default player.
        </p>
        <div className="dashboard-features">
          <div className="feature">
            <strong>ELO Progression</strong> - Track your rating over time
          </div>
          <div className="feature">
            <strong>Wins by Color</strong> - See if you prefer white or black
          </div>
          <div className="feature">
            <strong>Opening Stats</strong> - Find your best and worst openings
          </div>
          <div className="feature">
            <strong>Time Analysis</strong> - Discover when you play best
          </div>
          <div className="feature">
            <strong>Opening Tree</strong> - Visualize your repertoire
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <h1>{info.title}</h1>
      <p>{info.description}</p>
      {username && (
        <div className="dashboard-player">
          Showing data for: <strong>{username}</strong>
        </div>
      )}
    </div>
  );
}

export default DashBoard;

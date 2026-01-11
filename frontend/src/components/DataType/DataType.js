import React, { useState } from 'react';
import config from '../../config';
import './DataType.css';

const PLOT_OPTIONS = [
  { value: 'elo', label: 'ELO Progression' },
  { value: 'wins', label: 'Wins by Color' },
  { value: 'openings', label: 'Opening Stats' },
  { value: 'time', label: 'Time Analysis' },
  { value: 'tree', label: 'Opening Tree' },
];

function DataType({ onSubmit, onFilterChange, filters, disabled }) {
  const [selectedPlot, setSelectedPlot] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedPlot) {
      onSubmit(selectedPlot);
    }
  };

  const handleTimeClassChange = (e) => {
    const newTimeClass = e.target.value;
    // Reset time control when time class changes
    const newTimeControl = config.TIME_CONTROLS[newTimeClass]?.[0]?.value || '600';
    onFilterChange({
      timeClass: newTimeClass,
      timeControl: newTimeControl,
    });
  };

  const timeControlOptions = config.TIME_CONTROLS[filters.timeClass] || [];

  return (
    <div className="datatype-container">
      <form onSubmit={handleSubmit}>
        {/* Plot Type Selection */}
        <div className="form-group">
          <label htmlFor="plotType">Analysis Type:</label>
          <select
            id="plotType"
            value={selectedPlot}
            onChange={(e) => setSelectedPlot(e.target.value)}
            disabled={disabled}
          >
            <option value="" disabled>Select analysis...</option>
            {PLOT_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>

        {/* Filters */}
        <div className="filters-section">
          <div className="form-group">
            <label htmlFor="timeClass">Time Class:</label>
            <select
              id="timeClass"
              value={filters.timeClass}
              onChange={handleTimeClassChange}
              disabled={disabled}
            >
              <option value="rapid">Rapid</option>
              <option value="blitz">Blitz</option>
              <option value="bullet">Bullet</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="timeControl">Time Control:</label>
            <select
              id="timeControl"
              value={filters.timeControl}
              onChange={(e) => onFilterChange({ timeControl: e.target.value })}
              disabled={disabled}
            >
              {timeControlOptions.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>

          {(selectedPlot === 'openings' || selectedPlot === 'tree') && (
            <div className="form-group">
              <label htmlFor="playerColor">Playing as:</label>
              <select
                id="playerColor"
                value={filters.playerColor}
                onChange={(e) => onFilterChange({ playerColor: e.target.value })}
                disabled={disabled}
              >
                <option value="white">White</option>
                <option value="black">Black</option>
              </select>
            </div>
          )}
        </div>

        <button type="submit" disabled={disabled || !selectedPlot} className="analyze-btn">
          Analyze
        </button>
      </form>
    </div>
  );
}

export default DataType;

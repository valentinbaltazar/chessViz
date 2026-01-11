import React, { useEffect, useState, useCallback } from 'react';
import { EloChart, WinsChart, OpeningStatsChart, TimeAnalysisChart } from '../Charts';
import { Loading, Error } from '../Common';
import TreeDisplay from '../TreePlot/TreePlot';
import {
  getEloData,
  getWinsData,
  getOpeningStats,
  getTimeAnalysis,
} from '../../services/api';
import './DataPlot.css';

function DataPlot({ plotType, username, filters, userLoaded }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    if (!plotType || !username || !userLoaded) return;

    setLoading(true);
    setError(null);

    try {
      let result;
      switch (plotType) {
        case 'elo':
          result = await getEloData(username, filters.timeClass, filters.timeControl);
          break;
        case 'wins':
          result = await getWinsData(username);
          break;
        case 'openings':
          result = await getOpeningStats(
            username,
            filters.timeClass,
            filters.timeControl,
            filters.playerColor
          );
          break;
        case 'time':
          result = await getTimeAnalysis(username, filters.timeClass, filters.timeControl);
          break;
        case 'tree':
          // Tree is handled by TreeDisplay component
          result = { type: 'tree' };
          break;
        default:
          throw new Error('Unknown plot type');
      }
      setData(result);
    } catch (err) {
      setError(err.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  }, [plotType, username, filters, userLoaded]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const renderChart = () => {
    if (!data) return null;

    switch (plotType) {
      case 'elo':
        return <EloChart data={data} />;
      case 'wins':
        return <WinsChart data={data} />;
      case 'openings':
        return <OpeningStatsChart data={data} />;
      case 'time':
        return <TimeAnalysisChart data={data} />;
      case 'tree':
        return (
          <TreeDisplay
            username={username}
            filters={filters}
          />
        );
      default:
        return null;
    }
  };

  // No plot selected
  if (!plotType) {
    return (
      <div className="dataplot-empty">
        <h2>Choose an analysis type to begin</h2>
        <p>Select a player and analysis type from the menu to visualize chess data.</p>
      </div>
    );
  }

  // Loading state
  if (loading) {
    return <Loading message="Analyzing data..." />;
  }

  // Error state
  if (error) {
    return <Error message={error} onRetry={fetchData} />;
  }

  return (
    <div className="dataplot-container">
      {renderChart()}
    </div>
  );
}

export default DataPlot;

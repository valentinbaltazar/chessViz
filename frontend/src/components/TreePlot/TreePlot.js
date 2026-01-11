import React, { useEffect, useState } from 'react';
import { getOpeningTree } from '../../services/api';
import { Loading, Error } from '../Common';
import './TreePlot.css';

function TreeDisplay({ username, filters }) {
  const [tree, setTree] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTree = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await getOpeningTree(
        username,
        filters.timeClass,
        filters.timeControl,
        filters.playerColor,
        2
      );
      setTree(data.tree);
    } catch (err) {
      setError(err.message || 'Failed to load opening tree');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (username) {
      fetchTree();
    }
  }, [username, filters]);

  if (loading) {
    return <Loading message="Building opening tree..." />;
  }

  if (error) {
    return <Error message={error} onRetry={fetchTree} />;
  }

  return (
    <div className="tree-container">
      <div className="tree-header">
        <h2>Opening Repertoire Tree</h2>
        <p className="tree-subtitle">
          Playing as <strong>{filters.playerColor}</strong> |
          {filters.timeClass} ({filters.timeControl}s)
        </p>
      </div>
      <div className="tree-content">
        <pre>{tree || 'No opening data available'}</pre>
      </div>
      <div className="tree-legend">
        <p>Numbers at leaf nodes indicate how many times that line was played.</p>
      </div>
    </div>
  );
}

export default TreeDisplay;

import React, { useState } from 'react';
import { fetchUser, checkUser } from '../../services/api';
import { Loading } from '../Common';
import './ToolBar.css';

function Toolbar({ onUserChange, currentUser }) {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'success' or 'error'

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username.trim()) {
      setMessage('Please enter a username');
      setMessageType('error');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      // First check if user data already exists
      const checkResult = await checkUser(username);

      if (checkResult.exists) {
        setMessage(`Data loaded for ${username}`);
        setMessageType('success');
        onUserChange(username.toLowerCase(), true);
      } else {
        // Need to fetch user data
        setMessage('Fetching games from Chess.com...');
        setMessageType('info');

        const result = await fetchUser(username);
        setMessage(result.message);
        setMessageType('success');
        onUserChange(username.toLowerCase(), true);
      }
    } catch (error) {
      setMessage(error.message || 'Failed to load user data');
      setMessageType('error');
      onUserChange(username.toLowerCase(), false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="toolbar-container">
      <form onSubmit={handleSubmit} className="toolbar-form">
        <div className="form-group">
          <label htmlFor="username">Chess.com Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter username"
            disabled={loading}
          />
        </div>
        <button type="submit" disabled={loading} className="fetch-btn">
          {loading ? 'Loading...' : 'Load Player'}
        </button>
      </form>

      {loading && <Loading message="Fetching player data..." />}

      {message && !loading && (
        <div className={`message ${messageType}`}>
          {message}
        </div>
      )}

      <div className="current-user">
        <strong>Current Player:</strong> {currentUser}
      </div>
    </div>
  );
}

export default Toolbar;

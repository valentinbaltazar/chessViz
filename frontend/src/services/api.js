// API service for ChessViz backend
import config from '../config';

const API_URL = config.API_URL;

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new ApiError(error.detail || 'Request failed', response.status);
  }
  return response.json();
}

// User management
export async function fetchUser(username) {
  const response = await fetch(`${API_URL}/api/fetch-user`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username }),
  });
  return handleResponse(response);
}

export async function checkUser(username) {
  const response = await fetch(`${API_URL}/api/check-user/${encodeURIComponent(username)}`);
  return handleResponse(response);
}

export async function getPlayerStats(username) {
  const response = await fetch(`${API_URL}/api/player-stats/${encodeURIComponent(username)}`);
  return handleResponse(response);
}

// Chart data
export async function getEloData(username, timeClass, timeControl) {
  const params = new URLSearchParams({
    username,
    time_class: timeClass,
    time_control: timeControl,
  });
  const response = await fetch(`${API_URL}/api/elo-data?${params}`);
  return handleResponse(response);
}

export async function getWinsData(username) {
  const params = new URLSearchParams({ username });
  const response = await fetch(`${API_URL}/api/wins-data?${params}`);
  return handleResponse(response);
}

export async function getOpeningStats(username, timeClass, timeControl, playerColor) {
  const params = new URLSearchParams({
    username,
    time_class: timeClass,
    time_control: timeControl,
    player_color: playerColor,
  });
  const response = await fetch(`${API_URL}/api/opening-stats?${params}`);
  return handleResponse(response);
}

export async function getTimeAnalysis(username, timeClass, timeControl) {
  const params = new URLSearchParams({
    username,
    time_class: timeClass,
    time_control: timeControl,
  });
  const response = await fetch(`${API_URL}/api/time-analysis?${params}`);
  return handleResponse(response);
}

export async function getOpeningTree(username, timeClass, timeControl, playerColor, maxDepth = 2) {
  const params = new URLSearchParams({
    username,
    time_class: timeClass,
    time_control: timeControl,
    player_color: playerColor,
    max_depth: maxDepth.toString(),
  });
  const response = await fetch(`${API_URL}/api/opening-tree?${params}`);
  return handleResponse(response);
}

export { ApiError };

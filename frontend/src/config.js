// Frontend configuration
const config = {
  // API URL - uses environment variable or defaults to localhost
  API_URL: process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000',

  // Default settings
  DEFAULT_TIME_CLASS: 'rapid',
  DEFAULT_TIME_CONTROL: '600',
  DEFAULT_USERNAME: 'river650',

  // Time control options
  TIME_CONTROLS: {
    rapid: [
      { value: '600', label: '10 min' },
      { value: '900', label: '15 min' },
      { value: '1800', label: '30 min' },
    ],
    blitz: [
      { value: '180', label: '3 min' },
      { value: '300', label: '5 min' },
    ],
    bullet: [
      { value: '60', label: '1 min' },
      { value: '120', label: '2 min' },
    ],
  },

  // Chart colors
  COLORS: {
    primary: '#4CAF50',
    secondary: '#2196F3',
    white: '#f0f0f0',
    black: '#333333',
    win: '#4CAF50',
    loss: '#f44336',
    draw: '#9e9e9e',
    background: 'rgb(24, 26, 27)',
    paper: 'rgb(42, 45, 47)',
    text: '#ffffff',
  },
};

export default config;

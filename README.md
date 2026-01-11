# ChessViz - Chess Game Analytics Dashboard

A full-stack web application that visualizes and analyzes chess game data from Chess.com. Built as a personal project to combine my passion for chess with software engineering and data analysis skills.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.3-61DAFB?style=flat&logo=react&logoColor=black)
![Plotly](https://img.shields.io/badge/Plotly.js-2.27-3F4F75?style=flat&logo=plotly&logoColor=white)

## Overview

ChessViz fetches a player's complete game history from the Chess.com public API, processes the data, and generates interactive visualizations that reveal patterns in playing performance. The dashboard helps players understand their strengths, weaknesses, and trends over time.

### Key Features

- **ELO Progression Tracking** - Line chart showing rating changes over time with hover details for each game (opponent, result, rating change)
- **Win/Loss Analysis by Color** - Monthly breakdown of performance playing as white vs black pieces
- **Opening Repertoire Statistics** - Win rates for each opening, helping identify which openings perform best
- **Time-Based Performance** - Discover peak playing hours and best days of the week
- **Opening Tree Visualization** - Hierarchical view of most-played opening move sequences

## Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | REST API framework with automatic OpenAPI documentation |
| **Pandas** | Data manipulation, aggregation, and CSV storage |
| **python-chess** | PGN parsing and opening move extraction |
| **anytree** | Building hierarchical opening repertoire trees |
| **Requests** | Chess.com API integration with error handling |
| **pytest** | Unit and integration testing |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | Component-based UI with functional components and hooks |
| **Plotly.js** | Interactive charts with hover, zoom, and pan |
| **Custom Hooks** | Reusable `useFetch` hook for loading/error state management |
| **CSS3** | Dark theme UI with responsive Flexbox layout |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                        │
├─────────────────────────────────────────────────────────────────┤
│  TopHalf (State Container)                                      │
│  ├── Toolbar        → User input & player selection             │
│  ├── DataType       → Analysis type & filter controls           │
│  ├── DataPlot       → Chart container with loading states       │
│  │   └── Plotly Charts (ELO, Wins, Openings, Time Analysis)    │
│  └── DashBoard      → Educational descriptions                  │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTP
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                          │
├─────────────────────────────────────────────────────────────────┤
│  viz_api.py         → REST endpoints & request validation       │
│  profile_plots.py   → Data processing & analysis functions      │
│  opening_tree.py    → Hierarchical move tree builder            │
│  pub_api.py         → Chess.com API client                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Layer                                   │
├─────────────────────────────────────────────────────────────────┤
│  player_data/*.csv  → Cached game archives (JSON in CSV)        │
│  Chess.com API      → External data source                      │
└─────────────────────────────────────────────────────────────────┘
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/fetch-user` | POST | Download & cache player's games from Chess.com |
| `/api/check-user/{username}` | GET | Check if user data exists locally |
| `/api/player-stats/{username}` | GET | Summary statistics (games, date range) |
| `/api/elo-data` | GET | ELO progression with opponent details |
| `/api/wins-data` | GET | Monthly wins/losses by color |
| `/api/opening-stats` | GET | Win rates by opening repertoire |
| `/api/time-analysis` | GET | Performance by hour and day of week |
| `/api/opening-tree` | GET | Opening move tree structure |

All chart endpoints support filtering by `time_class` (rapid, blitz, bullet) and `time_control` (600, 900, etc.).

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Start the FastAPI server
python backend/viz_api.py
```

The API runs at `http://127.0.0.1:8000` with interactive docs at `/docs`.

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The React app runs at `http://localhost:3000`.

### Running Tests

```bash
# Backend tests
cd backend
pytest test_api.py -v

# Frontend tests
cd frontend
npm test
```

## Data Analysis Techniques

### ELO Progression
Parses PGN game records to extract player ratings, opponent ratings, and game results. Plots time-series data with custom hover templates showing match details.

### Win Rate Calculations
Aggregates game outcomes by month, separating results by player color (white/black). Calculates percentages for wins, losses, and draws across different time controls.

### Opening Statistics
Uses `python-chess` to parse PGN headers and extract ECO opening names. Groups games by opening, calculates win rates, and filters to show only openings played 3+ times.

### Time-Based Analysis
Converts Unix timestamps to local time, groups games by hour and day of week, and calculates performance metrics to identify optimal playing times.

### Opening Tree
Builds a hierarchical tree structure using the `anytree` library. Tracks move frequencies at each depth level, enabling visualization of a player's most common opening sequences.

## Project Structure

```
chessViz/
├── backend/
│   ├── viz_api.py          # FastAPI application & routes
│   ├── profile_plots.py    # Data processing functions
│   ├── opening_tree.py     # Tree builder for openings
│   ├── pub_api.py          # Chess.com API client
│   ├── config.py           # Environment configuration
│   ├── test_api.py         # pytest test suite
│   ├── requirements.txt    # Python dependencies
│   └── player_data/        # Cached CSV files
│
├── frontend/
│   ├── src/
│   │   ├── App.js          # Root component
│   │   ├── config.js       # Frontend configuration
│   │   ├── services/
│   │   │   └── api.js      # API client functions
│   │   ├── hooks/
│   │   │   └── useFetch.js # Custom fetch hook
│   │   └── components/
│   │       ├── TopHalf/    # Main state container
│   │       ├── ToolBar/    # User input
│   │       ├── DataType/   # Analysis selection
│   │       ├── DataPlot/   # Chart container
│   │       ├── DashBoard/  # Descriptions
│   │       ├── TreePlot/   # Opening tree display
│   │       ├── Charts/     # Plotly components
│   │       └── Common/     # Loading, Error
│   └── package.json
│
└── README.md
```

## What I Learned

Building ChessViz taught me practical skills across the full stack:

**Backend Development**
- Designing RESTful APIs with FastAPI including request validation and error handling
- Working with external APIs (Chess.com) including rate limiting and error recovery
- Data processing with Pandas for aggregation, filtering, and transformation
- PGN parsing and chess-specific data structures

**Frontend Development**
- Building component-based UIs with React functional components and hooks
- Creating custom hooks for reusable stateful logic
- Implementing interactive data visualizations with Plotly.js
- State management patterns in React (lifting state up)

**Data Analysis**
- Time-series analysis for ELO progression
- Statistical aggregation for win/loss metrics
- Tree data structures for opening analysis
- Filtering and grouping large datasets

**Software Engineering Practices**
- Separation of concerns (API layer, data processing, UI components)
- Error handling and loading states for better UX
- Configuration management for different environments
- Writing tests for API endpoints

## Future Improvements

- [ ] Add user authentication to save preferences
- [ ] Implement game replay with board visualization
- [ ] Add comparative analysis between players
- [ ] Include Stockfish engine analysis for game accuracy scores
- [ ] Deploy to cloud platform (AWS/GCP)

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with passion for chess and software engineering*

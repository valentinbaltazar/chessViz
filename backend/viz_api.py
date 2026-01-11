"""API to serve chess analysis data and visualizations"""
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from config import API_HOST, API_PORT, CORS_ORIGINS
from profile_plots import (
    get_elo_data,
    get_wins_data,
    get_opening_stats,
    get_time_analysis,
    save_all_games,
    get_player_stats,
    player_data_exists,
    DataError
)
from opening_tree import get_tree

app = FastAPI(
    title="ChessViz API",
    description="API for analyzing and visualizing Chess.com game data",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FetchUserRequest(BaseModel):
    username: str


class UserResponse(BaseModel):
    status: str
    message: str
    username: Optional[str] = None
    total_games: Optional[int] = None


# --- User Management Endpoints ---

@app.post("/api/fetch-user", response_model=UserResponse)
async def fetch_user(request: FetchUserRequest):
    """Fetch and store game data for a Chess.com user.

    This downloads all available games from Chess.com API and stores them locally.
    """
    username = request.username.strip().lower()
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    try:
        result = save_all_games(username)
        return UserResponse(
            status=result['status'],
            message=result['message'],
            username=username,
            total_games=result.get('total_games')
        )
    except DataError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/check-user/{username}")
async def check_user(username: str):
    """Check if a user's data exists locally."""
    username = username.strip().lower()
    exists = player_data_exists(username)
    return {"exists": exists, "username": username}


@app.get("/api/player-stats/{username}")
async def player_stats(username: str):
    """Get summary statistics for a player."""
    username = username.strip().lower()
    try:
        stats = get_player_stats(username)
        return stats
    except DataError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --- Chart Data Endpoints ---

@app.get("/api/elo-data")
async def elo_data(
    username: str = Query(..., description="Chess.com username"),
    time_class: str = Query("rapid", description="Time class: rapid, blitz, bullet"),
    time_control: str = Query("600", description="Time control in seconds")
):
    """Get ELO progression data for interactive chart."""
    username = username.strip().lower()
    try:
        data = get_elo_data(username, time_class, time_control)
        return data
    except DataError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/wins-data")
async def wins_data(
    username: str = Query(..., description="Chess.com username")
):
    """Get wins/losses by color data for interactive chart."""
    username = username.strip().lower()
    try:
        data = get_wins_data(username)
        return data
    except DataError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/opening-stats")
async def opening_stats(
    username: str = Query(..., description="Chess.com username"),
    time_class: str = Query("rapid", description="Time class"),
    time_control: str = Query("600", description="Time control"),
    player_color: str = Query("white", description="white or black")
):
    """Get opening win rate statistics."""
    username = username.strip().lower()
    try:
        data = get_opening_stats(username, time_class, time_control, player_color)
        return data
    except DataError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/time-analysis")
async def time_analysis(
    username: str = Query(..., description="Chess.com username"),
    time_class: str = Query("rapid", description="Time class"),
    time_control: str = Query("600", description="Time control")
):
    """Get performance by time of day and day of week."""
    username = username.strip().lower()
    try:
        data = get_time_analysis(username, time_class, time_control)
        return data
    except DataError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/opening-tree")
async def opening_tree(
    username: str = Query(..., description="Chess.com username"),
    time_class: str = Query("rapid", description="Time class"),
    time_control: str = Query("600", description="Time control"),
    player_color: str = Query("white", description="white or black"),
    max_depth: int = Query(2, description="Max depth of tree")
):
    """Get opening repertoire tree structure."""
    username = username.strip().lower()
    try:
        tree = get_tree(username, time_class, time_control, player_color, max_depth)
        return {"tree": tree, "username": username, "player_color": player_color}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# --- Legacy endpoint for backwards compatibility ---

@app.get("/get-plot")
async def get_plot(option: str):
    """Legacy endpoint - redirects to new API.

    Maintained for backwards compatibility.
    """
    if option == 'Option 3':
        tree = get_tree()
        return {"tree": tree}
    else:
        # For options 1 and 2, return data for Plotly instead of PNG
        if option == 'Option 1':
            try:
                data = get_elo_data('river650', 'rapid', '1800')
                return data
            except DataError as e:
                raise HTTPException(status_code=404, detail=str(e))
        elif option == 'Option 2':
            try:
                data = get_wins_data('river650')
                return data
            except DataError as e:
                raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail="Invalid option")


@app.get("/")
async def root():
    """API health check and info."""
    return {
        "name": "ChessViz API",
        "version": "2.0.0",
        "docs": "/docs",
        "endpoints": [
            "/api/fetch-user",
            "/api/check-user/{username}",
            "/api/player-stats/{username}",
            "/api/elo-data",
            "/api/wins-data",
            "/api/opening-stats",
            "/api/time-analysis",
            "/api/opening-tree"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)

"""Backend configuration - environment variables and settings"""
import os

# API Configuration
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))

# CORS - allowed origins (comma-separated in env var)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Chess.com API settings
CHESS_API_EMAIL = os.getenv("CHESS_API_EMAIL", "valentin.urena@gmail.com")
CHESS_API_USERNAME = os.getenv("CHESS_API_USERNAME", "river650")
USER_AGENT = f"username: {CHESS_API_USERNAME}, email: {CHESS_API_EMAIL}"

# Data storage
DATA_DIR = os.getenv("DATA_DIR", "./player_data")

# Default analysis settings
DEFAULT_TIME_CLASS = os.getenv("DEFAULT_TIME_CLASS", "rapid")
DEFAULT_TIME_CONTROL = os.getenv("DEFAULT_TIME_CONTROL", "600")

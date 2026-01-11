"""Get different endpoints from PubAPI chess.com"""
import requests
from config import USER_AGENT

class ChessAPIError(Exception):
    """Custom exception for Chess.com API errors"""
    pass


def get_headers():
    """Return headers for Chess.com API requests"""
    return {'User-Agent': USER_AGENT}


def player_profile(username):
    """Get player profile information from Chess.com"""
    url = f"https://api.chess.com/pub/player/{username}"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise ChessAPIError(f"Player '{username}' not found on Chess.com")
        raise ChessAPIError(f"Chess.com API error: {e}")
    except requests.exceptions.RequestException as e:
        raise ChessAPIError(f"Network error: {e}")


def games_archive_list(username):
    """Get array of monthly archives available for this player."""
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise ChessAPIError(f"Player '{username}' not found or has no games")
        raise ChessAPIError(f"Chess.com API error: {e}")
    except requests.exceptions.RequestException as e:
        raise ChessAPIError(f"Network error: {e}")


def games_by_month(username, year, month):
    """Get array of games that a player has finished for a specific month.

    Args:
        username: Chess.com username
        year: Four digit year (YYYY)
        month: Two digit month (MM)

    Returns:
        Dict containing games array
    """
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise ChessAPIError(f"Chess.com API error: {e}")
    except requests.exceptions.RequestException as e:
        raise ChessAPIError(f"Network error: {e}")


def game_url(game_url):
    """Fetch game data from a Chess.com archive URL.

    Args:
        game_url: Full URL to a monthly archive

    Returns:
        Dict containing games array
    """
    try:
        response = requests.get(game_url, headers=get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise ChessAPIError(f"Chess.com API error: {e}")
    except requests.exceptions.RequestException as e:
        raise ChessAPIError(f"Network error: {e}")


if __name__ == '__main__':
    # Test the API functions
    try:
        profile = player_profile('river650')
        print(f"Profile: {profile.get('username', 'Unknown')}")

        archives = games_archive_list('river650')
        print(f"Archives available: {len(archives.get('archives', []))}")
    except ChessAPIError as e:
        print(f"Error: {e}")

"""Data processing and analysis for chess games"""
import pandas as pd
import numpy as np
import json
import os
import datetime
from collections import defaultdict

from pub_api import games_archive_list, game_url, ChessAPIError
from config import DATA_DIR


class DataError(Exception):
    """Custom exception for data processing errors"""
    pass


def get_player_file_path(username):
    """Get the file path for a player's data file"""
    return os.path.join(DATA_DIR, f'{username}.csv')


def player_data_exists(username):
    """Check if player data file exists"""
    return os.path.exists(get_player_file_path(username))


def get_elo(game):
    """Return elo info for given players from Game object"""
    end_time = game['end_time']
    end_date = datetime.datetime.fromtimestamp(end_time)
    date = end_date.strftime('%Y-%m-%d')

    white_player = game['white']['username']
    white_elo = game['white']['rating']
    black_player = game['black']['username']
    black_elo = game['black']['rating']

    return {
        'white_player': white_player,
        'white_elo': white_elo,
        'black_player': black_player,
        'black_elo': black_elo,
        'end_date': date
    }


def load_games(username, time_class=None, time_control=None):
    """Load and optionally filter games for a user.

    Args:
        username: Chess.com username
        time_class: Filter by time class (e.g., 'rapid', 'blitz')
        time_control: Filter by time control (e.g., '600', '1800')

    Returns:
        List of game objects
    """
    file_path = get_player_file_path(username)
    if not os.path.exists(file_path):
        raise DataError(f"No data found for player '{username}'. Please fetch their data first.")

    df = pd.read_csv(file_path)
    all_games = []

    for game_obj in df['games_obj']:
        game_obj_json = json.loads(game_obj)
        for game in game_obj_json['games']:
            # Apply filters if specified
            if time_class and game.get('time_class') != time_class:
                continue
            if time_control and game.get('time_control') != time_control:
                continue
            all_games.append(game)

    return all_games


def get_elo_data(username, time_class='rapid', time_control='600'):
    """Get ELO progression data for Plotly chart.

    Returns:
        Dict with dates, elos, and metadata for interactive chart
    """
    games = load_games(username, time_class, time_control)

    if not games:
        return {'dates': [], 'elos': [], 'opponents': [], 'results': []}

    elo_data = []
    for game in games:
        elo_info = get_elo(game)
        is_white = elo_info['white_player'].lower() == username.lower()
        player_elo = elo_info['white_elo'] if is_white else elo_info['black_elo']
        opponent = elo_info['black_player'] if is_white else elo_info['white_player']
        opponent_elo = elo_info['black_elo'] if is_white else elo_info['white_elo']

        # Get result
        color = 'white' if is_white else 'black'
        result = game[color].get('result', 'unknown')

        elo_data.append({
            'date': elo_info['end_date'],
            'elo': player_elo,
            'opponent': opponent,
            'opponent_elo': opponent_elo,
            'result': result
        })

    # Sort by date
    elo_data.sort(key=lambda x: x['date'])

    return {
        'dates': [d['date'] for d in elo_data],
        'elos': [d['elo'] for d in elo_data],
        'opponents': [d['opponent'] for d in elo_data],
        'opponent_elos': [d['opponent_elo'] for d in elo_data],
        'results': [d['result'] for d in elo_data],
        'username': username,
        'time_class': time_class,
        'time_control': time_control,
        'total_games': len(elo_data)
    }


def get_wins_data(username):
    """Get wins by color data for Plotly chart.

    Returns:
        Dict with monthly wins data for interactive chart
    """
    file_path = get_player_file_path(username)
    if not os.path.exists(file_path):
        raise DataError(f"No data found for player '{username}'")

    df = pd.read_csv(file_path)
    monthly_data = defaultdict(lambda: {'wins_white': 0, 'wins_black': 0, 'losses_white': 0, 'losses_black': 0, 'draws_white': 0, 'draws_black': 0})

    for game_obj in df['games_obj']:
        game_obj_json = json.loads(game_obj)
        for game in game_obj_json['games']:
            end_time = game['end_time']
            end_date = datetime.datetime.fromtimestamp(end_time)
            month_key = end_date.strftime('%Y-%m')

            is_white = game['white']['username'].lower() == username.lower()
            color = 'white' if is_white else 'black'
            result = game[color].get('result', '')

            if result == 'win':
                monthly_data[month_key][f'wins_{color}'] += 1
            elif result in ['checkmated', 'timeout', 'resigned', 'abandoned']:
                monthly_data[month_key][f'losses_{color}'] += 1
            else:
                monthly_data[month_key][f'draws_{color}'] += 1

    # Sort by month
    sorted_months = sorted(monthly_data.keys())

    return {
        'months': sorted_months,
        'wins_white': [monthly_data[m]['wins_white'] for m in sorted_months],
        'wins_black': [monthly_data[m]['wins_black'] for m in sorted_months],
        'losses_white': [monthly_data[m]['losses_white'] for m in sorted_months],
        'losses_black': [monthly_data[m]['losses_black'] for m in sorted_months],
        'draws_white': [monthly_data[m]['draws_white'] for m in sorted_months],
        'draws_black': [monthly_data[m]['draws_black'] for m in sorted_months],
        'username': username
    }


def get_opening_stats(username, time_class='rapid', time_control='600', player_color='white'):
    """Get win rate by opening for Plotly chart.

    Returns:
        Dict with opening names and win rates
    """
    import chess.pgn
    from io import StringIO

    games = load_games(username, time_class, time_control)

    opening_stats = defaultdict(lambda: {'wins': 0, 'losses': 0, 'draws': 0, 'total': 0})

    for game in games:
        is_white = game['white']['username'].lower() == username.lower()
        if (player_color == 'white' and not is_white) or (player_color == 'black' and is_white):
            continue

        pgn_str = game.get('pgn', '')
        if not pgn_str:
            continue

        # Parse PGN to get opening name
        try:
            pgn_game = chess.pgn.read_game(StringIO(pgn_str))
            if pgn_game is None:
                continue
            opening = pgn_game.headers.get('ECOUrl', 'Unknown')
            # Extract opening name from URL
            if opening != 'Unknown' and '/' in opening:
                opening = opening.split('/')[-1].replace('-', ' ').title()
        except Exception:
            opening = 'Unknown'

        # Get result
        color = 'white' if is_white else 'black'
        result = game[color].get('result', '')

        opening_stats[opening]['total'] += 1
        if result == 'win':
            opening_stats[opening]['wins'] += 1
        elif result in ['checkmated', 'timeout', 'resigned', 'abandoned']:
            opening_stats[opening]['losses'] += 1
        else:
            opening_stats[opening]['draws'] += 1

    # Calculate win rates and sort by total games
    openings_data = []
    for opening, stats in opening_stats.items():
        if stats['total'] >= 3:  # Only include openings played at least 3 times
            win_rate = (stats['wins'] / stats['total']) * 100 if stats['total'] > 0 else 0
            openings_data.append({
                'opening': opening[:30],  # Truncate long names
                'wins': stats['wins'],
                'losses': stats['losses'],
                'draws': stats['draws'],
                'total': stats['total'],
                'win_rate': round(win_rate, 1)
            })

    # Sort by total games played
    openings_data.sort(key=lambda x: x['total'], reverse=True)

    return {
        'openings': [d['opening'] for d in openings_data[:15]],  # Top 15
        'wins': [d['wins'] for d in openings_data[:15]],
        'losses': [d['losses'] for d in openings_data[:15]],
        'draws': [d['draws'] for d in openings_data[:15]],
        'totals': [d['total'] for d in openings_data[:15]],
        'win_rates': [d['win_rate'] for d in openings_data[:15]],
        'username': username,
        'player_color': player_color
    }


def get_time_analysis(username, time_class='rapid', time_control='600'):
    """Get performance by time of day/day of week.

    Returns:
        Dict with hourly and daily performance data
    """
    games = load_games(username, time_class, time_control)

    hourly_stats = defaultdict(lambda: {'wins': 0, 'total': 0})
    daily_stats = defaultdict(lambda: {'wins': 0, 'total': 0})

    for game in games:
        end_time = game['end_time']
        end_datetime = datetime.datetime.fromtimestamp(end_time)
        hour = end_datetime.hour
        day = end_datetime.strftime('%A')

        is_white = game['white']['username'].lower() == username.lower()
        color = 'white' if is_white else 'black'
        result = game[color].get('result', '')

        hourly_stats[hour]['total'] += 1
        daily_stats[day]['total'] += 1

        if result == 'win':
            hourly_stats[hour]['wins'] += 1
            daily_stats[day]['wins'] += 1

    # Calculate win rates
    hours = list(range(24))
    hourly_win_rates = []
    hourly_games = []
    for h in hours:
        stats = hourly_stats[h]
        win_rate = (stats['wins'] / stats['total'] * 100) if stats['total'] > 0 else 0
        hourly_win_rates.append(round(win_rate, 1))
        hourly_games.append(stats['total'])

    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_win_rates = []
    daily_games = []
    for d in days_order:
        stats = daily_stats[d]
        win_rate = (stats['wins'] / stats['total'] * 100) if stats['total'] > 0 else 0
        daily_win_rates.append(round(win_rate, 1))
        daily_games.append(stats['total'])

    return {
        'hours': hours,
        'hourly_win_rates': hourly_win_rates,
        'hourly_games': hourly_games,
        'days': days_order,
        'daily_win_rates': daily_win_rates,
        'daily_games': daily_games,
        'username': username
    }


def save_all_games(username):
    """Download and save all games for a user from Chess.com.

    Args:
        username: Chess.com username

    Returns:
        Dict with status and game count
    """
    file_path = get_player_file_path(username)

    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(file_path):
        return {'status': 'exists', 'message': f'Data already exists for {username}'}

    try:
        all_games_url = games_archive_list(username)
    except ChessAPIError as e:
        raise DataError(str(e))

    all_games_info = []
    total_games = 0

    for games_url in all_games_url.get('archives', []):
        try:
            data = game_url(games_url)
            games_json = json.dumps(data)
            all_games_info.append({'url': games_url, 'games_obj': games_json})
            total_games += len(data.get('games', []))
        except ChessAPIError as e:
            # Continue with other archives even if one fails
            continue

    if not all_games_info:
        raise DataError(f"Could not fetch any games for {username}")

    df = pd.DataFrame(all_games_info)
    df.to_csv(file_path, index=False)

    return {
        'status': 'success',
        'message': f'Downloaded {total_games} games for {username}',
        'total_games': total_games,
        'archives': len(all_games_info)
    }


def get_player_stats(username):
    """Get summary statistics for a player.

    Returns:
        Dict with overall stats
    """
    file_path = get_player_file_path(username)
    if not os.path.exists(file_path):
        raise DataError(f"No data found for player '{username}'")

    df = pd.read_csv(file_path)
    total_games = 0
    time_classes = defaultdict(int)
    first_game = None
    last_game = None

    for game_obj in df['games_obj']:
        game_obj_json = json.loads(game_obj)
        for game in game_obj_json['games']:
            total_games += 1
            time_classes[game.get('time_class', 'unknown')] += 1

            end_time = game['end_time']
            if first_game is None or end_time < first_game:
                first_game = end_time
            if last_game is None or end_time > last_game:
                last_game = end_time

    return {
        'username': username,
        'total_games': total_games,
        'time_classes': dict(time_classes),
        'first_game': datetime.datetime.fromtimestamp(first_game).strftime('%Y-%m-%d') if first_game else None,
        'last_game': datetime.datetime.fromtimestamp(last_game).strftime('%Y-%m-%d') if last_game else None,
        'archives': len(df)
    }


if __name__ == '__main__':
    # Test functions
    try:
        stats = get_player_stats('river650')
        print(f"Stats: {stats}")

        elo_data = get_elo_data('river650', 'rapid', '1800')
        print(f"ELO data points: {len(elo_data['dates'])}")
    except DataError as e:
        print(f"Error: {e}")

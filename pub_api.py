"""Get different endpoints from PubAPI chess.com"""
import requests


def player_profile(username):
    url = "https://api.chess.com/pub/player/{username}".format(username=username)
    response = requests.get(url, headers = {'User-Agent': 'username: river650, email: valentin.urena@gmail.com'})

    data = response.json()

    print(data)


def monthly_archive_list(username):
    """Description: Array of monthly archives available for this player."""
    url = "https://api.chess.com/pub/player/{username}/games/archives".format(username=username)
    response = requests.get(url, headers = {'User-Agent': 'username: river650, email: valentin.urena@gmail.com'})

    data = response.json()

    print(data)


def games_by_month(username, year, month):
    """Description: Array of Live and Daily Chess games that a player has finished.
        URL pattern: https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}

        "YYYY" is the four digit year of the game-end
        "MM" is the two-digit month"""
    
    url = "https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}".format(username=username, YYYY=year, MM=month)
    response = requests.get(url, headers = {'User-Agent': 'username: river650, email: valentin.urena@gmail.com'})

    data = response.json()

    print(data)


# player_profile('river650')
monthly_archive_list('river650')
# games_by_month('river650', '2024', '07')


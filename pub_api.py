"""Get different endpoints from PubAPI chess.com"""
import requests
import json
import datetime

def player_profile(username):
    url = "https://api.chess.com/pub/player/{username}".format(username=username)
    response = requests.get(url, headers = {'User-Agent': 'username: river650, email: valentin.urena@gmail.com'})

    data = response.json()

    print(data)


def games_archive_list(username):
    """Description: Array of monthly archives available for this player."""
    url = "https://api.chess.com/pub/player/{username}/games/archives".format(username=username)
    response = requests.get(url, headers = {'User-Agent': 'username: river650, email: valentin.urena@gmail.com'})

    data = response.json()

    # print(data)

    return data


def games_by_month(username, year, month):
    """Description: Array of Live and Daily Chess games that a player has finished.
        URL pattern: https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}

        "YYYY" is the four digit year of the game-end
        "MM" is the two-digit month"""
    
    url = "https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}".format(username=username, YYYY=year, MM=month)
    response = requests.get(url, headers = {'User-Agent': 'username: river650, email: valentin.urena@gmail.com'})

    data = response.json()

    print(data)


def game_url(game_url):
    """Url will return a Game object"""
    # print(game_url)
    response = requests.get(game_url, headers = {'User-Agent': 'username: river650, email: valentin.urena@gmail.com'})
    data = response.json()

    # print(type(data))

    print(json.dumps(data, indent=4))
    pgn = data['games'][0]['pgn']
    # print(pgn)

    return data



if __name__ == '__main__':
    # player_profile('river650')
    all_games = games_archive_list('river650')
    example = game_url(all_games['archives'][0])
    # get_elo(example)
    # games_by_month('river650', '2024', '07')


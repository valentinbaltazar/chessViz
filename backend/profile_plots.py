"""Basic plots with matplot.lib for user games data"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pprint

import json
import os
import datetime
import io

from pub_api import games_archive_list, game_url

# USERNAME = 'river650'


def get_elo(game):
    """Return elo for given players from Game object data point"""
    # print("Game data here")
    # print(game)
    end_time = game['end_time']
    end_date = datetime.datetime.fromtimestamp(end_time)
    date = end_date.strftime('%Y-%m-%d')

    white_player, white_elo = game['white']['username'], game['white']['rating']
    black_player, black_elo = game['black']['username'], game['black']['rating']

    # print(white_player, white_elo)
    # print(black_player, black_elo)
    # print(date)

    return {'white_player': white_player,'white_elo': white_elo,'black_player': black_player,'black_elo': black_elo,'end_date': date}

def plot_elo(user_name='river650', time_class='rapid', time_control='600',  testing=False):
    """From player df plot elo vs time"""
    file_path = './player_data/{user_name}.csv'.format(user_name=user_name)
    df = pd.read_csv(file_path)
    elo_info = []
    for game_obj in df['games_obj']:
        # print(game_obj)

        game_obj_json = json.loads(game_obj)

        for game in game_obj_json['games']:
            if (game['time_class']==time_class) and (game['time_control']==time_control):
                elo = get_elo(game)
                elo_info.append(elo)

    elo_df = pd.DataFrame(elo_info)
    elo_df['player_elo'] = np.where(elo_df['white_player']==user_name, elo_df['white_elo'], elo_df['black_elo'])

    elo_df['date'] = pd.to_datetime(elo_df['end_date'])

    # Seaborn density plot
    sns.set_theme(style='whitegrid')
    plot = sns.jointplot(x='date', y='player_elo', data=elo_df, kind='kde', fill=True, color='b')

    plot.set_axis_labels('Date', 'ELO Rating')
    # plot.figure.suptitle('ELO Rating vs Time', y=1.02)
    plot.figure.set_size_inches(12, 8)
    plt.xticks(rotation=45)

    if testing:
        plt.show()

    fig = plot.figure

    return fig


def save_all_games(user_name='river650'):
    """Save all of the users Game objects from archives"""
    file_path = './player_data/{user_name}.csv'.format(user_name=user_name)

    if os.path.exists(file_path):
        print("Game File for this player already exist")
        return None
    
    all_games_url = games_archive_list(user_name)
    all_games_info = []

    for games_url in all_games_url['archives']:
        print(games_url)
        data = game_url(games_url)
        games = json.dumps(data)

        all_games_info.append({'url':games_url, 'games_obj':games})
        
    df = pd.DataFrame(all_games_info)

    print(df.head())

    # return df
    df.to_csv(file_path)


def get_wins(user_name='river650', games_obj=None):
    """Return total number of wins for given player from Games object"""
    # Keep totals
    wins_as_white = 0
    wins_as_black = 0
    # print(games_obj)
    # return None

    for game in games_obj['games']:
        end_time = game['end_time']
        end_date = datetime.datetime.fromtimestamp(end_time)
        date = end_date.strftime('%Y-%m')

        wins_as_white += np.where((game['white']['username']==user_name) and (game['white']['result']=='win'), 1, 0)
        wins_as_black += np.where((game['black']['username']==user_name) and (game['black']['result']=='win'), 1, 0)


    return {'wins_as_white': wins_as_white, 'wins_as_black': wins_as_black, 'end_date': date}

def plot_wins(user_name='river650'):
    file_path = './player_data/{user_name}.csv'.format(user_name=user_name)
    df = pd.read_csv(file_path)

    wins_data = []

    for game_obj in df['games_obj']:
        # print(game_obj)

        game_obj_json = json.loads(game_obj)
        wins_data.append(get_wins(user_name, game_obj_json))

    wins_df = pd.DataFrame(wins_data)
    print(wins_df.head(20))
        
    # Melt the DataFrame to make it suitable for Seaborn
    df_melted = wins_df.melt(id_vars='end_date', value_vars=['wins_as_black', 'wins_as_white'],
                        var_name='Color', value_name='Wins')

    # Create the bar plot
    # plt.figure(figsize=(10, 6))
    sns.set_theme(style='whitegrid')
    plot = sns.barplot(data=df_melted, x='end_date', y='Wins', hue='Color')

    # plot.set_axis_labels('Date', 'Wins')
    # plot.figure.suptitle('ELO Rating vs Time', y=1.02)
    plot.figure.set_size_inches(10, 6)
    plt.xticks(rotation=45)
    # plt.show()

    fig = plot.figure

    return fig


def view_data(user_name='river650', item=0):
    """Format the Games object for viewing"""
    file_path = './player_data/{user_name}.csv'.format(user_name=user_name)
    df = pd.read_csv(file_path)

    print(df.head())

    game_obj_json = json.loads(df['games_obj'][item])

    pprint.pprint(game_obj_json, indent=4)




if __name__ == '__main__':
    # save_all_games()
    # df = pd.read_csv('./player_data/river650.csv')
    # print(df.head())
    plot_elo('river650', 'rapid', '1800', testing=True)

    # view_data('river650', item=0)

    # plot_wins()

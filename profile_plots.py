"""Basic plots with matplot.lib for user games data"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import json
import os
import datetime


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

def plot_elo(df, time_class='rapid', time_control='600', user_name='river650'):
    """From player df plot elo vs time"""
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
    # plt.show()

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



if __name__ == '__main__':
    save_all_games()
    df = pd.read_csv('./player_data/river650.csv')
    print(df.head())
    plot_elo(df, 'rapid', '1800')

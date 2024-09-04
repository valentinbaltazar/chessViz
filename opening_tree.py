"""Make tree structre of opening from players game dataset"""

import chess.pgn
import pandas as pd
import pprint
import json

user_name = 'river650'

file_path = './player_data/{user_name}.csv'.format(user_name=user_name)

df = pd.read_csv(file_path)

print(df.head())

game_obj = df['games_obj'][1]


game_obj_json = json.loads(game_obj)

# pprint.pprint(game_obj_json, indent=4)

# pprint.pprint(game_obj_json['games'][10]['pgn'], indent=4)

all_pgn = [list_item['pgn'] for list_item in game_obj_json['games']]

# game_out = chess.pgn.read_game(pgn)

# for i in range(len(all_pgn)):
#     print(f"PGN for game...{i}\n")
#     print(all_pgn)

from anytree import Node, RenderTree, find_by_attr
import chess.pgn
from io import StringIO
from anytree.exporter import DotExporter
import graphviz

# Parse PGNs from DataFrame
def parse_pgn_list(pgn_list):
    games = []
    for pgn in pgn_list:
        game = chess.pgn.read_game(StringIO(pgn))
        if game is not None:
            games.append(game)
    return games

def build_tree(games, player_color="white", max_depth=3):
    root = Node("Start")
    
    for game in games:
        print("New game pgn...")
        node = root
        board = game.board()
        current_depth = 0
        
        # Determine whether to track White or Black's moves
        is_white = (player_color.lower() == "white")
        
        for ply, move in enumerate(game.mainline_moves()):
            if ply <= max_depth*2:
                # Track move only if it's made by the chosen player
                if (is_white and ply % 2 == 0) or (not is_white and ply % 2 == 1):
                    move_san = board.san(move)
                    print(f"Looking at move: {move_san}")
                    # Add the move to the tree only if within the depth limit
                    if current_depth < max_depth:
                        child = find_by_attr(node, move_san)
                        if not child:
                            child = Node(move_san, parent=node)
                        node = child
                        current_depth += 1  # Increase depth only when a move is added
                    
                board.push(move)
    
    return root

def print_tree(root):
    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}")



# Visualize the tree
def visualize_tree(root, output_file="chess_tree"):
    DotExporter(root).to_dotfile("tree.dot")

    # Load the DOT file
    with open("tree.dot", "r") as file:
        dot_data = file.read()

    # Create a graph from the DOT data
    graph = graphviz.Source(dot_data)

    # Render the graph to a PNG file and save it
    graph.render(filename="tree", format="png", cleanup=False)


# Example Usage
# pgn_file = 'your_games.pgn'
games = parse_pgn_list(all_pgn)
tree_root = build_tree(games, "white", 3)
print_tree(tree_root)

visualize_tree(tree_root)

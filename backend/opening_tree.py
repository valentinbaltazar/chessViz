"""Make tree structre of opening from players game dataset"""

import chess.pgn
import pandas as pd
import json

from anytree import Node, RenderTree
import chess.pgn
from io import StringIO


def make_pngs(user_name = 'river650', time_class='rapid', time_control='600', player_color="white"):
    """Get list of all PGN objects from user dataset."""
    file_path = './player_data/{user_name}.csv'.format(user_name=user_name)
    df = pd.read_csv(file_path)

    all_pgn = []

    for game_obj in  df['games_obj']:
        game_obj_json = json.loads(game_obj)
        for game in game_obj_json['games']:
            if (game['time_class']== time_class) and (game['time_control']== time_control) and (game[f'{player_color}']['username']== user_name):
        
                all_pgn.append(game['pgn'])
    
    return all_pgn


# Parse PGNs from DataFrame
def parse_pgn_list(pgn_list):
    """Take string PNGs to a list of chess.pgn objects"""
    games = []
    for pgn in pgn_list:
        game = chess.pgn.read_game(StringIO(pgn))
        if game is not None:
            games.append(game)
    return games


def build_tree(games, player_color="white", max_depth=3):
    root = Node("Start")
    move_totals = {}
    main_lines = {}
    for game in games:
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
                    # print(f"Looking at move: {move_san}")
                    # Add the move to the tree only if within the depth limit
                    if current_depth < max_depth:
                        # Manually check if the move already exists among the current node's children
                        child = None
                        for existing_child in node.children:
                            if existing_child.name == move_san:
                                child = existing_child
                                # print(f"Looking at move: {move_san}")
                                # if move_san in move_totals:
                                #     move_totals[move_san] += 1
                                # else:
                                #     move_totals[move_san] = 1

                                # Increment dict mainline value
                                child_anc = [n.name for n in existing_child.ancestors] + [existing_child.name]
                                # print(child_anc)
                                anc_key = '_'.join(child_anc)
                                if anc_key in main_lines:
                                    main_lines[anc_key] += 1
                                else:
                                    main_lines[anc_key] = 1

                                # Counts move totals
                                if move_san in move_totals:
                                    move_totals[move_san] += 1
                                else:
                                    move_totals[move_san] = 1
                                break
                        
                        # If no existing child found, create a new node for the move
                        if not child:
                            child = Node(move_san, parent=node)

                            # Make a dict entry for each mianline
                            ancestors = [n.name for n in child.ancestors] + [child.name]
                            # print(ancestors)
                            anc_key = '_'.join(ancestors)
                            if anc_key in main_lines:
                                main_lines[anc_key] += 1
                            else:
                                main_lines[anc_key] = 1

                            
                           
                        
                        # Move to the child node and increment depth
                        node = child
                        current_depth += 1
                    
                board.push(move)
    # print(move_totals)
    # print(main_lines)
    # Add leaf node with mainline counts

    # child_mainline = Node('1', parent=child)
    for children in root.descendants:
        if children.is_leaf:
            leaf_path = '_'.join([n.name for n in children.path])
            # print(leaf_path)
            Node(main_lines[leaf_path], parent=children)

    return root


def print_tree(root):
    output_tree = ""
    for pre, _, node in RenderTree(root):
        output_tree += f"{pre}{node.name}\n"
        # print(f"{pre}{node.name}")
    # print(output_tree)

    return output_tree

def get_tree(user_name='river650', time_class='rapid', time_control='1800', player_color="white", max_depth=2):
    """Return Tree given input params"""
    
    pgn_list = make_pngs(user_name, time_class, time_control, player_color)
    games = parse_pgn_list(pgn_list)
    tree_root = build_tree(games, player_color, max_depth)

    return print_tree(tree_root)

if __name__ == '__main__':
    get_tree()
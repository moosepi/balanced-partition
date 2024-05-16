import itertools
import random
import math
import time
import gc

import bldm

TEAMSIZE = 4
TIMELIMIT = 10
START = time.time()

ranks = {}
def process_rank(line):
    rank, rank_players = line.split(':', 2)
    rank = int(rank)
    for player in rank_players.split(','):
        ranks[player.strip().lower()] = rank

with open('ranks.txt', 'r') as file:
    for line in file.readlines():
        process_rank(line)

players = {}
with open('players.txt', 'r') as file:
    for player in file.read().split(','):
        player = player.strip().split(' (')[0]
        player = player.strip()
        player_key = player.lower()
        if player_key in ranks:
            new_player = {player: ranks[player_key]}
            players.update(new_player)
        else:
            print(f"[WARN] Player '{player}' not found")

players = dict(sorted(players.items(), key=lambda x:x[1], reverse=True))
print(len(players), players)

def get_player_value(player):
    return int(player.split("(")[1].split(")")[0])

def get_group_sum(group):
    return sum([get_player_value(player) for player in group])

possible_teams = bldm.balanced_partition(list(players.items()), TEAMSIZE, TIMELIMIT)
if len(possible_teams) > 5:
    print(random.choice(possible_teams))
    print(random.choice(possible_teams))
    print(random.choice(possible_teams))
    print(random.choice(possible_teams))
    print(random.choice(possible_teams))
elif len(possible_teams) > 0:
    for possible_team in possible_teams:
        print(possible_team)
else:
    print('found nothing')
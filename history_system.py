#####################
## === Imports === ##
import player_pool

###################################
## === Global History System === ##

##########################
## -- global matches -- ##
## - "match_id": key for tracking match information
## - "players": 2-tuple of players
## - "match history": a list of T dictionaries corresponding to T rounds
## - "total_score": 2-tuple of end game cumulative score 


####################################
## -- match history (each dict)-- ##
## - "round": numerical, round t
## - "message": 2-tuple of strings, (self_message, oppo_message)
## - "action": 2-tuple of strings, (self_action, oppo_action)
## - "payoff": 2-tuple of strings, (self_payoff, oppo_payoff)
## - "current_score": 2-tuple of strings, (self_curr_score, oppo__curr_score)

# global_matches = {
#     match_id: {
#         "players": ("000", "001"),
#         "match history": [...],
#         "total_score": (x, y)
#     }
# }

#########################
## -- agent history -- ##

# agent_history = {
#     "000": [match_id0, match_id1],
#     "001": [match_id0, match_id2],
#     "002": [match_id1, match_id2]
# }







##############################
## -- Initialize History -- ##

global_matches = {}
agent_history = {}
match_counter = 0

def initialize_history():
    global global_matches, agent_history, match_counter

    ## Reset
    global_matches = {}
    agent_history = agent_history = {agent_id: [] for agent_id in player_pool.agent_pool.keys()}
    match_counter = 0


def display_history():
    for ID in agent_history:
        print(f"\nPlayer {ID}: wins ...")

    
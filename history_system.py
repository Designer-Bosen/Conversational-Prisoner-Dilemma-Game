#####################
## === Imports === ##
import threading
import player_pool

###################################
## === Global History System === ##

##########################
## -- global matches -- ##
## - "match_id": key for tracking match information
## - "players": a 2-tuple of players
## - "match history": a list of T dictionaries corresponding to T rounds
## - "total_score": a 2-tuple of end game cumulative score 
## - "match_summary": a dictionary of 


####################################
## -- match history (each dict)-- ##
## - "round": numerical, round t
## - "message": 2-tuple of strings, (self_message, oppo_message)
## - "action": 2-tuple of strings, (self_action, oppo_action)
## - "payoff": 2-tuple of numbers, (self_payoff, oppo_payoff)
## - "current_score": 2-tuple of strings, (self_curr_score, oppo__curr_score)

# global_matches = {
#     match_id: {
#         "players": ("000", "001"),
#         "match history": [...],
#         "total_score": (x, y)
#         "match_summary": {
#             "000": sum_x,
#             "001": sum_y
#         }
#     }
#     ......
# }

# agent_matches = {
#     "000": [match_id0, match_id1],
#     "001": [match_id0, match_id2],
#     "002": [match_id1, match_id2]
#     ......
# }

# agent_stats = {
#     "000": {"rank": None, "wins": 0, "losses": 0, "draws": 0, "total_rounds": 0, "total_payoff": 0, "average_payoff": 0}
#     "001": {"rank": None, "wins": 0, "losses": 0, "draws": 0, "total_rounds": 0, "total_payoff": 0, "average_payoff": 0}
#     "002": {"rank": None, "wins": 0, "losses": 0, "draws": 0, "total_rounds": 0, "total_payoff": 0, "average_payoff": 0}
#     ......
# }

## Descending order based on avg
# global_ranking = [(idXXX, avg), (idXXX, avg), ......]

## Match-wise Summary

## Tournament Summary



##############################
## -- Initialize History -- ##

global_matches = {}
agent_matches = {}
agent_stats = {}
global_ranking = []
match_counter = 0
thread_lock = threading.Lock()  ## Protector of multi-thread task

def initialize_history(teams):
    global global_matches, agent_matches, agent_stats, global_ranking, match_counter

    ## Reset
    global_matches = {}
    agent_matches = {id: [] for id in teams}
    agent_stats = {id: {"rank": None, "wins": 0, "losses": 0, "draws": 0, "total_payoff": 0, "total_rounds": 0, "average_payoff": 0} for id in teams}
    global_ranking = []
    match_counter = 0


## Update match history (every time a match is finished, call this)
def update_match(i, j, history, score_0, score_1, sum_0, sum_1):
    with thread_lock:
        ## --- Update global match --- ##
        global match_counter

        match_id = match_counter
        match_counter += 1

        global_matches[match_id] = {
            "players": (i, j),
            "match_history": history,
            "total_score": (score_0, score_1),
            "match_summary": {i: sum_0, j: sum_1}
        }

        ## --- Update agent match --- ##
        agent_matches[i].append(match_id)
        agent_matches[j].append(match_id)

        ## --- Update agent stats --- ##
        total_rounds = len(history)

        agent_stats[i]["total_payoff"] += score_0
        agent_stats[i]["total_rounds"] += total_rounds

        agent_stats[j]["total_payoff"] += score_1
        agent_stats[j]["total_rounds"] += total_rounds

        if score_0 > score_1:
            agent_stats[i]["wins"] += 1
            agent_stats[j]["losses"] += 1
        elif score_0 < score_1:
            agent_stats[j]["wins"] += 1
            agent_stats[i]["losses"] += 1
        else:
            agent_stats[i]["draws"] += 1
            agent_stats[j]["draws"] += 1

        ## --- Update ranking --- ##
        update_ranking()

## Update ranking, called in update_match()        
def update_ranking():
    global global_ranking
    ranking = []

    ## Compute average payoff
    for id, stats in agent_stats.items():
        if stats["total_rounds"] == 0:
            avg = 0
        else:
            avg = stats["total_payoff"] / stats["total_rounds"]

        agent_stats[id]["average_payoff"] = avg
        ranking.append((id, avg))

    ## Sort in descending order: high to low
    ranking.sort(key=lambda x: x[1], reverse=True)

    ## Update "rank" in agent_stats
    for rank, (id, _) in enumerate(ranking, start=1):
        agent_stats[id]["rank"] = rank

    global_ranking = ranking


## Display real-time leaderboard to a pair of agents when a single match starts
def display_dynamic_leaderboard():
    global global_ranking, agent_stats

    text = "===================\n=== LEADERBOARD ===\n"

    ## Filter players who have played at least one match
    played_ids = {id for id, stats in agent_stats.items() if stats["total_rounds"] > 0}

    ## If no player has any matches yet
    if not played_ids:
        return text + "No matches played yet.\n"

    ## Only keep those in ranking AND have played
    filtered_ranking = [(id, avg) for id, avg in global_ranking if id in played_ids]

    for id, avg in filtered_ranking:
        stats = agent_stats[id]
        rank = stats["rank"]
        text += f"Rank: {rank} | Player {id} | W: {stats['wins']}, L: {stats['losses']}, D: {stats['draws']}\n"
        
    text += "\nIDs that do not show in the leaderboard have not matched yet.\n"

    return text


## Display Match Information after tornament is finished (DEBUG)
def display_leaderboard():
    global global_ranking, agent_stats
    print("==========================\n=== TOURNAMENT SUMMARY ===\n")

    ## --- Leaderboard ---
    print("===================\n=== LEADERBOARD ===\n")
    for id, avg in global_ranking:
        stats = agent_stats[id]
        rank = stats["rank"]
        print(f"Rank: {rank} | Player {id} | Avg Payoff: {stats['average_payoff']:.3f} | Rounds: {stats['total_rounds']} |" 
              f"W: {stats['wins']}, L: {stats['losses']}, D: {stats['draws']}")
    
    ## --- Match Summary ---
    print("\n=============================\n=== AGENT MATCH SUMMARIES ===\n")
    agent_summary_map = {id: [] for id in agent_stats.keys()}

    for match in global_matches.values():  ## Extract and reorganize into a new data structure
        i, j = match["players"]
        summaries = match["match_summary"]

        agent_summary_map[i].append((j, summaries[i]))
        agent_summary_map[j].append((i, summaries[j]))

    for id in agent_summary_map:  ## Display
        print(f"\n=== ID \"{id}\"'s summary ===")

        for opponent_id, summary in agent_summary_map[id]:
            print(f"[MATCH WITH {opponent_id}]: {summary}")


    ## --- Tournament Summary ---
    print("\n==================================\n=== AGENT TOURNAMENT SUMMARIES ===\n")
    print("NOT DESIGNED YET")


    
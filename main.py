#####################
## === Imports === ##

## Local files
import history_system
import match
import matching_algorithm



###############################
## === Single Tournament === ##

## PARAMETERS
# teams = ["006", "007"]
# K = 2
# T = 5

# history_system.initialize_cross_tournament(teams)
# matching_algorithm.greedy_matching(teams, K, T = T) 



##############################
## === Multi-Tournament === ##

## PARAMETERS
# teams = ["000", "001", "002", "003", "004", "005", "006", "007"]
teams = ["004", "006", "007"]
K = 2
T = 8
tournaments = 1


history_system.initialize_cross_tournament(teams)
for tournament in range(tournaments):

    ## --- Manipulate output system --- ##
    history_system.outputs.append("")  ## Create a new element in the output lists
    tournament_msg = f"\n\n====================\n=== TOURNAMENT {tournament + 1} ===\n====================\n"
    print(tournament_msg)
    history_system.outputs[-1] += tournament_msg

    ## --- Launch Tournament --- ##
    matching_algorithm.greedy_matching(teams, K, T = T)

    ## --- Store Output in different files --- ##
    with open(f"outputs/tournament_{tournament + 1}.txt", "w", encoding="utf-8") as f:
        f.write(history_system.outputs[-1])
#####################
## === Imports === ##


## LLM
from openai import OpenAI
from anthropic import Anthropic

## Local files
import player_pool
import match
import matching_algorithm
print("LOADED:", player_pool.__file__)



## Single Game Simulation
# result = match.match(0, 1, T=3, human=False)
# print(result)


## Round-Robin simulation
teams = ["000", "001", "002", "003"]
K = 2
matching_algorithm.greedy_matching(teams, K, T = 10)  ## AGENT MATCH

## if run indep, batch b is not required. inter-tournament carries thru summary.
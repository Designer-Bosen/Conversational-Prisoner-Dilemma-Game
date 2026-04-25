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
teams = ["000", "001", "002"]
K = 2
matching_algorithm.greedy_matching(teams, K, b = None, T = 2, updating_round = 3, know_round = True, human = False)
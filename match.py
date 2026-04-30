#####################
## === IMPORTS === ##
import pyspiel
import os
import getpass # Human input privacy

## LLM
from openai import OpenAI
from anthropic import Anthropic

## Local files
import player_pool
import history_system


#####################
## === METHODS === ##

## Clear textbox 
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


## Decode binary action to text
def cd_decode(num):
    if num == 0:
        return "cooperate"
    if num == 1:
        return "defect"


## Encode LLM action information into binary
def action_encode(text):
    t = text.strip().lower()
    if t == "cooperate": return 0
    if t == "defect": return 1
    if "defect" in t: return 1
    if "cooperate" in t: return 0
    if t == "c": return 0
    if t == "d": return 1
    return 1  # default is defect


## Input prompt to agent and returns LLM output
def llm_input(agent, prompt):
    provider = agent["provider"]
    model = agent["model"]
    client = agent["client"]

    ## ---- OpenAI ----
    if provider == "openai":
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}  # Only update game rule with prompt
            ]
        )
        return response.choices[0].message.content.strip()

    ## ---- Claude ----
    elif provider == "anthropic":
        response = client.messages.create(
            model=model,
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    
    ## ---- Unrecognized Model ----
    else:
        raise ValueError(f"Unknown provider: {provider}")



## String about the game rule
def rule_telling():
    return """
# Now you are a rational player participating in a Dilemma Game.
# IMPORTANT: always remember in this match: Your goal is to maximize long-term payoff across all rounds. Do NOT optimize only for the current round.
# Some tricks: If cooperating with some agents may help maximizing your total payoff affecting your global ranking, you may do so
# Game Rule:
in each round, there are two phases: Message Phase and Action Phase
- In Message Phase: You may send a message to the opponent. You message don't necessarily need to be truthful, 
    but can be strategic to affect your opponent's next action. Before you compose the message, 
    you will receive available history information in previous rounds.
- In Action Phase: opponent's messages are available to both players. Together with the available 
    history information in previous rounds, choose your action: Cooperate (C) or Defect (D).
- Payoffs:
    - (C, C) -> (2, 2)
    - (C, D) -> (-1, 3)
    - (D, C) -> (3, -1)
    - (D, D) -> (0, 0)
- Available history is displayed below:

"""


## String of history in player i's perspective
def history_telling(player_index, history):
    text = "\n==== Game history====:"

    if not history:
        return text + "\nNo previous rounds for now."

    for line in history:
        m0, m1 = line["message"]
        a = line["action"]
        p = line["payoff"]
        sc = line["current_score"]

        if player_index == 0:
            you_msg, opp_msg = m0, m1
        else:
            you_msg, opp_msg = m1, m0

        text += (
            f"\n\n=== Round {line['round']}==="
            f"\nYou said: \"{you_msg}\""
            f"\nOpponent said: \"{opp_msg}\""
        )
        ######################################
        if (a is None) or (p is None) or (sc is None):
            text += "\n"
            continue

        a0, a1 = a
        p0, p1 = p
        sc0, sc1 = sc

        if player_index == 0:
            you_a, opp_a = a0, a1
            you_p, opp_p = p0, p1
            you_score, opp_score = sc0, sc1
        else:
            you_a, opp_a = a1, a0
            you_p, opp_p = p1, p0
            you_score, opp_score = sc1, sc0

        text += (
            f"\nYou chose to {cd_decode(you_a)}, opponent chose to {cd_decode(opp_a)}."
            f"\nPayoff: you {you_p}, opponent {opp_p}.\n"
            f"\nCumulative payoff for round {line['round']}: you have scored {you_score}, opponent has scored {opp_score}"
        )

    return text


## MESSAGE PHASE INQUIRY to agent
def message_request(player_index, agent_map, history, t, T, know_round, updating_round, self_id, opponent_id, leaderboard_text):
    prompt = ""

    ## ---- Rule Telling Logic ----
    if t == 1:
        prompt += f"""
===PRISONER DILEMMA GAME===
{rule_telling()}

Your ID: {self_id}, Opponent ID: {opponent_id}

=== CURRENT LEADERBOARD ===
{leaderboard_text}
"""
    elif (t - 1) % updating_round == 0:
        prompt += f"""
===REMINDER OF GAME RULE===
{rule_telling()}

Your ID: {self_id}, Opponent ID: {opponent_id}

=== CURRENT LEADERBOARD ===
{leaderboard_text}
"""
        
    ## ---- Round Information ----
    prompt += f"\n=== ROUND {t}: MESSAGE PHASE ===\n"
    if know_round:
        prompt += f"This is round {t} out of {T}. {T - t + 1} rounds remaining.\n"

    ## ---- Main Content ----
    prompt += f"""
{history_telling(player_index, history)}
Now send a message to the opponent for the next round.
Your message should strategically influence the opponent's future behavior.
You may make promises, threats, or signals, which may or may not be truthful.
Your message should be relevant to the game and your strategy.
Reminder: Do not sacrifice long-term gains for short-term rewards.
Compose your response in at most 50 words.
"""
    return llm_input(agent_map[player_index], prompt)


## ACTION PHASE INQUIRY to agent
def action_request(player_index, agent_map, history, t, T, know_round):
    ## ---- Round Information ----
    prompt = f"\n=== ROUND {t}: ACTION PHASE ===\n"
    if know_round:
        prompt += f"This is round {t} out of {T}. {T - t + 1} rounds remaining.\n"

    ## ---- Main Content ----
    prompt += f"""
{history_telling(player_index, history)}
NOTE: Messages shown right above correspond to the CURRENT round.
Now choose you decision based on the history and your opponent's message this round.
Beware your opponent's message could be strategic.
Reminder: Do not sacrifice long-term gains for short-term rewards.
Respond with EXACTLY ONE WORD: "Cooperate" or "Defect" and nothing else.
This response will be used as your action for this round, don't be ambiguous.
"""
    return llm_input(agent_map[player_index], prompt)


## END GAME INQUIRY FOR SUMMARY
def summary_request(self_index, agent_map, history, opponent_id):
    prompt = f"""
You now have finished a match against - Opponent ID: {opponent_id}. 
Below is a complete view of your match history:
{history_telling(self_index, history)}
Compose a match summary about your opponent's behavior in 2-3 sentences:
This summary can include: cooperation tendency, reaction to defection, consistency etc.
This summary will help you with your future decisions, be concise.
"""
    return llm_input(agent_map[self_index], prompt)


## Display the history (DEBUG)
def display_history(player_ids, history):
    i, j = player_ids
    print("\n===============\n=== HISTORY ===")
    for line in history:
        print(
            f"\n===============\n=== Round {line['round']} ==="
            f"\nPlayer {i} says: \"{line['message'][0]}\";"
            f"\nPlayer {j} says: \"{line['message'][1]}\";"
            f"\nPlayer {i} chose to {cd_decode(line['action'][0])};"
            f"\nPlayer {j} chose to {cd_decode(line['action'][1])};"
            f"\nPlayer {i}'s payoff is: {line['payoff'][0]};"
            f"\nPlayer {j}'s payoff is: {line['payoff'][1]};"
        )





########################################################################################################
########################################################################################################


def match_agent(i, j, T = 10, updating_round = 3, know_round = True):
    """
    Single match of conversational Prisoner's Dilemma between player i and j
    PARAMETERS: 
    - "i": Passed-in ID i, corresponds to player 0
    - "j": Passed-in ID j, corresponds to player 1
    - "T": Number of iterations in a single match, default = 10
    - "updating_round": Number of rounds between until the next reminder of game rule, default = 3.
    - "know_round": If both players are informed how many rounds in total, default = TRUE.
    - "b": batch size (number of repeated simulations per match) — not used yet

    RETURN:
    A dictionary of
    - "player_ids": 2-tuple of player IDs
    - "history": a dictionary of history of this match
    - "total_score": 2-tuple of the final cumulative score

    ##############################
    ## Customized Payoff Matrix ##
    ##       C         D
    ## C  (2, 2)    (-1, 3) 
    ## D  (3, -1)    (0, 0)

    ############################
    ## Legal Actions Encoding ##
    ## Cooperate (C) = 0, Defect (D) = 1
    ## (C, C) -> 0
    ## (C, D) -> 1
    ## (D, C) -> 2
    ## (D, D) -> 3
    """

    ########################
    ## === INITIALIZE === ##

    history = []
    score_0 = 0
    score_1 = 0

    game = pyspiel.create_matrix_game(
    [[2, 3], [-1, 0]],   # player 0
    [[2, -1], [3, 0]]    # player 1
    )

    agent_map = {
        0: player_pool.agent_pool[i],
        1: player_pool.agent_pool[j]
    }
    
    leaderboard_text = history_system.display_dynamic_leaderboard()

    ########################
    ## === START GAME === ##

    for t in range(1, T+1):  # Later change to stop condition
        state = game.new_initial_state() # reset (each trail are independent, but are connected through history system)

        message_0 = message_request(0, agent_map, history, t, T, know_round, updating_round, i, j, leaderboard_text)
        message_1 = message_request(1, agent_map, history, t, T, know_round, updating_round, j, i, leaderboard_text)
        
        ## Update History
        history.append({
            "round": t,
            "message": (message_0, message_1),
            "action": None,
            "payoff": None,
            "current_score": None
        })

        ##########################
        ## === ACTION PHASE === ##
        
        action_0 = action_encode(action_request(0, agent_map, history, t, T, know_round))
        action_1 = action_encode(action_request(1, agent_map, history, t, T, know_round))

        joint_action = action_0 * 2 + action_1
        state.apply_action(joint_action)
        payoff_0, payoff_1 = tuple(state.returns())

        ## Update Current Cumulative Score
        score_0 += payoff_0
        score_1 += payoff_1

        ## Update History
        history[-1]["action"] = (action_0, action_1)
        history[-1]["payoff"] = (payoff_0, payoff_1)
        history[-1]["current_score"] = (score_0, score_1)


    ######################
    ## === END GAME === ##

    ## Display Match History
    display_history((i, j), history)  # FOR DEBUG

    ## Ask both agents for match summary
    sum_0 = summary_request(0, agent_map, history, j)
    sum_1 = summary_request(1, agent_map, history, i)
    
    return {
        "player_ids": (i, j),
        "history": history,
        "total_score": (score_0, score_1),
        "match_summary": (sum_0, sum_1)
    }




# # !!! This is a temporary storage for match_human() 



# ########################################################################################################
# ########################################################################################################


# ###############################
# ## === THE MAIN FUNCTION === ##

# def match_human(i, j, T = 10, know_round = True):
#     ######################
#     # === INITIALIZE === #

#     history = []
#     score_0 = 0
#     score_1 = 0

#     game = pyspiel.create_matrix_game(
#     [[2, 3], [-1, 0]],   # player 0
#     [[2, -1], [3, 0]]    # player 1
#     )

#     print(rule_telling())
#     print(f"ID: {i}, you are player 0\n")
#     print(f"ID: {j}, you are player 1\n")
#     print("\n\n\n")


#     ########################
#     ## === START GAME === ##

#     for t in range(1, T+1):  # Later change to stop condition
#         state = game.new_initial_state() # reset (each trail are independent, but are connected through history system)

#         #########################
#         # === MESSAGE PHASE === #

#         print(f"\n=== ROUND {t}: MESSAGE PHASE ===\n")
#         ###########################################
#         print(f"\n--- Player 0 (ID: {i}) Message Phase ---\n")
#         choice = input("Player 0: do you want to read the game rule again?\nType 'y' for YES, 'n' for NO: \n").strip().lower()
#         if choice == "y": print(rule_telling() + "\n\n")
#         choice = input("Player 0: do you want to see your history?\nType 'y' for YES, 'n' for NO: \n").strip().lower()
#         if choice == "y": print(history_telling(0, history) + "\n\n")
#         message_0 = getpass.getpass("Player 0, enter your message (your opponent cannot see this): ")
#         input("\nPress Enter and hand over to Player 1...\n")
#         clear_screen()
#         ###########################################
#         print(f"\n--- Player 1 (ID: {j}) Message Phase ---\n")
#         choice = input("Player 1: do you want to read the game rule again?\nType 'y' for YES, 'n' for NO: \n").strip().lower()
#         if choice == "y": print(rule_telling() + "\n\n")
#         choice = input("Player 1: do you want to see your history?\nType 'y' for YES, 'n' for NO: \n").strip().lower()
#         if choice == "y": print(history_telling(1, history) + "\n\n")
#         message_1 = getpass.getpass("Player 1, enter your message (your opponent cannot see this): ")
#         input("\nPress Enter to continue...\n")
#         clear_screen()

#         # Update History
#         history.append({
#             "round": t,
#             "message": (message_0, message_1),
#             "action": None,
#             "payoff": None,
#             "current_score": None
#         })

#         ########################
#         # === ACTION PHASE === #

#         print(f"\n=== ROUND {t}: ACTION PHASE ===\n")
#         print(f"Player 0 just says: \"{message_0}\"\n")
#         print(f"Player 1 just says: \"{message_1}\"\n")
#         ###########################################
#         print(f"\n--- Player 0 (ID: {i}) Action Phase ---\n")
#         choice = input("Player 0: do you want to read the game rule again?\nType 'y' for YES, 'n' for NO: \n").strip().lower()
#         if choice == "y": print(rule_telling() + "\n\n")
#         choice = input("Player 0: do you want to see your history?\nType 'y' for YES, 'n' for NO: \n").strip().lower()
#         if choice == "y": print(history_telling(0, history) + "\n\n")
#         while True:
#             act_input = getpass.getpass("Player 0, choose your action,\nType 'c' for Cooperate, 'd' for Defect (your opponent cannot see this): ").strip().lower()
#             if act_input == "c":
#                 action_0 = 0
#                 break
#             elif act_input == "d":
#                 action_0 = 1
#                 break
#             else:
#                 print("Invalid input. Type 'c' for Cooperate, 'd' for Defect: ")

#         input("\nPress Enter and hand over to Player 1...\n")
#         clear_screen()
#         ###########################################
#         print(f"\n--- Player 1 (ID: {j}) Action Phase ---\n")
#         choice = input("Player 1: do you want to read the game rule again?\nType 'y' for YES, 'n' for NO: \n").strip().lower()
#         if choice == "y": print(rule_telling() + "\n\n")
#         choice = input("Player 1: do you want to see your history?\nType 'y' for YES, 'n' for NO: \n").strip().lower()
#         if choice == "y": print(history_telling(1, history) + "\n\n")
#         while True:
#             act_input = getpass.getpass("Player 1, choose your action,\nType 'c' for Cooperate, 'd' for Defect (your opponent cannot see this): ").strip().lower()
#             if act_input == "c":
#                 action_1 = 0
#                 break
#             elif act_input == "d":
#                 action_1 = 1
#                 break
#             else:
#                 print("Invalid input. Type 'c' for Cooperate, 'd' for Defect: ")

#         input("\nPress Enter to continue...\n")
#         clear_screen()

#         joint_action = action_0 * 2 + action_1
#         state.apply_action(joint_action)
#         payoff_0, payoff_1 = tuple(state.returns())

#         # Update Current Cumulative Score
#         score_0 += payoff_0
#         score_1 += payoff_1

#         # Display results to human
#         print("\n=== ROUND RESULT ===")
#         print(f"Player 0 chose: {cd_decode(action_0)}")
#         print(f"Player 1 chose: {cd_decode(action_1)}")
#         print(f"Payoff: Player 0 = {payoff_0}, Player 1 = {payoff_1}")
#         print(f"Total Score: Player 0 = {score_0}, Player 1 = {score_1}")
#         input("\nPress Enter to proceed to next round...\n")  # Determine who press 
#         clear_screen()

        
#         # Update History
#         history[-1]["action"] = (action_0, action_1)
#         history[-1]["payoff"] = (payoff_0, payoff_1)
#         history[-1]["current_score"] = (score_0, score_1)


#     ######################
#     ## === END GAME === ##
#     ## Record History to history_system.py 

#     ## Display Match History
#     display_history((i, j), history)  # FOR DEBUG

#     return {
#         "player_ids": (i, j),
#         "history": history,
#         "total_score": (score_0, score_1)
#     }

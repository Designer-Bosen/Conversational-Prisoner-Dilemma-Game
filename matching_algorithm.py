### Algorithm designed by: Hengzhi He ###

#####################
## === IMPORTS === ##
import time
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
import match

#####################
## === METHODS === ##

## Pairing Algorithm
def find_pair_simple(teams, remaining, busy):
    idle = [i for i in teams if not busy[i]]
    idle.sort(key=lambda i: len(remaining[i]))
    for i in idle:
        candidates = [j for j in remaining[i] if not busy[j]]
        if not candidates: continue
        candidates.sort(key=lambda j: len(remaining[j]))
        return i, candidates[0]
    return None

## Launch parallel threads
def launch_batch(task_id, i, j, b, finished_queue, T, updating_round, know_round, human, executor):
    def worker():
        print(f"\n[START] {i} vs {j}\n")
        time.sleep(0.01)
        try:
            match.match(i, j, T = T, updating_round = updating_round, know_round = know_round, human = human, b=b)
        finally:
            print(f"\n[DONE] {i} vs {j}\n")
            finished_queue.put(task_id)
    executor.submit(worker)



#############################
## === GREEDY MATCHING === ##

def greedy_matching(teams, K, b = None, T = 10, updating_round = 3, know_round = True, human = False):
    """
    teams: all IDs [0,1,2,...,n]
    K: Maximum number of parallel matches (tuning)
    b: passed in to match() parameter
    """
    ##################
    # === SETUPS === #

    remaining = {i: set(teams) - {i} for i in teams} ## For node i: opponents that i has NOT matched with yet
    busy = {i: False for i in teams} ## For node i: whether i is currently in a running match
    running = {} ## task_id -> (i, j), used to store current matching pairs
    unfinished = {(i, j) for i in teams for j in teams if i < j} ## unfinished (pairs) , cut down entire match matrix to upper triangular
    task_id_counter = 0 ## Used to distinguish running tasks (can be incremented)
    finished_queue = Queue() ## track finished tasks
    executor = ThreadPoolExecutor(max_workers=K)

    #######################
    # === MATCH START === #

    while unfinished:
    
        ## Run K parallel matches
        while len(running) < K:
            pair = find_pair_simple(teams, remaining, busy)
            if pair is None: break
            i, j = pair

            busy[i] = True
            busy[j] = True

            ## Increment Task ID
            task_id_counter += 1
            current_id = task_id_counter

            # launch async match
            running[current_id] = (i, j)
            launch_batch(current_id, i, j, b, finished_queue, T = T, updating_round = updating_round, know_round = know_round, human = human, executor = executor)

        ## === When one ongoing match finishes === ##
        finished_id = finished_queue.get()
        i, j = running.pop(finished_id)  # Pop this running task
        busy[i] = False
        busy[j] = False

        ## Remove i and j from their corresponding strutures
        remaining[i].remove(j) # Remove j from whom i has not matched yet
        remaining[j].remove(i) # Remove i from whom j has not matched yet
        unfinished.remove((min(i, j), max(i, j))) # remove the pair from the triangular matrix

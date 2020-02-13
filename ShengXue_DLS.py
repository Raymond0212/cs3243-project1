import copy
import os
import sys
import time


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.visited = set()
        self.p = {}
        self.foundSolution = False
        self.totalNodes = 0

    def solve(self):
        # TODO
        # implement your search algorithm here
        max_recursion_depth = 10
        lower_bound = 0
        upper_bound = 10000
        for max_recursion_depth in range(lower_bound, upper_bound):
            print("Attempting depth: " + str(max_recursion_depth))
            self.dfs(self.init_state, 0, max_recursion_depth)
            print("Total nodes so far: " + str(self.totalNodes))
            if not self.foundSolution:
                print("Depth " + str(max_recursion_depth) + " failed")
                self.actions.clear()
                self.visited.clear()
                self.p.clear()
                continue
            else:
                break

        current_state_str = str(self.goal_state)
        actions_reversed = []

        while current_state_str in self.p:
            actions_reversed.append(self.p[current_state_str][1])
            current_state_str = self.p[current_state_str][0]

        actions_reversed.reverse()
        print(actions_reversed)
        return actions_reversed  # sample output



    def dfs(self, state, current_recursion_depth, max_recursion_depth):
        if current_recursion_depth > max_recursion_depth:
            pass
        elif self.isSolved(state):
            self.totalNodes = self.totalNodes + 1
            self.foundSolution = True
        else:
            self.totalNodes = self.totalNodes + 1
            state_str = str(state)
            self.visited.add(state_str)
            for direction in ["RIGHT", "LEFT", "UP", "DOWN"]:
                neighbour_state = self.move(direction, state)
                if neighbour_state is not None:
                    neighbour_state_str = str(neighbour_state)
                    if neighbour_state_str not in self.visited:
                        self.p[neighbour_state_str] = (state_str, direction)
                        self.dfs(neighbour_state, current_recursion_depth + 1, max_recursion_depth)

    def isSolved(self, state):
        goal_state_str = str(self.goal_state)
        return state == goal_state or state == goal_state_str

    def move(self, direction, state):
        newstate = copy.deepcopy(state)
        pos = self.find_zero(newstate)
        posx = pos[0]
        posy = pos[1]
        if direction == "UP" and posy > 0:
            temp = newstate[posy - 1][posx]
            newstate[posy - 1][posx] = 0
            newstate[posy][posx] = temp
            return newstate
        elif direction == "DOWN" and posy < len(newstate) - 1:
            temp = newstate[posy + 1][posx]
            newstate[posy + 1][posx] = 0
            newstate[posy][posx] = temp
            return newstate
        elif direction == "LEFT" and posx > 0:
            temp = newstate[posy][posx - 1]
            newstate[posy][posx - 1] = 0
            newstate[posy][posx] = temp
            return newstate
        elif direction == "RIGHT" and posx < len(newstate[0]) - 1:
            temp = newstate[posy][posx + 1]
            newstate[posy][posx + 1] = 0
            newstate[posy][posx] = temp
            return newstate
        else:
            #Illegal move
            return None

    def print_state(self, state):
        if state == None:
            print("Empty")
        else:
            for row in range(0, len(state)):
                print(state[row])

    def find_zero(self, state):
        for y in range(0, len(state)):
            for x in range(0, len(state[y])):
                if state[y][x] == 0:
                    return x, y
        return None

    # you may add more functions if you think is useful


if __name__ == "__main__":
    start = time.process_time()

    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()

    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]

    i, j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number, base=10)
            if 0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i - 1) // n][(i - 1) % n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    print(time.process_time() - start)

    with open(sys.argv[2], 'w') as f:
        for answer in ans:
            f.write(answer + '\n')








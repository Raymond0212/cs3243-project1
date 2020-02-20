import copy
import os
import sys
import time

frontierQueue = []
directions = ["UP", "DOWN", "LEFT", "RIGHT"]
visited = set()

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    def solve(self):
        # TODO
        # implement your search algorithm here
        start = time.time()
        print("Solving...")
        frontierQueue.insert(len(frontierQueue), [self.init_state, self.actions])
        sol = list()
        while len(frontierQueue) != 0:
            p = frontierQueue.pop(0)
            visited.add(str(p[0]))
            if p[0] == self.goal_state:
                sol = p[1]
                break
            else:
                for x in range(4):
                    self.init_state = p[0]
                    newState = self.move(directions[x], p[0])
                    if newState is not None:
                        if str(newState) not in visited:
                            if len(p[1]) == 0:
                                newList = list()
                                newList.append(directions[x])
                                frontierQueue.append([newState, newList])
                            else:
                                newList = copy.deepcopy(p[1])
                                newList.append(directions[x])
                                frontierQueue.insert(len(frontierQueue), [newState, newList])

        with open(sys.argv[2], 'w') as f:
            end = time.time()
            f.write("Total time: " + str(end - start) + " seconds" + "\n")

        return sol

    # you may add more functions if you think is useful
    def findEmptySquare(self, state):
        n = len(state)
        for row in range(n):
            for col in range(n):
                if state[row][col] == 0:
                    return [col, row]

    def move(self, direction, state):
        newstate = copy.deepcopy(state)
        pos = self.findEmptySquare(newstate)
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
            return None

if __name__ == "__main__":
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

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer + '\n')

import os
import sys

# Import necessary libraries
import heapq
import time
import copy

"""
Node is a class which is used to store each node
It contains the state, estimated cost, search depth, parent, move of current node.
__str__, __eq__, __ne__, __lt__, __gt__, __le__, __ge__ are overided
"""
class Node:
    def __init__(self, state, cost, depth, parent, move = None):
        self.state = state
        self.cost = cost
        self.parent = parent
        self.depth = depth
        self.move = move

    def __str__(self):
        output = "DEPTH: " + str(self.depth)+ " | COST: " + str(self.cost) + "\n"
        for line in self.state:
            output += ' '.join(map(str, line)) + '\n'
        return output
        
    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.cost == other.cost
        
    def __ne__(self, other):
        if type(other) != type(self):
            return True
        return self.cost != other.cost

    def __lt__(self, other):
        if type(other) != type(self):
            raise(ValueError)
        return self.cost < other.cost

    def __gt__(self, other):
        if type(other) != type(self):
            raise(ValueError)
        return self.cost > other.cost

    def __le__(self, other):
        if type(other) != type(self):
            raise(ValueError)
        return self.cost <= other.cost

    def __ge__(self, other):
        if type(other) != type(self):
            raise(ValueError)
        return self.cost >= other.cost

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        # self.actions = list()   # List of actions
        self.size = len(init_state)
        self.visited = {tuple(map(tuple, init_state))} # Check is the state has appeared or not
        self.explored = []
        self.result = []
        self.heap = []

    """
    Find the position of the blank
    """
    def locate_tile(self, puzzle, a):
        for x, row in enumerate(puzzle):
            for y, tile in enumerate(row):
                if tile == a:
                    return (x, y)

    def show_path(self, head):
        if head.parent is not None:
            self.show_path(head.parent)
        if head.move is not None:
            # print(head)
            self.result.append(head.move)

    def solve(self): #Astar
        self.heap = [Node(self.init_state, self.heuristic(self.init_state), 0, None)]
        heapq.heapify(self.heap)
        # ACTION = ["LEFT", "RIGHT", "UP", "DOWN"]
        # MOVE = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        ACTION = [ "UP", "LEFT", "RIGHT", "DOWN"]
        MOVE = [(1, 0), (0, 1), (0, -1), (-1, 0)]

        """
        This is the core part of A*
        """
        while len(self.heap) != 0:
            current = heapq.heappop(self.heap)
            if self.check_solved(current.state) == 0:
                self.show_path(current)
                return self.result

            self.explored.append(current)
            blank_x, blank_y  = self.locate_tile(current.state, 0)
            
            for i in range(4):
                if current.move is not None and i == (3-ACTION.index(current.move)):    #Don't move back
                    continue
                puzzle = copy.deepcopy(current.state) 
                dx, dy = MOVE[i]
                if blank_x + dx < 0\
                   or blank_x + dx >= self.size\
                   or blank_y + dy < 0\
                   or blank_y + dy >= self.size:
                    continue
                puzzle[blank_x][blank_y] = puzzle[blank_x+dx][blank_y+dy]
                puzzle[blank_x+dx][blank_y+dy] = 0
                if tuple(map(tuple, puzzle)) in self.visited:
                    continue
                self.visited.add(tuple(map(tuple,puzzle)))
                next_node = Node(puzzle, current.depth+1+self.heuristic(puzzle), current.depth+1, current, ACTION[i])
                heapq.heappush(self.heap, next_node)
                
        return "No Answer"

    '''
    check_solved is used to check if solved.
    return 0 while there is no misplaced tiles
    '0' is also considered as a tile
    '''
    def check_solved(self, puzzle):
        return tuple(map(tuple, puzzle)) == tuple(map(tuple, self.goal_state))

    """
    implement heuristic functions here
    return the estimated steps
    h2: n-Max Swap
    """
    def heuristic(self, state):
        puzzle = copy.deepcopy(state)
        ans = 0

        goal_blank_x, goal_blank_y = self.locate_tile(self.goal_state, 0)
        current_blank_x, current_blank_y = self.locate_tile(puzzle, 0)

        def place_zero(current_blank_x, current_blank_y):
            # 1-step swap: swap with 0 once to the goal state
            ans = 0

            while current_blank_x != goal_blank_x or current_blank_y != goal_blank_y:
                goal_idx = self.goal_state[current_blank_x][current_blank_y]
                current_goal_x, current_goal_y = self.locate_tile(puzzle, goal_idx)

                puzzle[current_blank_x][current_blank_y] = goal_idx
                puzzle[current_goal_x][current_goal_y] = 0
                ans += 1
                current_blank_x, current_blank_y = self.locate_tile(puzzle, 0)

            return ans

        place_zero(current_blank_x, current_blank_y)

        for curr_x in range(0, len(puzzle)):
            for curr_y in range(0, len(puzzle)):
                if puzzle[curr_x][curr_y] == self.goal_state[curr_x][curr_y]:
                    continue

                current_blank_x, current_blank_y = self.locate_tile(puzzle, 0)
                puzzle[current_blank_x][current_blank_y] = puzzle[curr_x][curr_y]
                puzzle[curr_x][curr_y] = 0
                ans += 1
                ans += place_zero(curr_x, curr_y)

        return ans

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
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    start = time.time()
    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()
    end = time.time()
    print("%.4f"%(end-start))

    print(len(ans))
    print("# of duplicated state:", len(puzzle.visited))
    print("# of explored nodes:", len(puzzle.explored))
    print("# of generated nodes:", len(puzzle.explored)+len(puzzle.heap))

    # print(ans) # Currently I just print the depth of the search

    # with open(sys.argv[2], 'a') as f:
    #     for answer in ans:
    #         f.write(answer+'\n')
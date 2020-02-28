import os
import sys

# Import necessary libraries
import heapq
import time
import copy
import gc

maxSizeOfFrontier = 0
"""
Node is a class which is used to store each node
It contains the state, estimated cost, search depth, parent, move of current node.
__str__, __eq__, __ne__, __lt__, __gt__, __le__, __ge__ are overided
"""


class Node:
    def __init__(self, state, cost, depth, parent, move=[]):
        self.state = state
        self.cost = cost
        self.parent = parent
        self.depth = depth
        self.move = move

    def __str__(self):
        output = "DEPTH: " + str(self.depth) + " | COST: " + str(self.cost) + "\n"
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
            raise (ValueError)
        return self.cost < other.cost

    def __gt__(self, other):
        if type(other) != type(self):
            raise (ValueError)
        return self.cost > other.cost

    def __le__(self, other):
        if type(other) != type(self):
            raise (ValueError)
        return self.cost <= other.cost

    def __ge__(self, other):
        if type(other) != type(self):
            raise (ValueError)
        return self.cost >= other.cost


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = self.tuplify(init_state)
        self.goal_state = self.tuplify(goal_state)
        # self.actions = list()   # List of actions
        self.size = len(init_state)
        self.visited = set(self.init_state)  # Check is the state has appeared or not
        self.result, self.heap = [], []
        self.goal_position = {}
        self.rank = {}
        self.state_duplicated, self.node_visited, self.node_generated = 0, 0, 0
        for x, row in enumerate(goal_state):
            for y, ele in enumerate(row):
                self.goal_position[ele] = (x, y)
                self.rank[ele] = x * self.size + y

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

    def tuplify(self, list_2d):
        return tuple(map(tuple, list_2d))

    def listify(self, tuple_2d):
        return list(map(list, tuple_2d))

    def solvability(self, puzzle):
        puzzle = self.listify(puzzle)
        line = []
        for row in puzzle:
            line += row

        inverse_count = 0
        for i, tile in enumerate(line):
            for j in range(i + 1, len(line)):
                if self.rank[line[j]] <= self.rank[tile] and tile != 0 and line[j] != 0:
                    inverse_count += 1

        print("inverse: ", inverse_count)
        blank_x, _ = self.locate_tile(puzzle, 0)

        return (self.size % 2 == 1 and inverse_count % 2 == 0) \
               or (self.size % 2 == 0 and blank_x % 2 == 1 and inverse_count % 2 == 0) \
               or (self.size % 2 == 0 and blank_x % 2 == 0 and inverse_count % 2 == 1)

    def solve(self):  # Astar
        global maxSizeOfFrontier

        if not self.solvability(self.init_state):
            return ["UNSOLVABLE"]

        source = Node(self.init_state, self.heuristic(self.init_state), 0, None)
        self.heap = [(source.cost, source)]
        heapq.heapify(self.heap)
        ACTION = ["UP", "LEFT", "RIGHT", "DOWN"]
        MOVE = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        maxSizeOfFrontier = 0

        """
        This is the core part of A*
        """
        while len(self.heap) != 0:

            gc.collect()
            # max size of frontier
            if len(self.heap) > maxSizeOfFrontier:
                maxSizeOfFrontier = len(self.heap)

            current = heapq.heappop(self.heap)[1]
            if self.check_state(current.state):
                self.node_generated = len(self.heap) + self.node_visited
                return current.move

            self.node_visited += 1
            blank_x, blank_y = self.locate_tile(current.state, 0)

            for i in range(4):
                if len(current.move) > 0 and i == (3 - ACTION.index(current.move[len(current.move)-1])):  # Don't move back
                    continue

                puzzle = self.listify(current.state)
                dx, dy = MOVE[i]
                if blank_x + dx < 0 \
                        or blank_x + dx >= self.size \
                        or blank_y + dy < 0 \
                        or blank_y + dy >= self.size:
                    continue
                puzzle[blank_x][blank_y] = puzzle[blank_x + dx][blank_y + dy]

                puzzle[blank_x + dx][blank_y + dy] = 0

                puzzle = self.tuplify(puzzle)
                if puzzle in self.visited:
                    self.state_duplicated += 1
                    continue
                self.visited.add(puzzle)
                next_node = Node(puzzle, current.depth + 1 + self.heuristic(puzzle), current.depth + 1, current,
                                 current.move + [ACTION[i]])
                heapq.heappush(self.heap, (next_node.cost, next_node))

            del current

        return ["No Answer"]

    '''
    check_state is used to check if it's goal
    '''

    def check_state(self, puzzle):
        return puzzle == self.goal_state

    """
    implement heuristic functions here
    return the estimated steps
    h2: n-Max Swap
    """

    def heuristic(self, state):
        puzzle = self.listify(state)
        ans = 0

        misplaced_idx_dict = {}
        for i in range(self.size):
            for j in range(self.size):
                curr = puzzle[i][j]
                if curr != self.goal_state[i][j]:
                    misplaced_idx_dict[curr] = (i, j)

        while len(misplaced_idx_dict) != 0:
            if 0 in misplaced_idx_dict:
                curr_blank_x, curr_blank_y = misplaced_idx_dict[0]
                goal = self.goal_state[curr_blank_x][curr_blank_y]

                # swap 0 and goal, remove goal from misplaced
                misplaced_idx_dict[0] = misplaced_idx_dict[goal]
                misplaced_idx_dict[goal] = (curr_blank_x, curr_blank_y)
                del misplaced_idx_dict[goal]
                ans += 1
                continue
            else:
                curr_blank_x, curr_blank_y = self.goal_position[0]
                goal = list(misplaced_idx_dict.keys())[0]

                # swap 0 and goal, add 0 into misplaced
                misplaced_idx_dict[0] = misplaced_idx_dict[goal]
                misplaced_idx_dict[goal] = (curr_blank_x, curr_blank_y)
                ans += 1
                continue

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

    start = time.time()
    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()
    end = time.time()
    print("%.4f" % (end - start))

    print(len(ans))
    print(ans)
    print("# of duplicated state:", puzzle.state_duplicated)
    print("# of explored nodes:", puzzle.node_visited)
    print("# of generated nodes:", puzzle.node_generated)

    # print(ans) # Currently I just print the depth of the search

    # with open(sys.argv[2], 'a') as f:
    #     for answer in ans:
    #         f.write(answer+'\n')

class MyTester_AStar3(object):
    def __init__(self, input):
        self.input = input

    def test(self):
        try:
            f = open(self.input, 'r')
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
        start = time.time()
        solution = puzzle.solve()
        end = time.time()

        totalNodes = maxSizeOfFrontier
        totalTime = end-start
        numOfDupStates = puzzle.state_duplicated
        numOfExploredNodes = puzzle.node_visited
        numOfGenNodes = puzzle.node_generated


        return totalTime, solution, numOfDupStates, numOfExploredNodes, numOfGenNodes, maxSizeOfFrontier
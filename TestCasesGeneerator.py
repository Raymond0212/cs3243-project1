import copy
import json
import os
from random import randint
import subprocess
from BFS import MyTester_BFS
from CS3243_P1_25_2 import MyTester_AStar2
from CS3243_P1_25_3 import MyTester_AStar3
from CS3243_P1_25_4 import MyTester_AStar4
from TestCaseTester import testPls


def find_zero(state):
    for y in range(0, len(state)):
        for x in range(0, len(state[y])):
            if state[y][x] == 0:
                return x, y
    return None


def move(direction, state):
    newstate = copy.deepcopy(state)
    pos = find_zero(newstate)
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
        # Illegal move
        return None


def returnState(state):
    output = ""
    if state == None:
        return state
    else:
        for row in range(0, len(state)):
            s = ""
            for col in state[row]:
                s += str(col) + " "
            output += (s.strip() + "\n")

        return output.strip()


def printstate(state):
    if state == None:
        pass
    else:
        for row in range(0, len(state)):
            s = ""
            for col in state[row]:
                s += str(col) + " "


def genTestCase(n, id):
    goal_state = [[0 for i in range(n)] for j in range(n)]

    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    num_of_shuffles = randint(100, 2000)
    # num_of_shuffles = 1000
    directions = ["RIGHT", "LEFT", "UP", "DOWN"]

    for i in range(1, max_num + 1):
        goal_state[(i - 1) // n][(i - 1) % n] = i
    goal_state[n - 1][n - 1] = 0

    new_state = goal_state
    shuffles = 0
    for x in range(0, num_of_shuffles):
        direction = directions[randint(0, 3)]
        temp_state = move(direction, new_state)
        if temp_state is not None:
            shuffles = shuffles + 1
            new_state = temp_state

    f = open("n_equals_" + str(n) + "/input_" + str(id) + ".txt", "w")
    f.write(returnState(new_state))
    f.close()

    return "n_equals_" + str(n) + "/input_" + str(id) + ".txt"


def genNTestCase(n_size, num_of_cases):
    for i in range(n_size + 1, num_of_cases + n_size + 1):
        # Reason for this is because there is 3 sample test case for n=3, 4 sample test case for n=4 and 5 sample test case for n=5
        # Don't overwrite the given sample test cases
        genTestCase(n_size, i)


def engine(n_size, num_of_cases, algo_name):
    with open("summary_n" + str(n_size) + "_" + algo_name + ".txt", 'w') as f:
        f.write("{}")

    # for i in range(1, num_of_cases):
    #     genTestCase(n_size, i)

    for i in range(1, num_of_cases + n_size + 1):
        print(str(n_size) + ";" + str(i))
        # Reason for this is because there is 3 sample test case for n=3, 4 sample test case for n=4 and 5 sample test case for n=5
        inputFile = "n_equals_" + str(n_size) + "/input_" + str(i) + ".txt"
        myTester = None
        algo_names = ["BFS", "CS3243_P1_25_2", "CS3243_P1_25_3", "CS3243_P1_25_4"]

        if algo_name == algo_names[0]:
            myTester = MyTester_BFS(inputFile)
        elif algo_name == algo_names[1]:
            myTester = MyTester_AStar2(inputFile)
        elif algo_name == algo_names[2]:
            myTester = MyTester_AStar3(inputFile)
        elif algo_name == algo_names[3]:
            myTester = MyTester_AStar4(inputFile)
        else:
            print("Error, algo not found")

        # myTester returns a tuple containing totalNodes, totalTime, solution, numOfDupStates, numOfExploredNodes, numOfGenNodes
        resultsTuple = myTester.test()

        # testPls is a function that runs the solution found in the outputFile to see if the answer is correct
        passedTestCase = testPls(n_size, inputFile, resultsTuple[1])
        testName = "n_equals_" + str(n_size) + "/input_" + str(i) + ".txt"
        data = {}
        with open("summary_n" + str(n_size) + "_" + algo_name + ".txt", 'r') as f:
            data = json.loads(f.read())  # data becomes a dictionary

        newTestCase = {
            "algorithm": algo_name,
            "self.node_generated": resultsTuple[4],
            "self.node_visited": resultsTuple[3],
            "self.state_duplicated": resultsTuple[2],
            # "self.total_nodes": resultsTuple[0],
            "self.total_time": resultsTuple[0],
            # "solution": resultsTuple[1],
            "max size of frontier": resultsTuple[5],
            "isSolutionCorrect": passedTestCase
        }

        data[testName] = newTestCase
        print(data[testName])

        with open("summary_n" + str(n_size) + "_" + algo_name + ".txt", 'w') as f:
            f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    # Change this for the number of input files you want to create and test with (Excluding the 3 sample test cases
    # given for each n size
    num_of_cases = 100

    # prep, generates the input files for n=3, 4, 5
    # genNTestCase(3, num_of_cases)
    # genNTestCase(4, num_of_cases)
    # genNTestCase(5, num_of_cases)

    algo_names = ["BFS", "CS3243_P1_25_2", "CS3243_P1_25_3", "CS3243_P1_25_4"]

    # BFS runs n = 3 only
    # engine(3, num_of_cases, algo_names[0])

    # for n_size in range(3, 6):
    #     # # BFS
    #     # engine(n_size, num_of_cases, algo_names[0])
    #
    #     # Manhattan
    #     engine(n_size, num_of_cases, algo_names[1])
    #
    #     # h2: n-Max Swap
    #     engine(n_size, num_of_cases, algo_names[2])
    #
    #     # h3: Number of tiles out of row + Number of tiles out of column
    #     engine(n_size, num_of_cases, algo_names[3])
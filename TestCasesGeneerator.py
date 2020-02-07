import copy
from random import randint

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

def printstate(state):
    if state == None:
        print("Empty")
    else:
        for row in range(0, len(state)):
            s = ""
            for col in state[row]:
                s += str(col) + " "
            print(s.strip())

if __name__ == "__main__":
    # Instantiate a 2D list of size n x n
    ######CHANGE N TO WHATEVER YOU LIKE
    n = 3
    goal_state = [[0 for i in range(n)] for j in range(n)]

    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    #num_of_shuffles = randint(100, 200)
    num_of_shuffles = 10000
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

    print(str(shuffles) + "\n")
    printstate(new_state)








class Node:
    # defintion in AIMA3, page 78
    def __init__(self, state, parent = None, action = None, pathCost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.pathCost = pathCost

    # lambda for comparison in priority queue
    def __lt__(self, other):
        return self.pathCost < other.pathCost

    # check if node has the same state to other node
    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

# get the path from the final node by using pointer to the parent
def path(node):
    actions = []
    current = node

    while current.parent is not None:
        actions.append(current.action[0])
        current = current.parent

    actions.reverse()
    return actions

# definition in AIMA3, page 79
def childNode(problem, parent, action):
    newState = problem.result(parent.state, action)
    newPathCost = parent.pathCost + problem.stepCost(parent.state, action)
    return Node(state = newState, parent = parent, action = action, pathCost = newPathCost)


import heapq
class PriorityQueue:
    def __init__(self, order='min', f=lambda x: x):
        self.heap = []
        if order == 'min':
            self.f = f
        elif order == 'max':
            self.f = lambda x: -f(x)
        else:
            raise ValueError("Order must be either 'min' or 'max'.")

    def append(self, item):
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        for item in items:
            self.append(item)

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        return len(self.heap)

    def __contains__(self, key):
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)


# define the state with aresPos and stones
class State:
    def __init__(self, aresPos, stones):
        self.aresPos = aresPos
        self.stones = frozenset(stones)

    def __eq__(self, other):
        return self.aresPos == other.aresPos and self.stones == other.stones

    def __hash__(self):
        return hash((self.aresPos, self.stones))


# the state is can not be solved when a stone is in the corner but not it a switch
def isNotSolvable(grid, stonePos):
    x, y = stonePos

    if grid[x][y] in ('.', '*'):
        return False
        
    leftStuck = grid[x][y - 1] == '#'
    rightStuck = grid[x][y + 1] == '#'
    upStuck = grid[x - 1][y] == '#'
    downStuck = grid[x + 1][y] == '#'

    return (leftStuck and upStuck) or (leftStuck and downStuck) or (rightStuck and upStuck) or (rightStuck and downStuck)


# describe the problem with initialState, actions, goalTest
class Problem:
    def __init__(self, initialState, grid):
        self.initial = initialState
        self.grid = grid

    # consider if the current position is valid on the grid
    def isValid(self, pos, state):
        if self.grid[pos[0]][pos[1]] == '#':
            return False
        if any(isNotSolvable(self.grid, stonePos) for stonePos, _ in state.stones):
            return False
        return True
    
    # return all validActions of the problem in current state
    def actions(self, state):
        moves = {
            'u': (-1, 0), 'd': (1, 0), 
            'l': (0, -1), 'r': (0, 1)
        }
        validActions = []

        for move, (dx, dy) in moves.items():
            newPos = (state.aresPos[0] + dx, state.aresPos[1] + dy)

            if self.isValid(newPos, state):
                # if Ares push a stone
                if any(newPos == stonePos for stonePos, _ in state.stones):
                    stonePos = (newPos[0] + dx, newPos[1] + dy)

                    if self.isValid(stonePos, state) and all(stonePos != s[0] for s in state.stones):
                        validActions.append((move.upper(), (dx, dy)))
                else:
                    validActions.append((move, (dx, dy)))

        return validActions


    # consider if the current state is the goal state of problem
    def goalTest(self, state):
        return all(self.grid[stonePos[0]][stonePos[1]] in ('.', '*') for stonePos, _ in state.stones)


    # return the stepCost from the parent state to the child state by action
    def stepCost(self, state, action):
        move, (dx, dy) = action
        newPos = (state.aresPos[0] + dx, state.aresPos[1] + dy)

        for (stonePos, weight) in state.stones:
            if newPos == stonePos:
                pushed_stone_pos = (stonePos[0] + dx, stonePos[1] + dy)

                if self.isValid(pushed_stone_pos, state):
                    return 1 + weight

        return 1

    
    # return the child state of parent state by action
    def result(self, state, action):
        move, (dx, dy) = action
        newAresPos = (state.aresPos[0] + dx, state.aresPos[1] + dy)
        newStones = set()

        for (stonePos, weight) in state.stones:
            if newAresPos == stonePos:
                pushedStonePos = (stonePos[0] + dx, stonePos[1] + dy)
                newStones.add((pushedStonePos, weight))

            else:
                newStones.add((stonePos, weight))

        return State(newAresPos, newStones)


# implement UCS with algorithm in AIMA3, page 84
def uniformCostSearch(problem, f = None):
    node = Node(problem.initial)
    frontier = PriorityQueue(f = f)
    frontier.append(node)
    explored = set()
    
    # set up the values for final result
    nodeGenerated = 1

    while frontier:
        node = frontier.pop()

        # use for debugging
        # print(f"Processing Node: Ares Position: {node.state.aresPos}, Stones: {node.state.stones}, Path Cost: {node.pathCost}")

        if problem.goalTest(node.state):
            return node, nodeGenerated

        explored.add(node.state)

        for action in problem.actions(node.state):
            child = childNode(problem, node, action)

            # increase number of nodes
            nodeGenerated += 1
            
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            
            elif child in frontier:
                # if child is in frontier with higher pathCost
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    
    return None, None


# read the input file
def readInput(filePath):
    with open(filePath, 'r') as f:
        lines = f.readlines()

    weights = list(map(int, lines[0].strip().split(' ')))
    grid = [list(line.rstrip()) for line in lines[1:]]

    aresPos = None
    stones = []

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == '@' or cell == '+':
                aresPos = (r, c)
            elif cell == '$' or cell == '*':
                stones.append(((r, c), weights.pop(0)))

    initialState = State(aresPos, stones)
    problem = Problem(initialState, grid)
    return problem


# main function
import time
import tracemalloc
def UCS(input,output):
    problem = readInput(input)

    start_time = time.time()
    tracemalloc.start()

    node, nodeGenerated = uniformCostSearch(problem, lambda node: node.pathCost)

    if (node == None):
        print("No solution")
        return

    pathSequence = ''.join(path(node))
    numSteps = len(path(node))
    weightPushed = node.pathCost - numSteps

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()

    total_time = (end_time - start_time) * 1000
    total_memory = peak / 10**6

    with open(output, 'a') as f:
        f.write('UCS\n')
        f.write(f'Steps: {numSteps}, Weight: {weightPushed}, Nodes: {nodeGenerated},')
        f.write(f' Time (ms): {total_time:.2f}, Memory (MB): {total_memory:.2f}\n')
        f.write(f'{pathSequence}\n')

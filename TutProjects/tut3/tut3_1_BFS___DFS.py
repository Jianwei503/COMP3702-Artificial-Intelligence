import queue

"""
Now lets consider our agent design, here we will create our state representation and transition function, 
as well as define some costs and heuristics we will use for UCS and A*.

The only thing that changes for our agent is the x,y corrdinates (coord), so this will be our state, 
however it is still useful to keep track of a few other things. The number of rows and columns in the 
grid, an id representation that we can use to compare different objects, and the cost.

In the transition (step) function we again take in a state, determine its validity, and create a new state, 
we can check its validity by determining if the resulting state given an action would be coincidental 
with the coordinates of an obstacle.

Lastly we have some functions for overriding the equality and less than operators and estimating the 
heuristic. In this case we will treate the heuristic as the manhattan distance between the current 
position and the destination, which is also the number of cells between the current position and 
destination. In order for this heuristic to be admissable it needs to not overrestimate the true 
lowest cost from the currrent position to the destination, in Exercise 3.2, the true lowest cost is 
the lowest number amongst all paths to the destination, taking the sum of the costs for each grid 
element. Since the lowest cost for any element is 1,the manhattan distance is indeed admissable.
"""


class GridWorldState():

    def __init__(self, coord, cost, obstacle_coords=[], cost_map=[]):
        self.ncol = self.nrow = 9
        self.id = coord
        self.coord = coord
        self.cost = cost
        self.total_cost = cost
        # Ecercise 3.1
        self.obstacle_coords = obstacle_coords
        # Exercise 3.2
        self.cost_map = cost_map

    def step(self, action):
        row, col = self.coord
        next_row, next_col = row, col

        if action == 'L':
            next_col = max(col - 1, 0)
        elif action == 'R':
            next_col = min(col + 1, self.ncol - 1)
        elif action == 'U':
            next_row = max(row - 1, 0)
        elif action == 'D':
            next_row = min(row + 1, self.nrow - 1)

        next_state_coord = (next_row, next_col)

        # Exercise 3.1
        if next_state_coord in self.obstacle_coords:
            next_state_coord = self.coord

        # Exercise 3.2
        next_state_cost = 0
        if self.cost_map:
            next_state_cost = self.cost_map[next_state_coord[0]][next_state_coord[1]]

        next_state = GridWorldState(next_state_coord, next_state_cost, self.obstacle_coords,
                                    self.cost_map)
        return next_state

    def estimate_cost_to_go(self, goal):
        cost_to_go_estimate = abs(goal.coord[0] - self.coord[0])
        cost_to_go_estimate += abs(goal.coord[1] - self.coord[1])
        return cost_to_go_estimate

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.total_cost < other.total_cost

# Given our state and transition functions we construct the environment for our agent.
if __name__ == "__main__":
    nrow = ncol = 9
    obstacle_map = []
    obstacle_map.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    obstacle_map.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    obstacle_map.append([0, 0, 1, 1, 1, 1, 1, 0, 0])
    obstacle_map.append([0, 0, 0, 0, 0, 0, 1, 0, 0])
    obstacle_map.append([0, 0, 0, 0, 0, 0, 1, 0, 0])
    obstacle_map.append([0, 0, 0, 0, 0, 0, 1, 0, 0])
    obstacle_map.append([0, 0, 0, 0, 0, 0, 1, 0, 0])
    obstacle_map.append([0, 0, 0, 1, 1, 1, 1, 0, 0])
    obstacle_map.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

    obstacle_coords = [(row, col) for row in range(nrow) \
                    for col in range(ncol) if obstacle_map[row][col]==1]

    actionset = ['L', 'R', 'U', 'D']

    start = GridWorldState(coord = (8,0), cost = 0, obstacle_coords=obstacle_coords)
    goal  = GridWorldState(coord = (0,8), cost = 0, obstacle_coords=obstacle_coords)


# Finally we begin our search, in BFS, we create a queue, add our starting element, and begin
# searching its neighbours until we find the goal, similar to previous week.
    explored = set() # need hashable objects!
    fringe = queue.Queue()
    fringe.put((start, []))

    reachedEnd = False
    while fringe.qsize() > 0:
        current, path = fringe.get()
        explored.add(current.id)
        for action in actionset: # "simulate" executing actions
            neighbor = current.step(action)
            if neighbor==goal:
                print ("reached the end, jolly good")
                print (path + [action])
                reachedEnd = True
                break;
            if neighbor.id in explored:
                continue
            fringe.put((neighbor, path + [action]))
        if reachedEnd:
            break


# For iterative deepening, we perform DFS until we reach the end or a certain depth in our tree,
# when we reach the maximum depth, we increase its upper bound and start again.
    max_depth = 1000 # problem-specific, guess: some reasonable finite positive number

    # outer loop
    reachedEnd = False
    for max_depth_i in range(1, max_depth + 1):
        explored = set()
        fringe = queue.LifoQueue()
        fringe.put((start, []))

        while fringe.qsize() > 0:
            current, path = fringe.get()
            if current==goal:
                print ("reached the end, jolly good")
                print (path)
                reachedEnd = True
                break
            if current.id in explored:
                continue
            if (max_depth is not None) and (len(path)==max_depth_i):
                continue
            explored.add(current.id)
            for action in actionset: # "simulate" executing actions
                neighbor = current.step(action)
                if neighbor.id not in explored:
                    fringe.put((neighbor, path + [action]))
        if reachedEnd:
            break

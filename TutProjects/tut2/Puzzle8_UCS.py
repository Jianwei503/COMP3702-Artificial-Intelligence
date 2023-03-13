import heapq
from queue import *


# state representation
class Node:
    def __init__(self):
        self.grid = []
        self.children = []
        self.parent = None
        self.previous_action = ""
        self.cost = 0

        # transition function for action Left

    def get_child(self, action):
        # treat the tile as '0'
        index = self.grid.index(0)
        new_node = None
        if action == "Left":
            # check for validity
            if not (index == 0 or index == 3 or index == 6):
                # swap tile with left element
                new_node = Node()
                # deep copy the grid
                new_node.grid = self.grid[:]
                new_node.grid[index] = new_node.grid[index - 1]
                new_node.grid[index - 1] = 0
                # also set us to be the parent of the child
                new_node.parent = self
                new_node.cost = self.cost + 3

        # We can do something similar for the other actions

        if action == "Right":
            # check for validity
            if not (index == 2 or index == 5 or index == 8):
                # swap tile with Right element
                new_node = Node()
                new_node.grid = self.grid[:]
                new_node.grid[index] = new_node.grid[index + 1]
                new_node.grid[index + 1] = 0
                new_node.parent = self
                new_node.cost = self.cost + 4

        if action == "Up":
            if not (index <= 2):
                # swap tile with Top element
                new_node = Node()
                new_node.grid = self.grid[:]
                new_node.grid[index] = new_node.grid[index - 3]
                new_node.grid[index - 3] = 0
                new_node.parent = self
                new_node.cost = self.cost + 1

        if action == "Down":
            if not (index >= 6):
                # swap tile with Bottom element
                new_node = Node()
                new_node.grid = self.grid[:]
                new_node.grid[index] = new_node.grid[index + 3]
                new_node.grid[index + 3] = 0
                new_node.parent = self
                new_node.cost = self.cost + 2

        if new_node:
            new_node.previous_action = action
            return new_node

    # override equality - needed to check when 2 states are equal
    def __eq__(self, obj):
        """self == obj."""
        return self.grid == obj.grid

    # override less than function for UCS
    def __lt__(self, obj):
        return self.cost < obj.cost


"""
The Last part is to convert our BFS code to UCS. The difference here is that UCS 
keeps track of the cost of actions. We are given that the cost of actions is 
{Up=1, Down=2, Left=3, Right=4}. In other words, going up 4 times holds the same 
weight as going right once. We are no longer concerned with minimizing the 
number of moves, instead we want to minimize the cost.

In our Node class above we keep track of the aggregate cost from the start 
position to each new state. To make use of this we will use a priority queue 
(heapq), which takes elements out that have the smallest cost.
"""

if __name__ == "__main__":
    init_state = Node()
    init_state.grid = [1, 2, 3, 4, 5, 6, 0, 7, 8]
    goal_state = Node()
    goal_state.grid = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    visited = []

    pq = []
    pq.append(init_state)
    heapq.heapify(pq)

    while pq:
        node = heapq.heappop(pq)
        print("node:", node.grid)
        if node.grid == goal_state.grid:
            print("We Reached the goal, Jolly Good!")
            break;

        for action in ["Up", "Down", "Right", "Left"]:
            child = node.get_child(action)
            # child not in visited works since we overloaded the equality operator
            if child and child not in visited:
                print("start:", node.grid, "end:", child.grid, action)
                heapq.heappush(pq, child)

    actions = []
    # initial node has no parent
    while node.parent:
        actions.append(node.previous_action)
        node = node.parent
    # reverse it to get the correct order
    actions.reverse()
    print("Number of actions:", len(actions))
    print(actions)

"""
Notice that very little changed from the previous code, we replaced the queue 
with the heapq. The heapq will always take the item with the lowest value from 
the queue. Since we overrode the less than lt operator in our class, the heapq 
knows how to compare the elements.
"""
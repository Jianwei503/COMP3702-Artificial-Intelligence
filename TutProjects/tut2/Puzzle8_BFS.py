"""
Let us recall the components we need for an agent.

- Action Space (A)
- Percept Space (P)
- State Space (S)
- Transition Function (T : S x A -> S')
- Utility Function (U: R -> R)
We know the problem is fully observable, thus the percept space is the same as
the state space and we dont need to do anything special while considering it.
For BFS and DFS problems there is no cost associated with actions, the utility
will therefore become 1 for reaching the goal state and 0 otherwise.

That leaves us with action space, state space, and transition function.

In the 8-puzzle game there are 4 actions that are available to us, Up, Right,
Down, Left. These 4 actions make up the action space, the actions are not all
always vailable, however we will worry about that when getting to the transition
function.

The transition function is the core of the problem, given a state and an action
we need a way to find the next state. The implementation for this will largely
depend on the state space, so lets start with that.

Lets start by defining the state space in terms of python code, there are a few
things we will be interested in.

- The grid layout - what numbers are in what positions, we will treat this as a
list, however there are a number of ways we can model it
- The children of each state
- Is the cell visited or not
- What action led to here
Well also keep track of the cost, this is not needed for BFS and DFS, however is
very important when we get to UCS.

Too keep track of all these properties, lets start by defining a class. Well also
import the queue class and the heapq class, well need it later.
"""
from queue import *

"""
Next, still in our class we can define the transition function, we need to do 2 
things here. Firstly we need to check that the action given is valid, and second 
we need to perform the action.

We can check if the action is valid by getting the current index of the tile. We 
know that the action Left is invalid in the left row, and we also know that the 
left row has elements 0, 3 and 6 in out Node.grid list, hence if the tile index 
is in one of those positions, the action Left is impossible.

While we are making children, we can also keep track of the childs parent and 
the action that led to the child.
"""
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
Youll notice we also made an eq function and lt, this is an override for the 
equality operator (==), which allows us to determine under what conditions 2 
classes are equal (obj1 == obj2), and the less than operator (<), which we will 
use for UCS.

This is all the basics we need for our state and transition components. Now we 
need to perform our search.

For testing, lets create an initial state and a goal state.

Well also start with BFS, so well need to create a queue, and well put our 
initial state into it.

Well also need some way to keep track of states that were already visited, so 
well make a list for that.
"""

# python entry point
if __name__ == "__main__":
    init_state = Node()
    init_state.grid = [1, 2, 3, 4, 5, 6, 0, 7, 8]
    goal_state = Node()
    goal_state.grid = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    visited = []
    # visited = set()

    q = Queue()
    q.put(init_state)

# Now lets start our search, reacll that the basic structure of search is to take
# items out of the queue, get its successors, and put them into the queue.

    while not q.empty():
        node = q.get()
        visited.append(node)
        # if node in visited:
        #     print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
        # visited.add(node)
        print("node:", node.grid)
        if node == goal_state: #__eq__(self, obj):
            print("We Reached the goal, Jolly Good!")
            break;

        for action in ["Up", "Down", "Right", "Left"]:
            child = node.get_child(action)
            # child not in visited works since we overloaded the equality operator
            if child and child not in visited:
                print("start:", node.grid, "end:", child.grid, action)
                q.put(child)
# To get the actions to get here we can backtrack from the goal up the chain
# of parents.
    actions = []
    # initial node has no parent
    while node.parent:
        actions.append(node.previous_action)
        node = node.parent
    # reverse it to get the correct order
    actions.reverse()
    print ("Number of actions:", len(actions))
    print (actions)

"""
Thats the core od BFS, to change it to DFS, we just have to recall that DFS uses 
a stack, so we would switch over the queue in the code above to a stack and were done.
"""
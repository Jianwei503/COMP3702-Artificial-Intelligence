#!/usr/bin/python
import copy
import queue
import time
import sys

from laser_tank import LaserTankMap

"""
Template file for you to implement your solution to Assignment 1.

COMP3702 2020 Assignment 1 Support Code
"""

# Code for any classes or functions you need can go here.
class Node:
    """
    Instance of a searching state.
    """
    def __init__(self):
        """
        Build a Node instance.
        """
        self.map = LaserTankMap(0, 0, None, 0, 0, 0)
        self.total_cost = 0
        self.id = 0

    # override equality - needed to check when 2 nodes are equal
    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.total_cost < other.total_cost

def find_flag(map):
    """
    Travrse the grid_data of map(LaserTankMap) and find the coordinate of flag
    :param map: a LaserTankMap
    :return: coordinate of flag
    """
    for i in range(map.y_size):
        for j in range(map.x_size):
            if map.grid_data[i][j] == 'F':
                return (j, i)

def write_output_file(filename, actions):
    """
    Write a list of actions to an output file. You should use this method to write your output file.
    :param filename: name of output file
    :param actions: list of actions where is action is in LaserTankMap.MOVES
    MOVES = [MOVE_FORWARD, TURN_LEFT, TURN_RIGHT, SHOOT_LASER]
    """
    f = open(filename, 'w')
    for i in range(len(actions)):
        f.write(str(actions[i]))
        if i < len(actions) - 1:
            f.write(',')
    f.write('\n')
    f.close()


def main(arglist):
    input_file = arglist[0]
    output_file = arglist[1]

    # Read the input testcase file
    game_map = LaserTankMap.process_input_file(input_file)

    actions = []

    # Code for main method.
    action_set = ['f', 'l', 'r', 's']
    goal = find_flag(game_map)
    start = Node()
    start.map = game_map

    fringe = queue.PriorityQueue()
    fringe.put(start)
    path = {start.id: []}
    explored = {start.id: 1}

    while not fringe.empty():
        parent = fringe.get()
        # Check if the finish condition (player at flag) has been reached
        if parent.map.is_finished():
            actions = path[parent.id]
            break
        for move in action_set:
            child = Node()
            child.map = copy.deepcopy(parent.map)
            if not child.map.apply_move(move):
                child.id = hash((child.map.player_x,
                                 child.map.player_y,
                                 child.map.player_heading,
                                 str(child.map.grid_data)))
                cost_so_far = explored.get(parent.id) + 1
                if (child.id not in explored) or (cost_so_far < explored.get(child.id)):
                    explored[child.id] = cost_so_far
                    path[child.id] = path.get(parent.id) + [move]
                    # Manhattan distance between current position and flag
                    child.total_cost = cost_so_far \
                                       + abs(child.map.player_x - goal[0]) \
                                       + abs(child.map.player_y - goal[1])
                    fringe.put(child)
            # del new_map
            # gc.collect() # save memory

    # Write the solution to the output file
    write_output_file(output_file, actions)

    print("Steps: {}".format(len(actions)))

# if __name__ == '__main__':
#     main(sys.argv[1:])

if __name__ == '__main__':
    time_start = time.perf_counter()
    main(sys.argv[1:])
    time_end = time.perf_counter()
    print("Run time: {}".format(time_end - time_start))
#!/usr/bin/python
import copy
import ctypes
import heapq
import math
import time
import sys

from laser_tank import LaserTankMap

"""
Template file for you to implement your solution to Assignment 1.

COMP3702 2020 Assignment 1 Support Code
"""


#
#
# Code for any classes or functions you need can go here.
#
class Node:
    def __init__(self, player_x=0, player_y=0, player_heading=0, grid_data=[]):
        # self.map = LaserTankMap(2, 2, None, 0, 0, 0)
        # self.player_x = player_x
        # self.player_y = player_y
        self.coord = (player_x, player_y)
        self.heading = player_heading
        self.grid = grid_data
        self.distance = 0 # Manhattan distance between current position and flag
        self.steps = 0
        self.previous_move = None
        self.parent = None

    # override equality - needed to check when 2 nodes are equal
    def __eq__(self, other):
        return (self.grid == other.grid) \
               and (self.coord == other.coord) \
               and (self.heading == other.heading)

    # def __hash__(self):
    #     return hash((self.coord, self.heading, str(self.grid)))

    def __lt__(self, other):
        return self.steps + self.distance < other.steps + other.distance

def find_flag(map):
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
    goal = find_flag(game_map)
    init_state = \
        Node(game_map.player_x, game_map.player_y, game_map.player_heading, game_map.grid_data)
    # visited = set()
    visited = []

    priority_queue = []
    priority_queue.append(init_state)
    heapq.heapify(priority_queue)

    while priority_queue:
        node = heapq.heappop(priority_queue)
        # visited.add(node)
        visited.append(node)
        # Check if the finish condition (player at flag) has been reached
        if node.coord == goal:
            break

        for move in ['f', 'l', 'r', 's']:
            # deepcopy entire game map of previous state
            new_map = copy.deepcopy(game_map)
            new_map.player_x = node.coord[0]
            new_map.player_y = node.coord[1]
            new_map.grid_data = copy.deepcopy(node.grid)
            new_map.player_heading = node.heading
            if not new_map.apply_move(move): # moved successfully, apply_move() returns 0
                # generate current state
                child = Node()
                child.coord = (new_map.player_x, new_map.player_y)
                child.heading = new_map.player_heading
                child.grid = new_map.grid_data
                if child not in visited:
                    child.parent = id(node)
                    child.previous_move = move
                    child.steps = node.steps + 1
                    child.distance = (abs(child.coord[0] - goal[0]) + abs(child.coord[1] - goal[1])) * 2
                    heapq.heappush(priority_queue, child)
            del new_map

    while node.parent:
        actions.append(node.previous_move)
        node = ctypes.cast(node.parent, ctypes.py_object).value
    # reverse actions' list to get the correct order
    actions.reverse()
    # Write the solution to the output file
    write_output_file(output_file, actions)

    print("Steps: {}".format(len(actions)))

# if __name__ == '__main__':
#     main(sys.argv[1:])

if __name__ == '__main__':
    start = time.perf_counter()
    main(sys.argv[1:])
    end = time.perf_counter()
    print("Run time: {}".format(end - start))
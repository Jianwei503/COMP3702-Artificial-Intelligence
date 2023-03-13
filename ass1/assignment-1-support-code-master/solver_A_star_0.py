#!/usr/bin/python
import copy
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
#
class Node:
    def __init__(self):
        self.map = LaserTankMap(2, 2, None, 0, 0, 0)
        self.distance = 0 # Manhattan distance between current position and flag
        self.steps = 0
        self.previous_move = None
        self.parent = None

    # override equality - needed to check when 2 nodes are equal
    def __eq__(self, other):
        return (self.map.grid_data == other.map.grid_data) \
               and (self.map.player_x == other.map.player_x) \
               and (self.map.player_y == other.map.player_y) \
               and (self.map.player_heading == other.map.player_heading)

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
    flag_position = find_flag(game_map)
    init_state = Node()
    init_state.map = game_map
    visited = []

    priority_queue = []
    priority_queue.append(init_state)
    heapq.heapify(priority_queue)

    while priority_queue:
        node = heapq.heappop(priority_queue)
        visited.append(node)
        # Check if the finish condition (player at flag) has been reached
        if node.map.is_finished():
            break

        for move in ['f', 'l', 'r', 's']:
            child = copy.deepcopy(node) # deepcopy current state
            # moved successfully, apply_move() returns 0
            if child and not child.map.apply_move(move) and (child not in visited):
                child.parent = copy.deepcopy(node)
                child.previous_move = move
                child.steps += 1
                child.distance = abs(child.map.player_x - flag_position[0]) \
                                 + abs(child.map.player_y - flag_position[1])
                heapq.heappush(priority_queue, child)

    while node.parent:
        actions.append(node.previous_move)
        node = node.parent
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
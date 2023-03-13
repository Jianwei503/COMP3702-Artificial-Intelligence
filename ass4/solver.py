import time

from laser_tank import LaserTankMap, DotDict
import random

"""
Template file for you to implement your solution to Assignment 4. You should implement your solution by filling in the
following method stubs:
    train_q_learning()
    train_sarsa()
    get_policy()
    
You may add to the __init__ method if required, and can add additional helper methods and classes if you wish.

To ensure your code is handled correctly by the autograder, you should avoid using any try-except blocks in your
implementation of the above methods (as this can interfere with our time-out handling).

COMP3702 2020 Assignment 4 Support Code
"""


class Solver:
    ANTI_TANKS = [LaserTankMap.ANTI_TANK_UP_SYMBOL, LaserTankMap.ANTI_TANK_DOWN_SYMBOL,
                  LaserTankMap.ANTI_TANK_LEFT_SYMBOL, LaserTankMap.ANTI_TANK_RIGHT_SYMBOL]
    PLAYER_SYMBOLS = [LaserTankMap.PLAYER_UP_SYMBOL, LaserTankMap.PLAYER_DOWN_SYMBOL,
                      LaserTankMap.PLAYER_LEFT_SYMBOL, LaserTankMap.PLAYER_RIGHT_SYMBOL]

    def __init__(self):
        """
        Initialise solver without a Q-value table.
        """
        # self.alpha = 0.001
        self.alpha = 0.05
        self.episode = 2000


        self.epsilon = 0.8
        self.safe_positions = None
        self.q_values = None

    def get_land_tiles(self, state):
        """
        Traverse the grid_data and find out all the possible player positions
        @param state: LaserTankMap instance
        """
        anti_tank_tiles = []
        land_tiles = set()
        # find all land positions
        for x in range(state.x_size):
            for y in range(state.y_size):
                if state.grid_data[y][x] == LaserTankMap.LAND_SYMBOL \
                        or state.grid_data[y][x] in Solver.PLAYER_SYMBOLS:
                    for i in range(4):
                        land_tiles.add((x, y, i))
                # find all anti tanks' positions
                elif state.grid_data[y][x] in Solver.ANTI_TANKS:
                    anti_tank_tiles.append((x, y))

        # weed out all the positions which face the anti tanks directly
        for tile in land_tiles:
            for anti_tank in anti_tank_tiles:
                if anti_tank == LaserTankMap.ANTI_TANK_UP_SYMBOL and tile[0] == anti_tank[0] \
                        and tile[1] < anti_tank[1]:
                    land_tiles.remove(tile)
                elif anti_tank == LaserTankMap.ANTI_TANK_DOWN_SYMBOL and tile[0] == anti_tank[0] \
                        and tile[1] > anti_tank[1]:
                    land_tiles.remove(tile)
                elif anti_tank == LaserTankMap.ANTI_TANK_LEFT_SYMBOL and tile[1] == anti_tank[1] \
                        and tile[0] < anti_tank[0]:
                    land_tiles.remove(tile)
                elif anti_tank == LaserTankMap.ANTI_TANK_RIGHT_SYMBOL and tile[1] == anti_tank[1] \
                        and tile[0] > anti_tank[0]:
                    land_tiles.remove(tile)
        self.safe_positions = list(land_tiles)

    def random_restart(self, state):
        """
        Restart the agent in a safe random map location, avoiding obstacles and anti_tanks
        """
        loc = random.choice(self.safe_positions)
        state.reset_to_start()
        state.player_x, state.player_y, state.player_heading = loc[0], loc[1], loc[2]

    def choose_action_q(self, state, q_table):
        """
        Choose an action by exploration strategy
        @param state:
        @param q_table:
        @return: the action chose, the q value corresponds to the action
        """
        key = hash(state)
        a_q = q_table.get(key)
        if a_q is None:
            q_table[key] = {LaserTankMap.MOVE_FORWARD: .0,
                            LaserTankMap.TURN_LEFT: .0,
                            LaserTankMap.TURN_RIGHT: .0,
                            LaserTankMap.SHOOT_LASER: .0}
            action = random.choice(LaserTankMap.MOVES)
            return action, .0
        elif random.random() > self.epsilon:
            action = random.choice(LaserTankMap.MOVES)
            return action, a_q[action]
        else:
            action = max(a_q, key=a_q.get)
            return action, a_q[action]

    def train_q_learning(self, simulator):
        """
        Train the agent using Q-learning, building up a table of Q-values.
        :param simulator: A simulator for collecting episode data (LaserTankMap instance)
        """
        self.get_land_tiles(simulator)
        # Q(s, a) table
        # suggested format: key = hash(state), value = dict(mapping actions to values)
        q_values = {}

        # episode = 1000000
        episode = self.episode
        start = time.time()
        while episode > 0 and (time.time() - start) < simulator.time_limit - 0.5:
            self.random_restart(simulator)
            finished = False
            while not finished:
                current_key = hash(simulator)
                action, current_q = self.choose_action_q(simulator, q_values)
                reward, end = simulator.apply_move(action)
                a_v = q_values.get(hash(simulator))
                if a_v is None:
                    next_max_q = .0
                else:
                    next_max_q = max(a_v.values())
                current_q += self.alpha * (reward + simulator.gamma * next_max_q - current_q)
                q_values[current_key][action] = current_q
                finished = end
            episode -= 1

        # store the computed Q-values
        self.q_values = q_values

    def train_sarsa(self, simulator):
        """
        Train the agent using SARSA, building up a table of Q-values.
        :param simulator: A simulator for collecting episode data (LaserTankMap instance)
        """
        self.get_land_tiles(simulator)
        # Q(s, a) table
        # suggested format: key = hash(state), value = dict(mapping actions to values)
        q_values = {}

        episode = self.episode
        start = time.time()
        while episode > 0 and (time.time() - start) < simulator.time_limit - 0.5:
            self.random_restart(simulator)
            finished = False
            while not finished:
                current_key = hash(simulator)
                action, current_q = self.choose_action_q(simulator, q_values)
                reward, end = simulator.apply_move(action)
                next_a, next_q = self.choose_action_q(simulator, q_values)
                current_q += self.alpha * (reward + simulator.gamma * next_q - current_q)
                q_values[current_key][action] = current_q
                finished = end
            episode -= 1

        # store the computed Q-values
        self.q_values = q_values

    def get_policy(self, state):
        """
        Get the policy for this state (i.e. the action that should be performed at this state).
        :param state: a LaserTankMap instance
        :return: pi(s) [an element of LaserTankMap.MOVES]
        """
        key = hash(state)
        a_q = self.q_values.get(key)
        if a_q is None:
            action = random.choice(LaserTankMap.MOVES)
            return action
        else:
            action = max(a_q, key=a_q.get)
            return action

from laser_tank import LaserTankMap, DotDict
import time

"""
Template file for you to implement your solution to Assignment 3. You should implement your solution by filling in the
following method stubs:
    run_value_iteration()
    run_policy_iteration()
    get_offline_value()
    get_offline_policy()
    get_mcts_policy()
    
You may add to the __init__ method if required, and can add additional helper methods and classes if you wish.

To ensure your code is handled correctly by the autograder, you should avoid using any try-except blocks in your
implementation of the above methods (as this can interfere with our time-out handling).

COMP3702 2020 Assignment 3 Support Code
"""

# directions
FORWARD_LEFT = 'FL'
FORWARD_RIGHT = 'FR'
MOVE_LEFT = 'LT'
MOVE_RIGHT = 'RT'
NO_CHANGE = 'NC'

class Solver:

    def __init__(self, game_map):
        self.game_map = game_map
        self.states = list()
        self.values = dict()
        self.policy = dict()

        for y in range(1, self.game_map.y_size - 1):
            for x in range(1, self.game_map.x_size - 1):
                if not self.game_map.grid_data[y][x] == '#':
                    for d in LaserTankMap.DIRECTIONS:
                        state = self.game_map.make_clone()
                        state.player_x, state.player_y, state.player_heading = x, y, d
                        self.states.append(state)

        for s in self.states:
            self.values[s] = 0
            self.policy[s] = LaserTankMap.TURN_RIGHT

    def stoch_action(self, a):
        # Stochasitc actions probability distributions
        if a == LaserTankMap.MOVE_FORWARD:
            stoch_a = {LaserTankMap.MOVE_FORWARD: self.game_map.t_success_prob}
                       # FORWARD_LEFT: self.game_map.t_error_prob * (1 / 5),
                       # FORWARD_RIGHT: self.game_map.t_error_prob * (1 / 5),
                       # MOVE_LEFT: self.game_map.t_error_prob * (1 / 5),
                       # MOVE_RIGHT: self.game_map.t_error_prob * (1 / 5),
                       # NO_CHANGE: self.game_map.t_error_prob * (1 / 5), }
        elif a == LaserTankMap.TURN_LEFT:
            stoch_a = {LaserTankMap.TURN_LEFT: 1}
        elif a == LaserTankMap.TURN_RIGHT:
            stoch_a = {LaserTankMap.TURN_RIGHT: 1}
        elif a == LaserTankMap.SHOOT_LASER:
            stoch_a = {LaserTankMap.SHOOT_LASER: 1}
        return stoch_a

    def attempt_move(self, state, action):
        new_s = state.make_clone()
        if action == FORWARD_LEFT:
            r1 = new_s.apply_move(LaserTankMap.MOVE_FORWARD)
            r2 = new_s.apply_move(LaserTankMap.TURN_LEFT)
            r3 = new_s.apply_move(LaserTankMap.MOVE_FORWARD)
            r4 = new_s.apply_move(LaserTankMap.TURN_RIGHT)
            r = r1 + r2 + r3 + r4
            return new_s, r
        elif action == FORWARD_RIGHT:
            r1 = new_s.apply_move(LaserTankMap.MOVE_FORWARD)
            r2 = new_s.apply_move(LaserTankMap.TURN_RIGHT)
            r3 = new_s.apply_move(LaserTankMap.MOVE_FORWARD)
            r4 = new_s.apply_move(LaserTankMap.TURN_LEFT)
            r = r1 + r2 + r3 + r4
            return new_s, r
        elif action == MOVE_LEFT:
            r1 = new_s.apply_move(LaserTankMap.TURN_LEFT)
            r2 = new_s.apply_move(LaserTankMap.MOVE_FORWARD)
            r3 = new_s.apply_move(LaserTankMap.TURN_RIGHT)
            r = r1 + r2 + r3
            return new_s, r
        elif action == MOVE_RIGHT:
            r1 = new_s.apply_move(LaserTankMap.TURN_RIGHT)
            r2 = new_s.apply_move(LaserTankMap.MOVE_FORWARD)
            r3 = new_s.apply_move(LaserTankMap.TURN_LEFT)
            r = r1 + r2 + r3
            return new_s, r
        elif action == NO_CHANGE:
            return state, -1
        else:
            r = new_s.apply_move(action)
            return new_s, r

    def dict_argmax(self, d):
        max_value = max(d.values())
        for k, v in d.items():
            if v == max_value:
                return k

    def run_value_iteration(self):
        """
        Build a value table and a policy table using value iteration, and store inside self.values and self.policy.
        """
        converged = False
        start = time.time()
        count = 0 ##############################
        while not converged:
            count += 1 ############################
            new_values = dict()
            for s in self.states:
                action_values = list()
                for a in LaserTankMap.MOVES:
                    total = 0
                    for action, p in self.stoch_action(a).items():
                        s_next, r = self.attempt_move(s, action)
                        total += p * (r + (self.game_map.gamma * self.values[s_next]))
                    action_values.append(total)
                new_values[s] = max(action_values)

            differences = [abs(self.values[s] - new_values[s]) for s in self.states]
            if max(differences) < self.game_map.epsilon:
                converged = True
                print(time.time() - start) ###########################
                print(count)

            end = time.time()
            if (end - start) > (self.game_map.time_limit - 0.5):
                converged = True
                print(end - start) ###########################
                print(count)

            # Update values
            self.values = new_values

    def run_policy_iteration(self):
        """
        Build a value table and a policy table using policy iteration, and store inside self.values and self.policy.
        """
        converged = False
        start = time.time()
        count = 0  ##############################
        while not converged:
            count += 1  ############################
            new_values = dict()
            new_policy = dict()
            for s in self.states:
                action_values = dict()
                for a in LaserTankMap.MOVES:
                    total = 0
                    for action, p in self.stoch_action(a).items():
                        s_next, r = self.attempt_move(s, action)
                        total += p * (r + (self.game_map.gamma * self.values[s_next]))
                    action_values[a] = total
                new_values[s] = max(action_values.values())
                new_policy[s] = self.dict_argmax(action_values)

            if new_policy == self.policy:
                converged = True

            end = time.time()
            if (end - start) > (self.game_map.time_limit - 0.5):
                converged = True
                print(end - start) ###########################
                print(count)

            # Update values
            self.values = new_values
            self.policy = new_policy

    def get_offline_value(self, state):
        """
        Get the value of this state.
        :param state: a LaserTankMap instance
        :return: V(s) [a floating point number]
        """
        return self.values[state]

    def get_offline_policy(self, state):
        """
        Get the policy for this state (i.e. the action that should be performed at this state).
        :param state: a LaserTankMap instance
        :return: pi(s) [an element of LaserTankMap.MOVES]
        """
        return self.policy[state]

    def get_mcts_policy(self, state):
        """
        Choose an action to be performed using online MCTS.
        :param state: a LaserTankMap instance
        :return: pi(s) [an element of LaserTankMap.MOVES]
        """

        #
        # TODO
        # Write your Monte-Carlo Tree Search implementation here.
        #
        # Each time this method is called, you are allowed up to [state.time_limit] seconds of compute time - make sure
        # you stop searching before this time limit is reached.
        #

        return self.policy[state]








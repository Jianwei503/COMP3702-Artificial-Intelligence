import random
import time

# Directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
EXIT = -1
RESTART = -2

def get_action_name(action):
    if action == UP:
        return "U"
    if action == DOWN:
        return "D"
    if action == LEFT:
        return "L"
    if action == RIGHT:
        return "R"
    if action == EXIT:
        return "E"


OBSTACLES = [(1, 1)]
EXIT_STATE = (-1, -1)


def dict_argmax(d):
    return max(d, key=d.get)


class Grid:

    def __init__(self):
        self.x_size = 4
        self.y_size = 3
        self.p = 0.8
        self.actions = [UP, DOWN, LEFT, RIGHT]
        self.rewards = {(3, 1): -100, (3, 2): 1}
        self.discount = 0.9  # 'gamma' in lecture notes

        self.states = list((x, y) for x in range(self.x_size) for y in range(self.y_size))
        self.states.append(EXIT_STATE)
        for obstacle in OBSTACLES:
            self.states.remove(obstacle)

        # New variables added for Tutorial 11
        self.obstacles = OBSTACLES
        self.player_x = 0
        self.player_y = 0

    def attempt_move(self, s, a):
        # s: (x, y), x = s[0], y = s[1]
        # a: {UP, DOWN, LEFT, RIGHT}

        x, y = s[0], s[1]

        # Check absorbing state
        if s in self.rewards:
            return EXIT_STATE

        if s == EXIT_STATE:
            return s

        # Default: no movement
        result = s

        # Check borders
        if a == LEFT and x > 0:
            result = (x - 1, y)
        if a == RIGHT and x < self.x_size - 1:
            result = (x + 1, y)
        if a == UP and y < self.y_size - 1:
            result = (x, y + 1)
        if a == DOWN and y > 0:
            result = (x, y - 1)

        # Check obstacle cells
        if result in OBSTACLES:
            return s

        return result

    def stoch_action(self, a):
        # Stochasitc actions probability distributions
        if a == RIGHT:
            stoch_a = {RIGHT: self.p, UP: (1 - self.p) / 2, DOWN: (1 - self.p) / 2}
        if a == UP:
            stoch_a = {UP: self.p, LEFT: (1 - self.p) / 2, RIGHT: (1 - self.p) / 2}
        if a == LEFT:
            stoch_a = {LEFT: self.p, UP: (1 - self.p) / 2, DOWN: (1 - self.p) / 2}
        if a == DOWN:
            stoch_a = {DOWN: self.p, LEFT: (1 - self.p) / 2, RIGHT: (1 - self.p) / 2}
        return stoch_a

    def get_reward(self, s):
        if s == EXIT_STATE:
            return 0

        if s in self.rewards:
            return self.rewards[s]
        else:
            return 0

    """
    Write your code to answer Q2 in Tutorial 11 below
    """

    def apply_move(self, a):
        """
        Apply a player move to the map.
        a: {UP, DOWN, LEFT, RIGHT}
        """
        s = (self.player_x, self.player_y)
        if s == EXIT_STATE:
            new_s = self.random_restart()
        else:
            # simulate action with random effect
            threshold = random.random()
            cumulative_p = .0
            for stoch_a, p in self.stoch_action(a).items():
                cumulative_p += p
                if threshold < cumulative_p:
                    a = stoch_a
                    break
            new_s = self.attempt_move(s, a)
            # print()
            # print(new_s)
            (self.player_x, self.player_y) = new_s
        return self.get_reward((self.player_x, self.player_y))

    def random_restart(self):
        """
        Restart the agent in a random map location, avoidng obstacles
        """
        conflict = True
        while conflict:
            self.player_x = random.randint(0, self.x_size - 1)
            self.player_y = random.randint(0, self.y_size - 1)
            conflict = False
            if (self.player_x, self.player_y) in OBSTACLES:
                conflict = True


class Q_Learning:
    def __init__(self, grid):
        self.grid = Grid()
        self.learning_rate = 0.05  # 'alpha' in lecture notes
        self.exploit_prob = 0.8  # 'epsilon' in epsilon-greedy
        self.q_values = {state: {} for state in self.grid.states}

    def chooose_action(self):
        """
        Write a method to choose an action here
        Incorporate your agent's exploration strategy in this method
        """
        s = (self.grid.player_x, self.grid.player_y)
        if s == EXIT_STATE:
            return EXIT

        q_s = self.q_values[s]
        if len(q_s) == 0 or random.random() > self.exploit_prob:
            a = random.choice(self.grid.actions)
        else:
            a = dict_argmax(q_s)
        # print(a)
        return a

    def next_iteration(self):
        """
        Write a method to update your agent's q_values here
        Include steps to generate new state-action q_values as you go
        """
        s = (self.grid.player_x, self.grid.player_y)
        a = self.chooose_action()
        r = self.grid.apply_move(a)
        next_s = (self.grid.player_x, self.grid.player_y)

        q_s = self.q_values[s]
        if a in q_s:
            old_q = q_s[a]
        else:
            old_q = .0

        if s != EXIT_STATE:
            next_s_q = {}
            for action in self.grid.actions:
                # print(action)
                next_s_q[action] = .0
                if action in self.q_values[next_s]:
                    next_s_q[action] = self.q_values[next_s][action]
    
            best_next_q = next_s_q[dict_argmax(next_s_q)]
    
            # update q_values(s,a,r,old_q,best_next_q)
            td = r + (self.grid.discount * best_next_q) - old_q
            self.q_values[s][a] = old_q + (self.learning_rate * td)
        else:
            self.q_values[s][RESTART] = 0.0

    def print_q_values(self):
        print('Q-values:')
        for q_val in self.q_values.items():
            print(q_val)


def run_q_learning(max_iter=1000000, time_limit=10):
    grid = Grid
    ql = Q_Learning(grid)

    start = time.time()
    print("Q_learning")
    print()

    i = 0
    while i < max_iter and (time.time() - start) < time_limit:
        i = i + 1
        ql.next_iteration()
        if i % round(max_iter/10) == 0:
            print("Q-values at iteration", i)
            print(ql.print_q_values())
            print()

    end = time.time()
    print("Time to copmlete", i + 1, "Q-learning iterations")
    print(end - start)
    print()

    policy = {}
    for state in ql.grid.states:
        policy[state] = dict_argmax(ql.q_values[state])
    print("Final policy")
    print(policy)
    

def test_QL():
    grid = Grid
    ql = Q_Learning(grid)
    
    # check initiaisation
    print('States:')
    print(ql.grid.states)
    print()
    print('Initial Q-values:')
    ql.print_q_values()
    print()

    # moves as expected
    ql.grid.player_x = 0
    ql.grid.player_y = 0
    print('Player starts at (', ql.grid.player_x, ql.grid.player_y, ')')
    action = UP
    print('Player attemps to move', action)
    ql.grid.apply_move(action)
    print('Player at (', ql.grid.player_x, ql.grid.player_y,')')
    action = RIGHT
    print('Player attemps to move', action)
    ql.grid.apply_move(action)
    print('Player at (', ql.grid.player_x, ql.grid.player_y,')')
    print()
    ql.print_q_values()
    print()
    
    # propagtes rewards correctly
    x,y = 1,2
    print('Player starts at (',x,y,')')    
    iters= 10
    print('Player attemps to move anywhere', iters, 'times')
    kk = 2
    for i in range(10):
        ql.grid.player_x = x
        ql.grid.player_y = y
        for k in range(kk):
            ql.next_iteration()
    ql.print_q_values()
    print()
    
    # exits correctly
    ql.grid.player_x = 3
    ql.grid.player_y = 2
    print('Player starts at (', ql.grid.player_x, ql.grid.player_y, ')')
    print('Player attemps to move anywhere')
    # ql.grid.apply_move(UP)
    ql.next_iteration()
    print('Player at (', ql.grid.player_x, ql.grid.player_y ,')')
    ql.print_q_values()
    print()
    
    # ... and restarts without propagating values back through the EXIT_STATE
    print('Player at (', ql.grid.player_x, ql.grid.player_y ,')')
    ql.next_iteration()
    print('Random restart: Player at (', ql.grid.player_x, ql.grid.player_y ,')')
    ql.print_q_values()
    
    
class ValueIteration:
    """
    Value iteration, for benchmarking RL algorithm solutions
    """

    def __init__(self, grid):
        self.grid = Grid()
        self.values = {state: 0 for state in self.grid.states}

    def next_iteration(self):
        new_values = dict()
        for s in self.grid.states:
            # Maximum value
            action_values = list()
            for a in self.grid.actions:
                total = 0
                for stoch_action, p in self.grid.stoch_action(a).items():
                    # Apply action
                    s_next = self.grid.attempt_move(s, stoch_action)
                    total += p * (self.grid.get_reward(s) + (self.grid.discount * self.values[s_next]))
                action_values.append(total)
            # Update state value with maximum
            new_values[s] = max(action_values)

        self.values = new_values

    def print_values(self):
        for state, value in self.values.items():
            print(state, value)


def run_value_iteration(max_iter=100):
    grid = Grid
    vi = ValueIteration(grid)

    start = time.time()
    print("Value iteration")
    print("Initial values:")
    vi.print_values()
    print()

    for i in range(max_iter):
        vi.next_iteration()
        if i % 10 == 9:
            print("Values after iteration", i + 1)
            vi.print_values()
            print()

    end = time.time()
    print("Time to copmlete", max_iter, "VI iterations")
    print(end - start)
    print()


if __name__ == "__main__":
    # test_QL()
    # run_value_iteration()
    run_q_learning()

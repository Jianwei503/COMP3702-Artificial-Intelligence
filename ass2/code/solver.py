import sys
import random
import copy

from problem_spec import ProblemSpec
from robot_config import *
from tester import *
from angle import Angle

# the total number of samples for each workspace
NUM_SAMPLES = 100
# maximum connection range of nodes
CONNECTION_RANGE = 0.25

# max primitive step size
PRIMITIVE_STEP = 1e-3

"""
Template file for you to implement your solution to Assignment 2. Contains a class you can use to represent graph nodes,
and a method for finding a path in a graph made up of GraphNode objects.

COMP3702 2020 Assignment 2 Support Code
"""


class GraphNode:
    """
    Class representing a node in the state graph. You should create an instance of this class each time you generate
    a sample.
    """

    def __init__(self, spec, config):
        """
        Create a new graph node object for the given config.

        Neighbors should be added by appending to self.neighbors after creating each new GraphNode.

        :param spec: ProblemSpec object
        :param config: the RobotConfig object to be stored in this node
        """
        self.spec = spec
        self.config = config
        self.neighbors = set()

    def __eq__(self, other):
        return test_config_equality(self.config, other.config, self.spec)

    def __ne__(self, other):
        return not test_config_equality(self.config, other.config, self.spec)

    def __hash__(self):
        return hash(tuple(self.config.points))

    def get_successors(self):
        return self.neighbors

    @staticmethod
    def add_connection(n1, n2):
        """
        Creates a neighbor connection between the 2 given GraphNode objects.

        :param n1: a GraphNode object
        :param n2: a GraphNode object
        """
        n1.neighbors.add(n2)
        n2.neighbors.add(n1)

    @staticmethod
    def delete_connection(n1, n2):
        """
        Deletes a neighbor connection between the 2 given GraphNode objects.
        @param n1: a GraphNode object
        @param n2: a GraphNode object
        """
        n1.neighbors.discard(n2)
        n2.neighbors.discard(n1)

    @staticmethod
    def interpolate_all(configs):
        """
        Takes a sequence of robot configurations, interpolates for each two adjacent robot
        configurations by calling interpolate()
        @param configs: a sequence of robot configurations
        @return: a list of robot configurations
        """
        path = [configs[0]]
        for i in range(len(configs) - 1):
            path.extend(GraphNode.interpolate(configs[i], configs[i + 1]))
            path.append(configs[i + 1])
        return path

    @staticmethod
    def interpolate(c1, c2):
        """
         Takes 2 robot configurations, and outputs a list of robot configurations where
         every 2 consecutive configs are <= 1 primitive step apart.
        @param c1: a robot configuration
        @param c2: a robot configuration
        @return: a list of robot configurations
        """
        count = len(c1.lengths)
        length_diffs = []
        angle_diffs = []
        length_strides = []
        angle_strides = []
        fill_times = 0
        configs = []
        lengths = c1.lengths[:]

        if c1.ee1_grappled:
            x, y = c1.get_ee1()
            c1_angles = [i.in_radians() for i in c1.ee1_angles]
            c2_angles = [i.in_radians() for i in c2.ee1_angles]
            for i in range(count):
                length_diffs.append(c2.lengths[i] - c1.lengths[i])
                angle_diffs.append(c2_angles[i] - c1_angles[i])
                times1 = math.ceil(abs(length_diffs[i]) / PRIMITIVE_STEP)
                times2 = math.ceil(abs(angle_diffs[i]) / PRIMITIVE_STEP)
                max_times = times1 if times1 > times2 else times2
                if max_times > fill_times:
                    fill_times = max_times
            for j in range(count):
                length_strides.append(length_diffs[j] / fill_times)
                angle_strides.append(angle_diffs[j] / fill_times)
            for m in range(fill_times - 1):
                for n in range(count):
                    lengths[n] += length_strides[n]
                    c1_angles[n] += angle_strides[n]
                angles = [Angle(radians=i) for i in c1_angles]
                config = make_robot_config_from_ee1(x, y, angles, lengths, ee1_grappled=True)
                configs.append(config)
        else:
            x, y = c1.get_ee2()
            c1_angles = [i.in_radians() for i in c1.ee2_angles]
            c2_angles = [i.in_radians() for i in c2.ee2_angles]
            for i in range(count):
                length_diffs.append(c2.lengths[i] - c1.lengths[i])
                angle_diffs.append(c2_angles[i] - c1_angles[i])
                times1 = math.ceil(abs(length_diffs[i]) / PRIMITIVE_STEP)
                times2 = math.ceil(abs(angle_diffs[i]) / PRIMITIVE_STEP)
                max_times = times1 if times1 > times2 else times2
                if max_times > fill_times:
                    fill_times = max_times
            for j in range(count):
                length_strides.append(length_diffs[j] / fill_times)
                angle_strides.append(angle_diffs[j] / fill_times)
            for m in range(fill_times - 1):
                for n in range(count):
                    lengths[n] += length_strides[n]
                    c1_angles[n] += angle_strides[n]
                angles = [Angle(radians=i) for i in c1_angles]
                config = make_robot_config_from_ee2(x, y, angles, lengths, ee2_grappled=True)
                configs.append(config)

        return configs


def find_graph_path(spec, init_node):
    """
    This method performs a breadth first search of the state graph and return a list of configs which form a path
    through the state graph between the initial and the goal. Note that this path will not satisfy the primitive step
    requirement - you will need to interpolate between the configs in the returned list.

    You may use this method in your solver if you wish, or can implement your own graph search algorithm to improve
    performance.

    :param spec: ProblemSpec object
    :param init_node: GraphNode object for the initial configuration
    :return: List of configs forming a path through the graph from initial to goal
    """
    # search the graph
    init_container = [init_node]

    # here, each key is a graph node, each value is the list of configs visited on the path to the graph node
    init_visited = {init_node: [init_node.config]}

    while len(init_container) > 0:
        current = init_container.pop(0)

        if test_config_equality(current.config, spec.goal, spec):
            # found path to goal
            return init_visited[current]

        successors = current.get_successors()
        for suc in successors:
            if suc not in init_visited:
                init_container.append(suc)
                init_visited[suc] = init_visited[current] + [suc.config]

    return None

def generate_sample(spec):
    """
     Generates a collision free random instance of RobotConfig as a sample
    @param spec: an instance of Class representing a planning problem
    @return: the collision free instance of RobotConfig
    """
    lengths = []
    angles = []
    config = None
    generated = False
    # no need to check length limits(min & max) for each segment, since limits are the same
    min_len = spec.min_lengths[0]
    max_len = spec.max_lengths[0]
    if spec.initial.ee1_grappled:
        x, y = spec.initial.get_ee1()
        while not generated:
            while len(lengths) < spec.num_segments:
                lengths.append(random.uniform(min_len, max_len))
                angles.append(Angle(degrees=random.randint(-165, 165)))

            config = make_robot_config_from_ee1(x, y, angles, lengths, ee1_grappled=True)
            if test_obstacle_collision(config, spec, spec.obstacles) \
                    and test_self_collision(config, spec):
                generated = True
            else:
                lengths.clear()
                angles.clear()
    else:
        x, y = spec.initial.get_ee2()
        while not generated:
            while len(lengths) < spec.num_segments:
                lengths.append(random.uniform(min_len, max_len))
                angles.append(Angle(degrees=random.randint(-165, 165)))

            config = make_robot_config_from_ee2(x, y, angles, lengths, ee2_grappled=True)
            if test_obstacle_collision(config, spec, spec.obstacles) \
                    and test_self_collision(config, spec):
                generated = True
            else:
                lengths.clear()
                angles.clear()
    return config

def sample(spec):
    """
    Takes a certain number(NUM_SAMPLES) of samples.
    A sample is an instance of Robotconfig
    @param spec: an instance of Class representing a planning problem
    @return: a sequence of samples
    """
    samples = []
    while len(samples) < NUM_SAMPLES:
        samples.append(generate_sample(spec))
    return samples

def connect_nodes(nodes):
    """
    Connects all nodes as neighbors to a node within a certain range(CONNECTION_RANGE) of this node.
    @param nodes: a sequence of Graphnode instances
    """
    neighbors = list(nodes.values())
    for base in nodes.values():
        neighbors.remove(base)
        for neighbor in neighbors:
            distance = get_distance(base, neighbor)
            if distance < CONNECTION_RANGE:
                GraphNode.add_connection(base, neighbor)

def get_distance(node1, node2):
    """
    Calculates the average value of Manhattan distances of all points(joints of arms) between two
    Graphnode instances.
    @param node1: a Graphnode instance to be compare
    @param node2: the other Graphnode instance to be compare
    @return: average Manhattan distance
    """
    sum_distance = 0
    num_points = len(node1.config.points)

    for i in range(num_points):
        sum_distance += abs(node1.config.points[i][0] - node2.config.points[i][0]) \
                        + abs(node1.config.points[i][1] - node2.config.points[i][1])
    return sum_distance / num_points

def test_collision(config1, config2, spec):
    """
    Tests whether collisions will happen or not along tha path between config1 and config2.
    This method needs to interpolate the space between config1 and config2
    @param config1: an instance of Robotconfig, representing the posture of arm
    @param config2: the other instance of Robotconfig, representing the posture of arm
    @param spec: an instance of Class representing a planning problem
    @return: true for collision, false otherwise
    """
    configs = GraphNode.interpolate(config1, config2)
    for c in configs:
        if not test_obstacle_collision(c, spec, spec.obstacles): # test_self_collision
            return True
    return False

def find_workspace_path(spec):
    """
    Performs a search of the state graph by calling find_graph_path() and return a list of configs
    which form a path through the state graph between the initial and the goal.
    This method only works for one partition of workspace at once.
    @param spec: an instance of Class representing a planning problem
    @return: a path represented by a sequence of configs
    """
    configs = sample(spec)
    nodes = dict()
    # converts sampling configs to sampling graph nodes
    init_node = GraphNode(spec, spec.initial)
    goal_node = GraphNode(spec, spec.goal)
    nodes[init_node] = init_node
    nodes[goal_node] = goal_node
    for config in configs:
        node = GraphNode(spec, config)
        nodes[node] = node

    connect_nodes(nodes)

    found_path = False
    while not found_path:
        path = find_graph_path(spec, init_node)
        if path is None:
            break
        else:
            collided = False
            for i in range(len(path) - 1):
                if test_collision(path[i], path[i + 1], spec):
                    neighbor1 = nodes[GraphNode(spec, path[i])]
                    neighbor2 = nodes[GraphNode(spec, path[i + 1])]
                    GraphNode.delete_connection(neighbor1, neighbor2)
                    collided = True
                    break
            if not collided:
                found_path = True
    return path

def generate_bridge_config(init_x, init_y, end_x, end_y,
                           spec, ee1_grappled=False, ee2_grappled=False):
    """
    Generates a bridge config between two grapple points using given params
    @param init_x: horizontal coordinate of starting point for bridge config
    @param init_y: vertical coordinate of starting point for bridge config
    @param end_x: horizontal coordinate of ending point for bridge config
    @param end_y: vertical coordinate of ending point for bridge config
    @param spec: an instance of Class representing a planning problem
    @param ee1_grappled: whether ee1 is grappled or not
    @param ee2_grappled: whether ee2 is grappled or not
    @return: an instance of Robotconfig
    """
    lengths = []
    angles = []
    min_len = spec.min_lengths[0]
    max_len = spec.max_lengths[0]
    while True:
        while len(lengths) < spec.num_segments - 1:
            lengths.append(random.uniform(min_len, max_len))
            angles.append(Angle(degrees=random.randint(-165, 165)))
        if ee1_grappled:
            config = make_robot_config_from_ee1(init_x, init_y, angles, lengths, ee1_grappled=True)
            tail_len, tail_angle = get_tail_length_angle(config.points[-2], config.points[-1],
                                                         (end_x, end_y))
            if min_len <= tail_len <= max_len and -165 <= tail_angle <= 165:
                lengths.append(tail_len)
                angles.append(Angle(degrees=tail_angle))
                config = make_robot_config_from_ee1(init_x, init_y, angles, lengths,
                                                    ee1_grappled=True)
                if test_obstacle_collision(config, spec, spec.obstacles) \
                        and test_self_collision(config, spec):
                    return config
            lengths.clear()
            angles.clear()
        else:
            config = make_robot_config_from_ee2(init_x, init_y, angles, lengths, ee2_grappled=True)
            tail_len, tail_angle = get_tail_length_angle(config.points[1], config.points[0],
                                                         (end_x, end_y))
            if min_len <= tail_len <= max_len and -165 <= tail_angle <= 165:
                lengths.append(tail_len)
                angles.append(Angle(degrees=tail_angle))
                config = make_robot_config_from_ee2(init_x, init_y, angles, lengths,
                                                    ee2_grappled=True)
                if test_obstacle_collision(config, spec, spec.obstacles) \
                        and test_self_collision(config, spec):
                    return config
            lengths.clear()
            angles.clear()

def divide_workspace(spec):
    """
    Divides the workspace into partitions, number of partitions equals to number of grapple points.
    Uses bridge configs to connect up two adjacent partitions
    @param spec: an instance of Class representing a planning problem
    @return: a sequence of bridge configs
    """
    configs = []
    ee1_grappled = True
    configs.append(spec.initial)

    for i in range(spec.num_grapple_points - 1):
        init_x, init_y = spec.grapple_points[i]
        end_x, end_y = spec.grapple_points[i + 1]
        bridge = generate_bridge_config(init_x, init_y, end_x, end_y, spec, ee1_grappled)
        if ee1_grappled:
            angles = bridge.ee2_angles
            lengths = bridge.lengths
            reversal = make_robot_config_from_ee2(end_x, end_y, angles, lengths, ee2_grappled=True)
        else:
            angles = bridge.ee1_angles
            lengths = bridge.lengths
            reversal = make_robot_config_from_ee1(end_x, end_y, angles, lengths, ee1_grappled=True)
        configs.append(bridge)
        configs.append(reversal)
        ee1_grappled = not ee1_grappled
    configs.append(spec.goal)

    return configs

def get_tail_length_angle(point_a, point_b, point_c):
    """
    Calculates the length and angle for the last segment of arm.
    In order to generate a bridge config between two grapple points
    @param point_a: the 3rd last joint(point) of arm, counts from the outside
    @param point_b: the 2nd last joint(point) of arm
    @param point_c: the end effector of arm
    @return: length and angle for the last segment of arm
    """
    edge_a = math.hypot(point_c[0] - point_b[0], point_c[1] - point_b[1])
    edge_b = math.hypot(point_c[0] - point_a[0], point_c[1] - point_a[1])
    edge_c = math.hypot(point_b[0] - point_a[0], point_b[1] - point_a[1])

    cos_b = (edge_a**2 + edge_c**2 - edge_b**2) / (2 * edge_a * edge_c)
    angle_b = Angle.acos(cos_b).in_degrees()
    last_angle = 180 - angle_b

    orientation = triangle_orientation(point_a, point_b, point_c)
    if orientation == 0:
        return edge_a, 0
    elif orientation > 0:
        return edge_a, last_angle
    else:
        return edge_a, last_angle * (-1)

def main(arglist):
    input_file = arglist[0]
    output_file = arglist[1]

    spec = ProblemSpec(input_file)

    init_node = GraphNode(spec, spec.initial)
    goal_node = GraphNode(spec, spec.goal)

    steps = []

    if spec.num_grapple_points == 1:
        while True:
            path = find_workspace_path(spec)
            if path:
                steps = GraphNode.interpolate_all(path)
                break
    else:
        partitions = divide_workspace(spec)
        for i in range(0, len(partitions) - 1, 2):
            init_config = partitions[i]
            goal_config = partitions[i + 1]
            spec.initial = init_config
            spec.goal = goal_config
            path = find_workspace_path(spec)
            if path:
                steps.extend(GraphNode.interpolate_all(path))

    if len(arglist) > 1:
        write_robot_config_list_to_file(output_file, steps)

if __name__ == '__main__':
    main(sys.argv[1:])

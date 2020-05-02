from random import randint
from enum import Enum
import json
from bisect import *

# Should create an undo move feature. Need to keep track of move history.


class Quadrant(Enum):
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4


class Color(Enum):
    Blue = 1
    Red = 2
    Green = 3
    Yellow = 4
    Silver = 5
    All = 6


class Shape(Enum):
    Saturn = 1
    Star = 2
    Gear = 3
    Moon = 4
    Spiral = 5


class Direction(Enum):
    Up = 1
    Right = 2
    Down = 3
    Left = 4


class Destination:
    def __init__(self, x_coord, y_coord, color, shape):
        # self.x_coord = x_coord
        # self.y_coord = y_coord
        self.coords = x_coord, y_coord
        self.color = color
        self.shape = shape

    def get_dict(self):
        data = {}
        # data['x_coord'] = self.x_coord
        # data['y_coord'] = self.y_coord
        data['coords'] = self.coords
        data['color'] = self.color.name
        data['shape'] = self.shape.name
        return data

    def __repr__(self):
        return '{' + \
                    '"coords":' + str(self.coords) + ',' + \
                    '"color":' + '"' + str(self.color.name) + '"' + ',' + \
                    '"shape":' + '"' + str(self.shape.name) + '"' + \
               '}'

    def rotate(self, quadrant):
        if quadrant == Quadrant.Q2:
            return self.__rotate_to_q2()
        elif quadrant == Quadrant.Q3:
            return self.__rotate_to_q3()
        elif quadrant == Quadrant.Q4:
            return self.__rotate_to_q4()

    def __rotate_to_q2(self):
        x_coord = self.coords[1]
        y_coord = 15 - self.coords[0]
        return Destination(x_coord, y_coord, self.color, self.shape)

    def __rotate_to_q3(self):
        x_coord = 15 - self.coords[0]
        y_coord = 15 - self.coords[1]
        return Destination(x_coord, y_coord, self.color, self.shape)

    def __rotate_to_q4(self):
        x_coord = 15 - self.coords[1]
        y_coord = self.coords[0]
        return Destination(x_coord, y_coord, self.color, self.shape)


class Robot:
    def __init__(self, x_coord, y_coord, color: Color):
        # self.init_x_coord = x_coord
        # self.init_y_coord = y_coord
        # self.current_coords[0] = x_coord
        # self.current_coords[1] = y_coord
        self.init_coords = x_coord, y_coord
        self.current_coords = x_coord, y_coord
        self.color = color

    def __repr__(self):
        return "color: " + self.color.name + ", x: " + str(self.current_coords[0]) + ", y: " + str(self.current_coords[1])

    def update_current(self, new_x, new_y):
        # self.current_coords[0] = new_x
        # self.current_coords[1] = new_y
        self.current_coords = new_x, new_y

    def update_init(self):
        self.init_coords = self.current_coords

    def reset_current(self):
        self.current_coords = self.init_coords

    def get_data(self):
        data = {}
        data["current_coords"] = self.current_coords
        data["color"] = self.color.name.lower()
        return data


class QuarterBoardSide:
    """1 side of a quarter board"""

    def __init__(self, name: str, x_walls: dict, y_walls: dict, destinations: list, quadrant=Quadrant.Q1):
        self.quadrant = quadrant
        self.name = name
        self.destinations = destinations
        self.x_walls = x_walls
        self.y_walls = y_walls

    def rotate(self, quadrant):
        if quadrant == Quadrant.Q2:
            return self.__rotate_to_q2()
        elif quadrant == Quadrant.Q3:
            return self.__rotate_to_q3()
        elif quadrant == Quadrant.Q4:
            return self.__rotate_to_q4()

    def __rotate_to_q2(self):
        name = self.name
        quadrant = Quadrant.Q2
        x_walls = self.__flip_2(self.y_walls)
        y_walls = self.__flip_1(self.x_walls)
        destinations = [destination.rotate(Quadrant.Q2) for destination in self.destinations]
        return QuarterBoardSide(name, x_walls, y_walls, destinations, quadrant)

    def __rotate_to_q3(self):
        name = self.name
        quadrant = Quadrant.Q3
        x_walls = self.__flip_3(self.x_walls)
        y_walls = self.__flip_3(self.y_walls)
        destinations = [destination.rotate(Quadrant.Q3) for destination in self.destinations]
        return QuarterBoardSide(name, x_walls, y_walls, destinations, quadrant)

    def __rotate_to_q4(self):
        name = self.name
        quadrant = Quadrant.Q4
        x_walls = self.__flip_1(self.y_walls)
        y_walls = self.__flip_2(self.x_walls)
        destinations = [destination.rotate(Quadrant.Q4) for destination in self.destinations]
        return QuarterBoardSide(name, x_walls, y_walls, destinations, quadrant)

    @staticmethod
    def __flip_1(walls):
        new_walls = {}
        for key, value in walls.items():
            for x in range(len(value)):
                new_key = 15 - key
                new_value = value[x]
                try:
                    if new_value not in new_walls[new_key]:
                        new_walls[new_key].append(new_value)
                except:
                    new_walls[new_key] = [new_value]
        return new_walls

    @staticmethod
    def __flip_2(walls):
        new_walls = {}
        for key, value in walls.items():
            for x in range(len(value)):
                new_key = key
                new_value = 14 - value[x]
                try:
                    if new_value not in new_walls[new_key]:
                        new_walls[new_key].append(new_value)
                except:
                    new_walls[new_key] = [new_value]
        return new_walls

    @staticmethod
    def __flip_3(walls):
        new_walls = {}
        for key, value in walls.items():
            for x in range(len(value)):
                new_key = 15 - key
                new_value = 14 - value[x]
                try:
                    if new_value not in new_walls[new_key]:
                        new_walls[new_key].append(new_value)
                except:
                    new_walls[new_key] = [new_value]
        return new_walls


class QuarterBoard:
    """a quarter board with 2 sides"""

    def __init__(self, name: str, side_a: QuarterBoardSide, side_b: QuarterBoardSide):
        self.name = name
        self.side_a = side_a
        self.side_b = side_b

    def random_side(self):
        x = randint(0, 1)
        if x == 0:
            print(self.side_a.name)
            return self.side_a
        else:
            print(self.side_b.name)
            return self.side_b


class Board:
    def __init__(self, q1: QuarterBoardSide, q2: QuarterBoardSide, q3: QuarterBoardSide, q4: QuarterBoardSide):
        self.q1 = q1
        self.q2 = q2.rotate(Quadrant.Q2)
        self.q3 = q3.rotate(Quadrant.Q3)
        self.q4 = q4.rotate(Quadrant.Q4)
        self.x_walls = self.__merge_walls(self.q1.x_walls, self.q2.x_walls, self.q3.x_walls, self.q4.x_walls)
        self.y_walls = self.__merge_walls(self.q1.y_walls, self.q2.y_walls, self.q3.y_walls, self.q4.y_walls)
        self.destinations = self.q1.destinations + self.q2.destinations + self.q3.destinations + self.q4.destinations
        # Should probably make robots a dictionary where color is the key
        # Currently using single robot for testing
        # self.robots = {Color.Red: Robot(0, 0, Color.Red)}
        self.robots = self.place_all_robots()

    def get_json(self):
        data = {}
        data['x_walls'] = self.x_walls
        data['y_walls'] = self.y_walls
        data['destinations'] = [destination.get_dict() for destination in self.destinations]
        return json.dumps(data)

    def __repr__(self):
        return '{' + \
                    '"x_walls":' + str(self.x_walls) + ',' + \
                    '"y_walls":' + str(self.y_walls) + ',' + \
                    '"destinations":' + str(self.destinations) + ',' + \
                    '"robots":' + str(self.robots) + \
               '}'

    def move_robot(self, color: Color, direction: Direction):
        # robot = self.robots[color]
        # start = robot.current_coords[0], robot.current_coords[1]
        if direction == Direction.Up:
            self.__move_robot_up(color)
        elif direction == Direction.Right:
            self.__move_robot_right(color)
        elif direction == Direction.Down:
            self.__move_robot_down(color)
        else:
            self.__move_robot_left(color)
        # current = robot.current_coords[0], robot.current_coords[1]
        # print(f"{color.name} robot has been moved from {start} to {current}.")

    # def get_all_robot_coords(self):
    #     coords = []
    #     for robot in self.robots:


    def place_all_robots(self):
        coords = []
        while len(coords) < 5:
            coord = randint(0, 15), randint(0, 15)
            if coord != (7,7) and coord != (7,8) and coord != (8,7) and coord != (8,8) and coord not in coords:
                coords.append(coord)

        robots = {}
        print("coords", coords)
        for i in range(5):
            robots[Color(i+1)] = Robot(coords[i][0], coords[i][1], Color(i+1))

        return robots

    # implement bumping into other robots.
    def __get_other_robots_plus_x_walls(self, color: Color):
        robots = []
        for i in range(1, 6):
            if color != Color(i) and self.robots[color].current_coords[0] == self.robots[Color(i)].current_coords[0]:
                robots.append(self.robots[Color(i)].current_coords[1] - 1)
                robots.append(self.robots[Color(i)].current_coords[1])
        
        x_walls = []
        if self.x_walls.get(self.robots[color].current_coords[0]) != None:
            x_walls = self.x_walls.get(self.robots[color].current_coords[0])

        return sorted(robots + x_walls)

    def __get_other_robots_plus_y_walls(self, color: Color):
        robots = []
        for i in range(1, 6):
            if color != Color(i) and self.robots[color].current_coords[1] == self.robots[Color(i)].current_coords[1]:
                robots.append(self.robots[Color(i)].current_coords[0] - 1)
                robots.append(self.robots[Color(i)].current_coords[0])

        y_walls = []
        if self.y_walls.get(self.robots[color].current_coords[1]) != None:
            y_walls = self.y_walls.get(self.robots[color].current_coords[1])

        return sorted(robots + y_walls)


    def __move_robot_up(self, color: Color):
        x_walls = self.__get_other_robots_plus_x_walls(color)
        try:
            end_y = self.__find_ge(x_walls, self.robots[color].current_coords[1])
        except KeyError:
            end_y = 15
        self.robots[color].update_current(self.robots[color].current_coords[0], end_y)

    def __move_robot_down(self, color: Color):
        x_walls = self.__get_other_robots_plus_x_walls(color)
        try:
            end_y = self.__find_lt(x_walls, self.robots[color].current_coords[1])
        except KeyError:
            end_y = 0
        self.robots[color].update_current(self.robots[color].current_coords[0], end_y)

    def __move_robot_right(self, color: Color):
        y_walls = self.__get_other_robots_plus_y_walls(color)
        try:
            end_x = self.__find_ge(y_walls, self.robots[color].current_coords[0])
        except KeyError:
            end_x = 15
        self.robots[color].update_current(end_x, self.robots[color].current_coords[1])

    def __move_robot_left(self, color: Color):
        y_walls = self.__get_other_robots_plus_y_walls(color)
        try:
            end_x = self.__find_lt(y_walls, self.robots[color].current_coords[0])
        except KeyError:
            end_x = 0
        self.robots[color].update_current(end_x, self.robots[color].current_coords[1])


    @staticmethod
    def __find_ge(a, x):
        # Find leftmost item greater than or equal to x
        # used for moving up or right
        i = bisect_left(a, x)
        if i != len(a):
            return a[i]
        else:
            return 15

    @staticmethod
    def __find_lt(a, x):
        # Find rightmost value less than x + 1
        # used for moving down or left
        i = bisect_left(a, x)
        if i:
            return a[i-1] + 1
        else:
            return 0

    @staticmethod
    def __find_upper_cell(a, x):
        'Find leftmost item greater than or equal to x'
        i = bisect_left(a, x)
        if i != len(a):
            return a[i]
        else:
            return 15

    def __merge_walls(self, *walls):
        all_keys = self.__get_keys(*walls)
        new_walls = {}
        for key in all_keys:
            values = [self.__get_value(wall,key) for wall in walls if self.__get_value(wall,key) is not None]
            all_values = []
            for value in values:
                all_values += value
            new_walls[key] = list(set(all_values))
            new_walls[key].sort()
        return new_walls

    @staticmethod
    def __get_keys(*walls):
        all_keys = []
        for wall in walls:
            all_keys += list(wall.keys())
        return list(set(all_keys))

    @staticmethod
    def __get_value(wall, key):
        try:
            return wall[key]
        except KeyError:
            return


"""x_walls are the walls on the top side of a cells along the x axis (horizontal walls)"""
"""y_walls are the walls on the right side of the cells along the y axis (vertical walls)"""

qboard1a_x_walls = {0: [4], 1: [6], 2: [0], 5: [6], 6: [2], 7: [6]}
qboard1a_y_walls = {0: [5], 1: [1], 3: [6], 6: [1, 4], 7: [6]}
qboard_1a_destinations = [Destination(1, 6, Color.Yellow, Shape.Star),
                          Destination(2, 1, Color.Green, Shape.Gear),
                          Destination(5, 6, Color.Blue, Shape.Saturn),
                          Destination(6, 3, Color.Red, Shape.Moon)]

qboard1b_x_walls = {0: [1], 1: [3], 2: [1], 3: [6], 6: [2], 7: [6]}
qboard1b_y_walls = {0: [5], 1: [1], 3: [6], 4: [0], 6: [3], 7: [6]}
qboard_1b_destinations = [Destination(3, 6, Color.Yellow, Shape.Star),
                          Destination(2, 1, Color.Green, Shape.Gear),
                          Destination(6, 3, Color.Blue, Shape.Saturn),
                          Destination(1, 4, Color.Red, Shape.Moon)]

qboard2a_x_walls = {0: [3], 1: [0], 2: [6], 4: [2], 5: [6], 7: [6]}
qboard2a_y_walls = {0: [5], 1: [1], 2: [4], 6: [1], 7: [4, 6]}
qboard_2a_destinations = [Destination(5, 7, Color.Yellow, Shape.Saturn),
                          Destination(2, 6, Color.Green, Shape.Moon),
                          Destination(4, 2, Color.Blue, Shape.Star),
                          Destination(1, 1, Color.Red, Shape.Gear)]

qboard2b_x_walls = {0: [3], 2: [5], 4: [2], 5: [6], 6: [0], 7: [6]}
qboard2b_y_walls = {0: [4], 1: [5], 2: [3], 5: [2], 7: [5, 6]}
qboard_2b_destinations = [Destination(6, 1, Color.Yellow, Shape.Saturn),
                          Destination(4, 2, Color.Green, Shape.Moon),
                          Destination(2, 5, Color.Blue, Shape.Star),
                          Destination(5, 7, Color.Red, Shape.Gear)]

qboard3a_x_walls = {0: [4], 1: [1], 3: [5], 5: [4], 6: [1], 7: [6]}
qboard3a_y_walls = {0: [4], 1: [6], 2: [0], 4: [4], 6: [3], 7: [6]}
qboard_3a_destinations = [Destination(1, 2, Color.Yellow, Shape.Moon),
                          Destination(6, 1, Color.Green, Shape.Star),
                          Destination(3, 6, Color.Blue, Shape.Gear),
                          Destination(5, 4, Color.Red, Shape.Saturn)]

qboard3b_x_walls = {0: [3], 1: [5], 2: [0], 4: [5], 6: [2], 7: [6]}
qboard3b_y_walls = {0: [3], 1: [2], 2: [5], 5: [1], 6: [3], 7: [6]}
qboard_3b_destinations = [Destination(4, 6, Color.Yellow, Shape.Moon),
                          Destination(1, 5, Color.Green, Shape.Star),
                          Destination(6, 2, Color.Blue, Shape.Gear),
                          Destination(2, 1, Color.Red, Shape.Saturn)]

qboard4a_x_walls = {0: [3], 1: [5], 3: [1], 4: [4], 5: [2, 7], 7: [6]}
qboard4a_y_walls = {0: [6], 1: [2], 2: [5], 5: [3], 6: [1], 7: [5, 6]}
qboard_4a_destinations = [Destination(3, 1, Color.Yellow, Shape.Gear),
                          Destination(4, 5, Color.Green, Shape.Saturn),
                          Destination(1, 6, Color.Blue, Shape.Moon),
                          Destination(5, 2, Color.Red, Shape.Star),
                          Destination(5, 7, Color.All, Shape.Spiral)]

qboard4b_x_walls = {0: [4], 1: [2], 3: [0], 4: [5], 6: [5], 7: [3, 6]}
qboard4b_y_walls = {0: [4], 1: [3], 2: [1], 3: [7], 5: [5], 6: [3], 7: [6]}
qboard_4b_destinations = [Destination(4, 6, Color.Yellow, Shape.Gear),
                          Destination(3, 1, Color.Green, Shape.Saturn),
                          Destination(6, 5, Color.Blue, Shape.Moon),
                          Destination(1, 2, Color.Red, Shape.Star),
                          Destination(7, 3, Color.All, Shape.Spiral)]

qboard_side_1a = QuarterBoardSide("1a", qboard1a_x_walls, qboard1a_y_walls, qboard_1a_destinations)
qboard_side_1b = QuarterBoardSide("1b", qboard1b_x_walls, qboard1b_y_walls, qboard_1b_destinations)
qboard_1 = QuarterBoard("board_1", qboard_side_1a, qboard_side_1b)

qboard_side_2a = QuarterBoardSide("2a", qboard2a_x_walls, qboard2a_y_walls, qboard_2a_destinations)
qboard_side_2b = QuarterBoardSide("2b", qboard2b_x_walls, qboard2b_y_walls, qboard_2b_destinations)
qboard_2 = QuarterBoard("board_2", qboard_side_2a, qboard_side_2b)

qboard_side_3a = QuarterBoardSide("3a", qboard3a_x_walls, qboard3a_y_walls, qboard_3a_destinations)
qboard_side_3b = QuarterBoardSide("3b", qboard3b_x_walls, qboard3b_y_walls, qboard_3b_destinations)
qboard_3 = QuarterBoard("board_3", qboard_side_3a, qboard_side_3b)

qboard_side_4a = QuarterBoardSide("4a", qboard4a_x_walls, qboard4a_y_walls, qboard_4a_destinations)
qboard_side_4b = QuarterBoardSide("4b", qboard4b_x_walls, qboard4b_y_walls, qboard_4b_destinations)
qboard_4 = QuarterBoard("board_4", qboard_side_4a, qboard_side_4b)

test_board = Board(qboard_side_1a, qboard_side_2a, qboard_side_3a, qboard_side_4a)
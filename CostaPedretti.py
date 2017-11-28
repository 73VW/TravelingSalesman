"""
Traveling salesman problem solver.

The following code is used to try to find a solution to the TSP.
Using City and Individual (path) class it is possible to find a solution
approaching the real result. This code is optimized to take less time
to execute not to find the absolute shortest path.
"""
import argparse
import math
import random
import sys
import time
from copy import copy

import pygame
from pygame.locals import K_RETURN, KEYDOWN, MOUSEBUTTONDOWN, QUIT

import secrets

app_desc = "Traveling salesman problem"


class City:
    """
    Object that take the name of the city and it's coordonates.

    This object is used to compute and compare distance between towns
    in order to improve path length.
    """

    def __init__(self, name, x, y):
        """Init city object."""
        self.name = name
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        """Print object in a human readle way."""
        city_name = "City <" + self.name + "> "
        coordinates = "[x = " + str(self.x) + ", y = " + str(self.y) + "]"
        return city_name + coordinates

    def __repr__(self):
        """
        Represent object.

        Commonly used when printing a list of objects.
        """
        return str(self)

    def distance_to(self, other):
        """Compute distance between self and other city."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.hypot(dx, dy)

    def __eq__(self, other):
        """Compare two cities."""
        if (self.name == other.name
                and self.x == other.x
                and self.y == other.y):
            return True
        return False


class Individual:
    """
    Class that take a possible path as value.

    This object is used to compute parameters and manipulate paths in an easier
    way.
    """

    def __init__(self, path):
        """Init Individual object."""
        # list of City objects
        self.path = path
        self.length = len(self.path)
        self.path_length = self.p_length()

    def p_length(self):
        """Compute path length according to cities order."""
        path_length = 0
        for i in range(0, len(self.path) - 1):
            path_length += self.path[i].distance_to(self.path[i + 1])
        path_length += self.path[-1].distance_to(self.path[0])
        return path_length

    def fitness(self):
        """
        Compute fitness value in order to choose who lives.

        In this case we want to keep only the shortest path
        so we have to invert the result.
        """
        return 1000 / self.path_length

    def __str__(self):
        """Print object in a human readle way."""
        length = "[Path length = " + str(self.path_length) + ", "
        fitness = "fitness = " + str(self.fitness()) + ", "
        path = "path : "
        for c in self.path:
            path += c.name + " -> "
        path += self.path[0].name + "]"
        return "Individual. " + length + fitness + path

    def __repr__(self):
        """
        Represent object.

        Commonly used when printing a list of objects.
        """
        return str(self)

    def __eq__(self, other):
        """Compare two individuals."""
        if len(self) != len(other):
            return False
        for i in range(0, len(self.path)):
            if self.path[i] != other.path[i]:
                return False
        return True

    def __lt__(self, other):
        """Lower than operator."""
        return self.fitness() < other.fitness()

    def __len__(self):
        """Return path length."""
        return self.length

    def __getitem__(self, i):
        """Return city at position i."""
        if i < len(self.path):
            return self.path[i]
        else:
            raise IndexError("max value is ", len(self.path), "current ", i)

    def __setitem__(self, i, value):
        """Set value for city at position i."""
        if i < len(self.path):
            self.path[i] = value
        else:
            raise IndexError("max value is ", len(self.path), "current ", i)

    def index(self, value):
        """Return value's position in self.path."""
        return self.path.index(value)

    def insert(self, i, value):
        """Insert value in self.path at position i."""
        self.path.append(i, value)

    def __contains__(self, city):
        """Return if city is in path."""
        return city in self.path

    def extend(self, datas):
        """Extend path."""
        self.path.extend(datas)


screen_x = 510
screen_y = 510

city_color = [255, 0, 127]  # pink
city_radius = 3

font_color = [255, 255, 255]  # white


def fillArrayWithData(fileName, cities):
    """Fill city list with datas from [filename]."""
    with open(fileName) as f:
        for line in f:
            dataList = line.split()
            city = City(dataList[0], dataList[1], dataList[2])
            cities.append(city)


def draw(screen, font, positions):
    """Draw cities on window."""
    screen.fill(0)
    for pos in positions:
        pygame.draw.circle(screen, city_color, (pos.x, pos.y), city_radius)
    text = font.render("Nombre: %i" % len(positions), True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


def init_game():
    """Init pygame interface."""
    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption(app_desc)
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)
    return (window, screen, font)


def collect_cities(screen, font, cities):
    """Collect cities from user input."""
    collecting = True
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN and event.key == K_RETURN:
            collecting = False
        elif event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            cities.append(City("Bab", x, y))
            draw(screen, font, cities)
    return collecting


def draw_line(screen, font, cities, text):
    """Draw lines from cities list."""
    screen.fill(0)
    positions = [(c.x, c.y) for c in cities]
    pygame.draw.lines(screen, city_color, True, positions)
    text = font.render(text, True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


def init_solutions(cities, solutions, M):
    """Init first random solutions."""
    solutions.append(Individual(cities))
    for i in range(1, M):
        create_random_individual(cities, solutions)


def create_random_individual(cities, solutions):
    """Create random individual from cities list."""
    cities = copy(cities)
    random.shuffle(cities, random.random)
    new_individu = Individual(cities)
    while(new_individu in solutions):
        random.shuffle(cities, random.random)
        new_individu = Individual(cities)

    solutions.insert(0, new_individu)


def swap_two_opt(solution, i, k):
    """Swap cities between i and k in solution."""
    path = solution.path
    new_solution = path[0:i]
    new_solution.extend(reversed(path[i:k + 1]))
    new_solution.extend(path[k + 1:])
    new_solution = Individual(new_solution)
    assert len(new_solution) == len(solution)
    return new_solution


def extended_two_opt(solution, gui, screen, font, text, maxtime, start):
    """
    Peform extended 2-opt.

    Source :
    https://github.com/rellermeyer/99tsp/blob/master/python/2opt/TSP2opt.py
    """
    best_solution = solution
    best_distance = solution.path_length
    length = len(solution)

    for i in range(length - 1):
        for j in range(i, length):
            if maxtime is 0 or time.time() - start < maxtime:
                new_route = swap_two_opt(best_solution, i, j)
                if new_route.path_length < best_distance:
                    best_distance = new_route.path_length
                    best_solution = new_route
                    if gui:
                        draw_line(screen, font, best_solution, text)
            else:
                assert len(best_solution) == length
                return best_solution
    assert len(best_solution) == length
    return best_solution


def two_opt(solution):
    """
    Peform a short random 2-opt.

    Inspiration :
    https://github.com/rellermeyer/99tsp/blob/master/python/2opt/TSP2opt.py
    """
    best_distance = solution.path_length
    length = len(solution)

    # use secrets for more anthropy
    i = secrets.randbelow(length - 1)
    j = random.randint(i, length - 1)

    new_route = swap_two_opt(solution, i, j)
    new_distance = new_route.path_length
    if new_distance < best_distance:
        solution = new_route

    assert len(solution) == length
    return solution


def multiply_using_gSC(solutions, number_of_multiplication):
    """Multiply using greedy_subtour_crossover function."""
    i = 0
    for i in range(number_of_multiplication):
        new_individual = greedy_subtour_crossover(
            solutions[i], solutions[secrets.randbelow(len(solutions))])
        solutions.append(new_individual)


def greedy_subtour_crossover(ga, gb):
    """
    Multiply individuals according to Greedy Subtour Crossover.

    Source: http://www.gcd.org/sengoku/docs/arob98.pdf
    """
    fa = True
    fb = True
    g = list()

    length = len(ga) - 1
    rand = secrets.randbelow(length)
    t = ga[rand]
    x = rand
    y = gb.index(t)
    g.insert(0, t)

    while fa is True or fb is True:
        x = x - 1
        y = (y + 1) % length
        if fa is True:
            if ga[x] not in g:
                g.append(ga[x])
            else:
                fa = False

        if fb is True:
            if gb[y] not in g:
                g.insert(0, gb[y])
            else:
                fb = False

    cities_not_in_g = [city for city in ga if city not in g]

    random.shuffle(cities_not_in_g, random.random)
    for city in cities_not_in_g:
        g.append(city)

    g = Individual(g)
    return g


def ga_solve(filename=None, gui=True, maxtime=0):
    """Solve using Genetic Algorithm."""
    start = time.time()
    cities = []
    collecting = False

    if filename is not None:
        fillArrayWithData(filename, cities)
    else:
        collecting = True
    # init pygame and draw cities
    if gui:
        window, screen, font = init_game()
        draw(screen, font, cities)
    else:
        window = screen = font = None

    # if file is not specified, collect points from user input
    while collecting:
        collecting = collect_cities(screen, font, cities)

    if gui:
        # draw the line
        draw_line(screen, font, cities, "Initial situation!")

    length = len(cities)

    # number of individuals
    M = 15

    # percentage of individuals to eliminate
    pe = 1 / 2
    # percentage of individuals to mutate using 2 opt
    po = 1 / 2

    nb_2opt = int(length / 100) if length > 100 else 2

    # solve and draw here
    # init. Generate M random individuals
    solutions = []
    init_solutions(cities, solutions, M)

    best_solution = 1000
    stagnation_len = 0
    max_stagnation = 1
    while True and (maxtime is 0 or time.time() - start < maxtime):

        # sort solutions in order to remove the worst population
        solutions = sorted(solutions, reverse=True)

        # draw the line
        if gui:
            draw_line(
                screen,
                font,
                solutions[0],
                "Actual best solution")

        if solutions[0].fitness() == best_solution:
            if stagnation_len < max_stagnation:
                stagnation_len += 1
                # if the solution stagnates, mutate the best a lot
            elif stagnation_len is max_stagnation:
                solutions[0] = extended_two_opt(
                    solutions[0],
                    gui,
                    screen,
                    font,
                    "Actual best solution", maxtime, start)
                stagnation_len += 1
            elif (maxtime is not 0 and time.time() - start < maxtime):
                stagnation_len = 0
            else:
                break
        else:
            best_solution = solutions[0].fitness()
            stagnation_len = 0

        old_len = len(solutions)

        # Natural selection
        quantity_to_eliminate = int(M * pe)
        del solutions[-quantity_to_eliminate:]

        # Multplication using greedy subtour crossover
        multiply_using_gSC(solutions, quantity_to_eliminate)

        length = len(solutions)
        assert(old_len == length)

        # Mutation by 2 opt
        for i in range(int(length * po)):
            for j in range(nb_2opt):
                solutions[i] = two_opt(solutions[i])

    """if gui:
        draw_line(screen, font, solutions[0], "Possible result!")
        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN or event.type == QUIT:
                break"""

    cities_name = list()
    for city in solutions[0].path:
        cities_name.append(city.name)
    return (solutions[0].path_length, cities_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=app_desc)
    parser.add_argument(
        "--nogui",
        help="turn off gui",
        action="store_true")
    parser.add_argument(
        "--maxtime",
        help="max execution time",
        type=int)
    parser.add_argument(
        "--filename",
        help="filename to read datas from",
        type=str)
    args = parser.parse_args()

    gui = True
    filename = None
    maxtime = 0

    if args.filename:
        filename = args.filename
    if args.maxtime:
        maxtime = args.maxtime
    if args.nogui:
        gui = False

    path_length, cities_list = ga_solve(filename, gui, maxtime)
    print("total length : ", path_length)

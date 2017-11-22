"""Traveling salesman problem."""
import argparse
import math
import random
import sys
import time
from copy import deepcopy

import pygame
from pygame.locals import K_RETURN, KEYDOWN, MOUSEBUTTONDOWN, QUIT


class City:
    """Object that take the name of the city and it's coordonates."""

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
        """Compute distance between self and other."""
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)

    def __eq__(self, other):
        """Compare two cities."""
        if (self.name == other.name
                and self.x == other.x
                and self.y == other.y):
            return True
        return False


class Individu:
    """Class that take a possible path as value."""

    def __init__(self, path):
        """Init Individu object."""
        # list of City objects
        self.path = path

    def path_length(self):
        """Compute path length according to cities order."""
        path_length = 0
        for i in range(0, len(self.path)-1):
            path_length += self.path[i].distance_to(self.path[i+1])
        path_length += self.path[-1].distance_to(self.path[0])
        return path_length

    def fitness(self):
        """
        Compute fitness value in order to choose who lives.

        In this case we want to keep only the shortest path
        so we have to invert the result.
        """
        return 1000/self.path_length()

    def __str__(self):
        """Print object in a human readle way."""
        length = "[Path length = " + str(self.path_length()) + ", "
        fitness = "fitness = " + str(self.fitness()) + ", "
        path = "path : "
        for c in self.path:
            path += c.name + " -> "
        path += self.path[0].name + "]"
        return "Individu. " + length + fitness + path

    def __repr__(self):
        """
        Represent object.

        Commonly used when printing a list of objects.
        """
        return str(self)

    def __eq__(self, other):
        """Compare two individuals."""
        for i in range(0, len(self.path)):
            if self.path[i] != other.path[i]:
                return False
        return True

    def __lt__(self, other):
        """Compare objects."""
        return self.fitness() < other.fitness()

    def __len__(self):
        """Return path length."""
        return len(self.path)

    def __getitem__(self, i):
        """Return city at i."""
        if i < len(self.path):
            return self.path[i]
        else:
            raise IndexError("max value is ", len(self.path), "current ", i)

    def __setitem__(self, i, value):
        """Set city at i."""
        if i < len(self.path):
            self.path[i] = value
        else:
            raise IndexError("max value is ", len(self.path), "current ", i)

    def index(self, value):
        """Return index of value in self.path."""
        return self.path.index(value)

    def insert(self, i, value):
        """Insert value in self.path at i."""
        self.path.append(i, value)

    def __contains__(self, city):
        """Return if city is in path."""
        return city in self.path


screen_x = 500
screen_y = 500

city_color = [255, 0, 127]  # blue
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


def draw_line(screen, font, cities):
    """Draw lines from cities list."""
    screen.fill(0)
    positions = [(c.x, c.y) for c in cities]
    pygame.draw.lines(screen, city_color, True, positions)
    text = font.render("Meilleur chemin trouvé actuellement!",
                       True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


def init_solutions(cities, solutions, M):
    """Init first random solutions."""
    solutions.append(Individu(cities))
    cities = deepcopy(cities)
    for i in range(1, M):
        random.shuffle(cities, random.random)
        new_individu = Individu(cities)
        while(new_individu in solutions):
            random.shuffle(cities, random.random)
            new_individu = Individu(cities)
        solutions.append(new_individu)
        cities = deepcopy(cities)


def mutate_using_2_opt(solutions):
    """Mutate using 2opt method."""
    for solution in solutions:
        length = len(solution)
        # if ab + cd > ac + bd -> swap b and c
        # d1 = ab + cd
        # d2 = ac + bd
        for i in range(0, length):
            i1 = (i+1) % length
            i2 = (i+2) % length
            i3 = (i+3) % length
            d1 = solution[i].distance_to(solution[i1])
            d1 += solution[i2].distance_to(solution[i3])
            d2 = solution[i].distance_to(solution[i2])
            d2 += solution[i1].distance_to(solution[i3])
            if d1 > d2:
                solution[i1], solution[i2] = solution[i2], solution[i1]


def multiply_using_gSC(solutions, number_of_multiplication):
    """Multiply using greedy_subtour_crossover function."""
    i = 0
    while i < number_of_multiplication*2:
        new_individual = greedy_subtour_crossover(solutions[i], solutions[i+1])
        solutions.append(new_individual)
        i += 2


def greedy_subtour_crossover(ga, gb):
    """Multiply individuals according to Greedy Subtour Crossover."""
    fa = True
    fb = True
    g = list()

    length = len(ga)-1
    t = ga[random.randint(0, length)]
    x = ga.index(t)
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

    for city in ga:
        if city not in g:
            g.append(city)

    g = Individu(g)
    return g


def ga_solve(filename=None, gui=True, maxtime=0):
    """Solve using Genetic Algorithm."""
    cities = []
    collecting = False

    if filename is not None:
        fillArrayWithData(filename, cities)
    else:
        collecting = True

    # init pygame and draw cities
    window, screen, font = init_game()
    draw(screen, font, cities)

    # if file is not specified, collect points from user input
    while collecting:
        collecting = collect_cities(screen, font, cities)

    # draw the line
    draw_line(screen, font, cities)

    # number of individuals
    M = len(cities) * 3
    pe = 20/100
    # solve and draw here
    # init. Generate M random individuals
    solutions = []
    init_solutions(cities, solutions, M)

    best_solution = solutions[0].fitness()
    stagnation_len = 0
    keep_finding = True
    while True:

        while keep_finding:
            with open('log.txt', 'a') as fp:
                fp.write(str(solutions[0].fitness()) + "\n")
            if solutions[0].fitness() == best_solution:
                if stagnation_len < 5:
                    with open('log.txt', 'a') as fp:
                        fp.write("Warning, stagnation!\n")
                    stagnation_len += 1
                else:
                    with open('log.txt', 'a') as fp:
                        fp.write("Stagnated for too long, exiting!\n")
                    keep_finding = False
            else:
                best_solution = solutions[0].fitness()
                stagnation_len = 0

            # sort solutions in order to remove the worst population
            solutions = sorted(solutions, reverse=True)

            # draw the line
            draw_line(screen, font, solutions[0])

            # Natural selection. Eliminate the worst pe% of the population
            quantity_to_eliminate = int(M * pe)
            if quantity_to_eliminate % 2 is not 0:
                quantity_to_eliminate += 1
            del solutions[-quantity_to_eliminate:]

            # Multplication Choose M * pe/100 pairs of individuals randomly
            # and produce result of pair multiplication

            multiply_using_gSC(solutions, quantity_to_eliminate)

            # Mutation by 2 opt
            mutate_using_2_opt(solutions)

            time.sleep(1)

        event = pygame.event.wait()
        if event.type == KEYDOWN or event.type == QUIT:
            break


if __name__ == "__main__":
    app_desc = "Traveling salesman problem"
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

    ga_solve(filename, gui, maxtime)

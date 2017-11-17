"""Traveling salesman problem."""
import argparse
import math
import random
import sys
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
        # path length
        self.length = self.length()
        # fitness
        self.fitness = self.fitness()

    def length(self):
        """Compute path length according to cities order."""
        path_length = 0
        for i in range(0, len(self.path)-1):
            dx = self.path[i].x - self.path[i+1].x
            dy = self.path[i].y - self.path[i+1].y
            path_length += math.sqrt(dx**2 + dy**2)
        return path_length

    def fitness(self):
        """
        Compute fitness value in order to choose who lives.

        In this case we want to keep only the shortest path
        so we have to invert the result.
        """
        return 1/self.length

    def __str__(self):
        """Print object in a human readle way."""
        length = "[Path length = " + str(self.length) + ", "
        fitness = "fitness = " + str(self.fitness) + ", "
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


class Population:
    """Class that take possible path as values."""

    def __init__(self, individus):
        """Init Population object."""
        self.individus = individus


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
    text = font.render("Un chemin, pas le meilleur!", True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


def init_solutions(cities, solutions, M):
    """Init first random solutions."""
    for i in range(1, M):
        random.shuffle(cities, random.random)
        new_individu = Individu(cities)
        while(new_individu in solutions):
            random.shuffle(cities, random.random)
            new_individu = Individu(cities)
        solutions.append(new_individu)
        cities = deepcopy(cities)


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

    # solve and draw here
    # init. Generate M random individuals
    M = len(cities) * 2
    solutions = []
    solutions.append(Individu(cities))
    init_solutions(deepcopy(cities), solutions, M)

    print('\n'.join(str(i) for i in solutions))

    # Natural selection. Eliminate the worst pe% of the population

    # Multplication Choose M * pe/100 pairs of individuals randomly
    # and produce result of pair multiplication

    # Mutation by 2 opt

    #

    # wait for quit
    """while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN or event.type == QUIT:
            break"""


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

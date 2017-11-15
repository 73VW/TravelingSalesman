"""Traveling salesman problem."""
import argparse
import sys

import pygame
from pygame.locals import K_RETURN, KEYDOWN, MOUSEBUTTONDOWN, QUIT


class City:
    """Object that take the name of the city and it's coordonates."""

    def __init__(self, name, x, y):
        """Init city object."""
        self.name = name
        self.x = x
        self.y = y


screen_x = 500
screen_y = 500

city_color = [10, 10, 200]  # blue
city_radius = 3

font_color = [255, 255, 255]  # white

cityList = []


def fillArrayWithData(fileName):
    """Fill city list with datas from [filename]."""
    with open(fileName) as f:
        for line in f:
            dataList = line.split()
            city = City(dataList[0], dataList[1], dataList[2])
            cityList.append(city)


def draw(positions):
    """Draw cities on window."""
    screen.fill(0)
    for pos in positions:
        pygame.draw.circle(screen, city_color, pos, city_radius)
    text = font.render("Nombre: %i" % len(positions), True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


def ga_solve(file=None, gui=True, maxtime=0):
    """Solve using Genetic Algorithm."""
    return 0


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

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption(app_desc)
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)
    cities = []

    draw(cities)

    collecting = True

    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
            elif event.type == MOUSEBUTTONDOWN:
                cities.append(pygame.mouse.get_pos())
                draw(cities)

    screen.fill(0)
    pygame.draw.lines(screen, city_color, True, cities)
    text = font.render("Un chemin, pas le meilleur!", True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            break

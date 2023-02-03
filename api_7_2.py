import argparse
import os
import sys

import pygame
import requests


def draw_map(arg1, arg2, sap_new):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={arg1},{arg2}&spn={sap_new},{sap_new}&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    try:
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    except Exception:
        return
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    os.remove(map_file)


parser = argparse.ArgumentParser()
parser.add_argument('arg1', metavar='arg1', nargs='?')
parser.add_argument('arg2', metavar='arg2', nargs='?')
args = parser.parse_args()

spn = 10
x = args.arg1
y = args.arg2

pygame.init()
screen = pygame.display.set_mode((600, 450))
draw_map(x, y, spn)
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                spn -= 2
                if spn < 0:
                    spn += 2
                draw_map(x, y, spn)
            if event.key == pygame.K_UP:
                spn += 2
                if spn > 90:
                    spn -= 2
                draw_map(x, y, spn)
    pygame.display.flip()
    clock.tick(60)
import argparse
import os
import sys

import pygame
import requests

types = {1: "sat,skl",
         2: "sat",
         3: "map"
         }
number_type = 3

def draw_map(arg1, arg2, number_type):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={arg1},{arg2}&l={number_type}&spn=10,10&l=map"
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

x = int(args.arg1)
y = int(args.arg2)

pygame.init()
screen = pygame.display.set_mode((600, 450))
draw_map(x, y, types[number_type])
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                y -= 2
                if y < -84:
                    y += 2
                draw_map(x, y, types[number_type])
            if event.key == pygame.K_UP:
                y += 2
                if y > 84:
                    y -= 2
                draw_map(x, y, types[number_type])
            if event.key == pygame.K_LEFT:
                x -= 2
                if x < -178:
                    x = 179
                draw_map(x, y, types[number_type])
            if event.key == pygame.K_RIGHT:
                x += 2
                if x > 178:
                    x = -180
                draw_map(x, y, types[number_type])
            if event.key == pygame.K_1:
                number_type = 1
                draw_map(x, y, types[number_type])
            if event.key == pygame.K_2:
                number_type = 2
                draw_map(x, y, types[number_type])
            if event.key == pygame.K_3:
                number_type = 3
                draw_map(x, y, types[number_type])
    pygame.display.flip()
    clock.tick(60)

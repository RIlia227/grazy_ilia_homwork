import argparse
import os
import sys

import pygame
import requests


parser = argparse.ArgumentParser()
parser.add_argument('arg1', metavar='arg1', nargs='?')
parser.add_argument('arg2', metavar='arg2', nargs='?')
args = parser.parse_args()
map_request = f"http://static-maps.yandex.ru/1.x/?ll={args.arg1},{args.arg2}&spn=10,10&l=map"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
os.remove(map_file)
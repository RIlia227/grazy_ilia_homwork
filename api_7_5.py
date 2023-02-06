import argparse
import os
import sys

import pygame
import requests
from tkinter import *
from tkinter import messagebox as mb


def quit():
    global root, PLAYER_NAME
    s = entry.get()
    PLAYER_NAME = s
    root.destroy()


def size(top):
    f = top["boundedBy"]["Envelope"]["lowerCorner"].split()
    f2 = top["boundedBy"]["Envelope"]["upperCorner"].split()
    x = abs(float(f[0]) - float(f2[0]))
    y = abs(float(f[1]) - float(f2[1]))
    return str(max(x, y))


def get_pos(find):
    toponym_to_find = find
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    delta = size(toponym)
    return toponym_longitude, toponym_lattitude, delta


def draw_map(arg1, arg2, number_type, delta, m_x, m_y):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={arg1},{arg2}&l={number_type}&spn={delta},{delta}&l=map&pt={m_x},{m_y},pm2rdl"
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


number_type = 3
types = {1: "sat,skl",
         2: "sat",
         3: "map"
         }

root = Tk()
entry = Entry()
PLAYER_NAME = ""
entry.pack(pady=10)
Button(text='Искать', command=quit).pack()
label = Label(height=2)
label.place(relx=10000000, rely=10000000)
label.pack()
root.geometry('%dx%d+%d+%d' % (100, 100, 600, 400))
root.mainloop()

while True:
    if PLAYER_NAME != "":
        break
    if root:
        exit()
x, y, delta = get_pos(PLAYER_NAME)
x, y, delta = float(x), float(y), float(delta)
m_x, m_y = x, y
pygame.init()
screen = pygame.display.set_mode((600, 450))
draw_map(x, y, types[number_type], delta, m_x, m_y)
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                y -= float(delta)
                if y < -84:
                    y += float(delta)
                draw_map(x, y, types[number_type], delta, m_x, m_y)
            if event.key == pygame.K_UP:
                y += float(delta)
                if y > 84:
                    y -= float(delta)
                draw_map(x, y, types[number_type], delta, m_x, m_y)
            if event.key == pygame.K_LEFT:
                x -= float(delta)
                if x < -178:
                    x = 179
                draw_map(x, y, types[number_type], delta, m_x, m_y)
            if event.key == pygame.K_RIGHT:
                x += float(delta)
                if x > 178:
                    x = -180
                draw_map(x, y, types[number_type], delta, m_x, m_y)
            if event.key == pygame.K_1:
                number_type = 1
                draw_map(x, y, types[number_type], delta, m_x, m_y)
            if event.key == pygame.K_2:
                number_type = 2
                draw_map(x, y, types[number_type], delta, m_x, m_y)
            if event.key == pygame.K_3:
                number_type = 3
                draw_map(x, y, types[number_type], delta, m_x, m_y)
        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                delta -= 1
                if delta < 0:
                    delta += 1
                draw_map(x, y, types[number_type], delta, m_x, m_y)
            if event.y == -1:
                delta += 1
                if delta > 89:
                    delta -= 1
                draw_map(x, y, types[number_type], delta, m_x, m_y)
    pygame.display.flip()
    clock.tick(60)

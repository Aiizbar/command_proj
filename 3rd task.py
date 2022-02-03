import os
import sys

import pygame
import requests
s = input("введите координаты через пробел: ").split()
ll1 = float(s[0])
ll2 = float(s[1])
z = int(input("введите масштаб (1-17): "))

spn1 = 0.002
spn2 = 0.002
map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll1},{ll2}&spn={spn1},{spn2}&z={z}&l=map"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
speed=0.001
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                spn1+=speed
                spn2+=speed
            if event.key == pygame.K_PAGEDOWN:
                spn1 -= speed
                spn2 -= speed
            if event.key == pygame.K_UP:
                ll2+=speed
            if event.key == pygame.K_DOWN:
                ll2 -= speed
            if event.key == pygame.K_LEFT:
                ll1 -= speed
            if event.key == pygame.K_RIGHT:
                ll1 += speed

            map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll1},{ll2}&spn={spn1},{spn2}&l=map"
            response = requests.get(map_request)
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)

        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()

os.remove(map_file)


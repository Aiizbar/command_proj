import os
import sys

import pygame
import requests

pygame.init()
screen = pygame.display.set_mode((600, 450))

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

search_x =0
search_y =0
search_string = ""
search_width = 600
search_height = 60
font = pygame.font.SysFont("Times New Roman", 50)

#
# сам поиск
#
# (  уже перенесен на нужное место  )
#
# geocode_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={geo_object_name}&format=json"
# response_geocode = requests.get(geocode_request)
# json_response = response_geocode.json()
# toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# s = toponym["Point"]["pos"]
# ll1 = s[0]
# ll2 = s[1]




# Инициализируем pygame

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
            else:
                if event.key == pygame.K_RETURN:
                    geo_object_name = search_string
                    geocode_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={geo_object_name}&format=json"
                    response_geocode = requests.get(geocode_request)
                    json_response = response_geocode.json()
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    s = toponym["Point"]["pos"].split()
                    ll1 = float(s[0])
                    ll2 = float(s[1])
                    print(s)
                    print(ll1,ll2)
                elif event.key == pygame.K_BACKSPACE:
                    search_string = search_string[:len(search_string)-1]
                else:
                    search_string+=event.unicode
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll1},{ll2}&spn={spn1},{spn2}&l=map"
            response = requests.get(map_request)
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)

        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.draw.rect(screen,(255,255,255),(0,0,search_width,search_height))
        text = font.render(search_string, True, (0, 0, 0))
        screen.blit(text, (0, 0))
        pygame.display.flip()

os.remove(map_file)


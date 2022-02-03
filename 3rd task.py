import os
import sys

import pygame
import requests

# Инициализируем pygame
pygame.init()
WIDTH, HEIGHT = 1280, 720
pic_width = 650
pic_height = int(650 / WIDTH * HEIGHT)

if pic_width > 650:
    pic_width = 650
if pic_height > 450:
    pic_height = 450

screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True


class Button:
    class Names:
        scheme = 'схема'
        satellite = 'спутник'
        hybrid = 'гибрид'

    font_size = WIDTH // 55
    font = pygame.font.SysFont('Lucida Console', font_size, bold=False)
    font_bold = pygame.font.SysFont('Lucida Console', font_size, bold=True)

    color_text = (0, 0, 0)

    # width = WIDTH * 0.25

    def __init__(self, rect, text, name, centered_text=True):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.name = name
        self.centered_text = centered_text


def check_interaction(button_list):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in button_list:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    if button.text == 'текст в кнопке':
                        # что то делаем
                        pass


def draw_buttons(button_list, sc):
    for button in button_list:
        pygame.draw.rect(sc, (200, 200, 200), button.rect)
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            render = Button.font_bold.render(str(button.text), True, Button.color_text)
        else:
            render = Button.font.render(str(button.text), True, Button.color_text)

        sc.blit(render, (button.rect.x + button.rect.width / 2 - render.get_width() / 2,
                         button.rect.y + button.rect.height / 2 - render.get_height() / 2))


def get_req():
    global ll1, ll2, spn1, spn2, z, type_map, pic_width, pic_height
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll1},{ll2}&spn={spn1},{spn2}&z={z}&l={type_map}&size={pic_width},{pic_height}"
    return map_request


button_width = 300
button_height = 40
margin_width = 20
margin_height = 10

button_list = [
    Button(rect=(margin_width,
                 HEIGHT - (button_height + margin_height) * 1,
                 button_width,
                 button_height),
           text=Button.Names.scheme,
           name=Button.Names.scheme),
    Button(rect=(margin_width,
                 HEIGHT - (button_height + margin_height) * 2,
                 button_width,
                 button_height),
           text=Button.Names.satellite,
           name=Button.Names.satellite),
    Button(rect=(margin_width,
                 HEIGHT - (button_height + margin_height) * 3,
                 button_width,
                 button_height),
           text=Button.Names.hybrid,
           name=Button.Names.hybrid),
]

# s = input("введите координаты через пробел: ").split()
# ll1 = float(s[0])
# ll2 = float(s[1])
# z = int(input("введите масштаб (1-17): "))

ll1 = 37.620070
ll2 = 55.753630
z = 13
type_map = 'map'
spn1 = 0.002
spn2 = 0.002
map_request = get_req()
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
speed = 0.001

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                spn1 += speed
                spn2 += speed
            if event.key == pygame.K_PAGEDOWN:
                spn1 -= speed
                spn2 -= speed
            if event.key == pygame.K_UP:
                ll2 += speed
            if event.key == pygame.K_DOWN:
                ll2 -= speed
            if event.key == pygame.K_LEFT:
                ll1 -= speed
            if event.key == pygame.K_RIGHT:
                ll1 += speed

            map_request = get_req()
            response = requests.get(map_request)
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)

        image = pygame.image.load(map_file)
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        screen.blit(image, (0, 0))

        draw_buttons(button_list, screen)
        check_interaction(button_list)

        pygame.display.flip()

os.remove(map_file)

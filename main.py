"""
Project started at 19.02.2021
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

In this file the program is started
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

# TODO: bind different characteristics to each other
# TODO: lots of numeric constants, we should to remove it
# TODO: use properties in classes
# TODO: make collisions
# TODO: change draw_text function. It need to paste a text into left down corner
# TODO: we need to add exceptions

# TODO: для сохранения мы можем просто пихать в качестве аргумента при создании объекта словарь
# TODO: можно добавить скриншоты и запись видео

# TODO: убрать pillow, в pygame есть ширина текста

import sys
import random

import pygame
from PIL import ImageFont

import constants
from player import Player
import demon


def run_game():
    global main_game_window
    player = Player(constants.GAME_WINDOW_WIDTH // 2,
                    constants.GAME_WINDOW_HEIGHT // 2)

    shells_player = []
    enemies = create_enemies(2, 10)

    time_to_count_attack = 0
    clock = pygame.time.Clock()
    is_game_exit = False
    while not is_game_exit:
        delta = clock.tick(constants.FPS_LOCKING)
        pygame.event.pump()
        if time_to_count_attack < 500:
            time_to_count_attack += delta

        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                if time_to_count_attack >= 500:
                    time_to_count_attack = 0
                    player.set_amount_health(player.get_amount_health() - enemy.get_amount_damage())
                if player.get_amount_health() < 1:
                    return game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_pause_menu()
                if event.key == pygame.K_SPACE:
                    shell = player.attack()
                    shells_player.append(shell)

        main_game_window.fill(int())

        player.update(main_game_window)

        for shell in shells_player:
            shell.update(main_game_window)

        for enemy in enemies:
            enemy.update(main_game_window)
            enemy.attack(player.get_rect().centerx, player.get_rect().centery)

        for enemy in enemies:
            for shell in shells_player:
                if pygame.sprite.collide_rect(enemy, shell):
                    shells_player.remove(shell)
                    enemy.set_amount_health(enemy.get_amount_health() - player.get_amount_damage()
                                            - shell.get_amount_additional_damage())
                    if enemy.get_amount_health() < 0:
                        enemies.remove(enemy)

        for enemy in enemies:
            draw_bar(main_game_window, enemy.get_rect().centerx - 35,
                     enemy.get_rect().centery - enemy.get_rect().height // 2 - 7,
                     (255, 0, 0),
                     enemy.get_amount_health())
            draw_text(main_game_window, enemy.get_name(), 15, (255, 255, 255),
                      enemy.get_rect().centerx,
                      enemy.get_rect().centery - enemy.get_rect().height // 2 - 18)

        draw_bar(main_game_window, player.get_rect().centerx - 35,
                 player.get_rect().centery + player.get_rect().height // 2 + 15,
                 (255, 0, 0), player.get_amount_health())
        draw_text(main_game_window, player.get_name(), 15, (255, 255, 255),
                  player.get_rect().centerx,
                  player.get_rect().centery + player.get_rect().height // 2 + 5)

        pygame.display.flip()  # for double buffering
        pygame.display.update()
        clock.tick(constants.FPS_LOCKING)
    pygame.quit()


def show_pause_menu():
    # TODO: we don't need to calculate it, it's not good
    text_length_pixels = get_text_length_in_pixels('Pause. Press <Escape> To Continue',
                                                   30, 'resources/fonts/samson_font.ttf')
    draw_text(main_game_window, 'Pause. Press <Escape> To Continue', 30, (255, 255, 255),
              constants.GAME_WINDOW_WIDTH//2-text_length_pixels[0]//2, 10)

    clock = pygame.time.Clock()
    is_pause_over = False
    while not is_pause_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_pause_over = True

        pygame.display.update()
        clock.tick(constants.FPS_LOCKING)


def show_start_menu():
    # Можно попробовать менять не цвет выбранного пункта, а его размер, чтобы просто побольше был
    # TODO: add mouse menu control
    def set_color_active_menu_item(index_active_menu_item, color):
        if index_active_menu_item == 0:
            menu_items['New Game'] = color
        if index_active_menu_item == 1:
            menu_items['Load Game'] = color
        if index_active_menu_item == 2:
            menu_items['Settings'] = color
        if index_active_menu_item == 3:
            menu_items['Exit'] = color

    menu_background = pygame.image.load('resources/images/backgrounds/menu_background.png')

    menu_items = {
        'New Game': (255, 140, 0),
        'Load Game': (255, 255, 255),
        'Settings': (255, 255, 255),
        'Exit': (255, 255, 255)
    }
    index_selected_menu_item = 0

    is_menu_show = True
    clock = pygame.time.Clock()
    while is_menu_show:
        draw_text(main_game_window, constants.GAME_WINDOW_TITLE, 80, (255, 255, 255),
                  constants.GAME_WINDOW_WIDTH // 2, 30)

        x_to_paste_menu_item = 200
        for menu_item in menu_items.keys():
            draw_text(main_game_window, menu_item, 50, menu_items[menu_item],
                      constants.GAME_WINDOW_WIDTH//2, x_to_paste_menu_item)
            x_to_paste_menu_item += 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    index_previous_selected_item = index_selected_menu_item
                    index_selected_menu_item += 1
                    if index_selected_menu_item > 3:
                        index_selected_menu_item = 0
                        index_previous_selected_item = 3
                    set_color_active_menu_item(index_previous_selected_item, (255, 255, 255))
                    set_color_active_menu_item(index_selected_menu_item, (255, 140, 0))
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    index_previous_selected_item = index_selected_menu_item
                    index_selected_menu_item -= 1
                    if index_selected_menu_item < 0:
                        index_selected_menu_item = 3
                    set_color_active_menu_item(index_previous_selected_item, (255, 255, 255))
                    set_color_active_menu_item(index_selected_menu_item, (255, 140, 0))
                if event.key == pygame.K_RETURN:
                    if index_selected_menu_item == 0:
                        is_menu_show = False
                    if index_selected_menu_item == 1:
                        pass
                    if index_selected_menu_item == 2:
                        pass
                    if index_selected_menu_item == 3:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        main_game_window.blit(menu_background, (0, 0))
        clock.tick(constants.FPS_LOCKING)


def game_over():
    # TODO: we don't need to calculate it, it's not good
    text_length_pixels = get_text_length_in_pixels('You died. Press <Enter> To Restart Or <Escape> To Exit',
                                                   30, 'resources/fonts/samson_font.ttf')

    draw_text(main_game_window, 'You died. Press <Enter> To Restart Or <Escape> To Exit', 30, (255, 255, 255),
              text_length_pixels[0]//2-85, 10)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False

        pygame.display.update()
        clock.tick(constants.FPS_LOCKING)


def create_enemies(min_number_enemies, max_number_enemies):
    """
    Function creates enemies within the visible part of the screen
    :param min_number_enemies: lower limit of the number of enemies
    :param max_number_enemies: upper limit of the number of enemies
    :return: list of enemies
    """
    enemies_local = list()
    for i in range(min_number_enemies, max_number_enemies):
        x_for_appear_demon = random.randint(0, constants.GAME_WINDOW_WIDTH)
        y_for_appear_demon = random.randint(0, constants.GAME_WINDOW_HEIGHT)
        enemy_local = demon.Demon(x_for_appear_demon, y_for_appear_demon)
        enemies_local.append(enemy_local)
    return enemies_local


def draw_text(surface, text, size, color, x, y):
    font_name = pygame.font.match_font('resources/fonts/samson_font.ttf')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_bar(surface, x, y, color, value):
    if value < 0:
        value = 0

    bar_length = 70
    bar_height = 6

    fill = (value / 100) * bar_length
    if fill > bar_length:
        fill = bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, color, fill_rect)
    pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)


def get_text_length_in_pixels(text, size, font):
    font = ImageFont.truetype(font, size)
    length_pixels = font.getsize(text)
    return length_pixels


main_game_window = pygame.display.set_mode((constants.GAME_WINDOW_WIDTH,
                                            constants.GAME_WINDOW_HEIGHT))


def main():
    pygame.init()

    global main_game_window

    pygame.display.set_caption(constants.GAME_WINDOW_TITLE)
    icon = pygame.image.load('resources/images/icons/icon.png')
    pygame.display.set_icon(icon)

    show_start_menu()

    while run_game():
        pass


if __name__ == '__main__':
    main()

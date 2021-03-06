"""
Project started at 19.02.2021
The Game for a programming course.
Author: Alexander Tyamin
Python 3.9.2

The file describes a Map class
"""

# ! usr/bin/env python3
# -*- coding: utf8 -*-

import random

import Constants
import MapTile


class Map:
    def __init__(self):
        self._map_tiles = list()
        for init_x in range(-Constants.GAME_WINDOW_WIDTH * 2, Constants.GAME_WINDOW_WIDTH * 2,
                            random.randint(500, 524)):
            for init_y in range(-Constants.GAME_WINDOW_HEIGHT * 2, Constants.GAME_WINDOW_HEIGHT * 2,
                                random.randint(300, 340)):
                map_tile = MapTile.MapTile(init_x, init_y, 'resources/images/map/grass.png')
                self._map_tiles.append(map_tile)

    def update(self, surface):
        for map_tile in self._map_tiles:
            map_tile.update(surface)

    @property
    def map_tiles(self):
        return self._map_tiles

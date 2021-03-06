import pygame

from GameEnums import CoinTypes
from GameObject import GameObject


class Coin(GameObject):
    def __init__(self, center_x, center_y, basic_image, coin_type):
        super().__init__(center_x, center_y, basic_image)
        self._image = pygame.transform.scale(self._image, (20, 20))
        if coin_type == CoinTypes.GOLD:
            self._resource_name = 'gold_coin'
        elif coin_type == CoinTypes.SILVER:
            self._resource_name = 'silver_coin'
        elif coin_type == CoinTypes.BRONZE:
            self._resource_name = 'bronze_coin'

    @property
    def resource_name(self):
        return self._resource_name

import os
import random

import pygame
import utils
import config

class Floor:
    SPEED = 7
    CHUNKS = 3

    def __init__(self, y):
        self.floor_sprite = None
        self.load_sprite()
        self.chunk_width = self.floor_sprite.get_width()

        self.y = y

        self._chunks = []
        for x in range(self.CHUNKS):
            self._chunks.append([self.floor_sprite, x * self.chunk_width])


    def load_sprite(self):
        self.floor_sprite = pygame.transform.scale2x(pygame.image.load(os.path.join(config.TEXTURES_DIR, "base.png")).convert_alpha())


    def get_last_chunk_offset(self):
        offset = 0

        for chunk in self._chunks:
            if chunk[1] > offset:
                offset = chunk[1]

        return offset


    def move(self):
        for i, chunk in enumerate(self._chunks):
            chunk[1] -= self.SPEED

            if chunk[1] < -self.chunk_width:
                chunk[1] = self.get_last_chunk_offset() + self.chunk_width - self.SPEED


    def draw(self, screen):
        for chunk in self._chunks:
            screen.blit(chunk[0], (chunk[1], self.y))

import os
import random

import pygame
import utils
import config

class Pipe:
    GAP_SIZE = 175
    SPEED = 7

    UPPER_PIPE = None
    LOWER_PIPE = None

    def __init__(self, x):
        self.pipe_sprite = None
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        self.load_pipe_sprites()

        self.passed = False
        self.set_pipe_height()


    def load_pipe_sprites(self):
        self.pipe_sprite = pygame.transform.scale_by(pygame.image.load(os.path.join(config.TEXTURES_DIR, "pipe-green.png")).convert_alpha(), 1.5)

        self.UPPER_PIPE = pygame.transform.flip(self.pipe_sprite, False, True)
        self.LOWER_PIPE = self.pipe_sprite


    def set_pipe_height(self):
        self.height = random.randrange(40, int(config.WINDOW_SIZE[1]/2))
        self.top = self.height - self.UPPER_PIPE.get_height()
        self.bottom = self.height + self.GAP_SIZE


    def collide(self, bird, screen):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.UPPER_PIPE)
        bottom_mask = pygame.mask.from_surface(self.LOWER_PIPE)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False


    def fall(self, bird, screen):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.UPPER_PIPE)
        bottom_mask = pygame.mask.from_surface(self.LOWER_PIPE)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if t_point:
            self.UPPER_PIPE = pygame.transform.rotate(self.UPPER_PIPE, 20)
        elif b_point:
            self.LOWER_PIPE = pygame.transform.rotate(self.LOWER_PIPE, -20)


    def move(self):
        self.x -= self.SPEED


    def draw(self, screen):
        screen.blit(self.UPPER_PIPE, (self.x, self.top))
        screen.blit(self.LOWER_PIPE, (self.x, self.bottom))

import os
import random

import pygame
import utils
import config

class Bird:
    name = None
    color = None
    frames = None
    ROTATION_MAX_ANGLE = 25
    ROTATION_SPEED = 20
    ANIMATION_STEP = 5
    AVAILABLE_COLORS = ("blue", "red", "yellow", "purple", "toxic", "green", "teal", "pink", "white", "black", "orange")

    GRAVITY = 0.1
    FLAP_POWER = -2
    CLOCK = pygame.time.Clock()

    def __init__(self, name, color, x, y):
        self.name = name
        self.color = color if color in self.AVAILABLE_COLORS else random.choice(self.AVAILABLE_COLORS)
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.height = self.y
        self.anim_step = 0
        self.cframe = None

        self.load_frames()

    def load_frames(self):
        self.frames = [pygame.transform.scale_by(
            pygame.image.load(os.path.join(config.TEXTURES_DIR, "bird_" + self.color.lower() + str(x) + ".png")), 1.5)
                       for x
                       in range(1, 4)]
        self.cframe = self.frames[0]


    def jump(self):
        self.velocity = self.FLAP_POWER
        self.height = self.y


    def move(self):
        self.velocity += self.GRAVITY

        # fall = self.velocity * self.CLOCK.tick(config.FPS)
        fall = self.velocity

        if fall >= 6:
            fall = (fall/abs(fall)) * 6

        self.y += fall

        if fall < 0 or self.y < self.height + 50:  # tilt up
            if self.angle < self.ROTATION_MAX_ANGLE:
                self.angle = self.ROTATION_MAX_ANGLE
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_SPEED


    def draw(self, screen):
        self.anim_step += 1

        if self.anim_step > self.ANIMATION_STEP*6+1:
            self.anim_step = 0

        if self.angle <= -80:
            # diving
            self.cframe = self.frames[1]
        else:
            # flapping
            if self.anim_step <= self.ANIMATION_STEP:
                self.cframe = self.frames[0]
            elif self.anim_step <= self.ANIMATION_STEP*2:
                self.cframe = self.frames[1]
            elif self.anim_step <= self.ANIMATION_STEP*4:
                self.cframe = self.frames[2]
            elif self.anim_step <= self.ANIMATION_STEP*6:
                self.cframe = self.frames[1]
            elif self.anim_step <= self.ANIMATION_STEP*6+1:
                self.cframe = self.frames[0]
                self.anim_step = 0

        utils.blitSpriteRotated(screen, self.cframe, (self.x, self.y), self.angle)


    def draw_name(self, screen, font):
        c_label = font.render(self.name.capitalize(), True, (100, 100, 100))
        c_label_rect = c_label.get_rect()
        c_label_rect.center = (self.x + 25, self.y - 30)
        screen.blit(c_label, c_label_rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.cframe)

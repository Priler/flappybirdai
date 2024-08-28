import math
import os, sys
import random
import time

import pygame
import neat
import utils
import config

from GameObjects.Bird import Bird
from GameObjects.Pipe import Pipe
from GameObjects.Floor import Floor
from GameObjects.Background import Background

NAMES = ["Флафи", "Фалафель", "Ведьмак", "Лютик", "Пучеглазик", "Слайм", "Шустрый", "Следопыт",
         "Малыш", "Субарик", "Птеро", "Птенец", "Рядовой", "Опытный", "Ветеран", "Геймер",
         "Самурай", "Странник", "Вуконг", "Хануман", "Флэпи", "Райзер", "Мурамаса",
         "Клювокрыл", "Летун", "Аркадий", "Вольт", "Флэш", "Джет", "Болтун", "Молчун"]

pygame.init()
FONT__NAMES = pygame.font.SysFont("Roboto Condensed", 25)
FONT__SCORE = pygame.font.SysFont("Roboto Condensed Bold", 40)
FONT__HEADING = pygame.font.SysFont("Roboto Condensed Semibold Italic", 40)

gen = 0

def draw_all(screen, birds, pipes, floor, background, score, generation, closest_pipe):
    # Move & Draw background
    background.move()
    background.draw(screen)

    # Move & Draw pipes
    for pipe in pipes:
        pipe.move()
        pipe.draw(screen)

    # Move & Draw floor
    floor.move()
    floor.draw(screen)

    # Move & Draw birds
    for bird in birds:
        bird.draw(screen)
        bird.draw_name(screen, FONT__NAMES)

    # blit score
    score_label = FONT__SCORE.render("Очки: " + str(math.floor(score)), True, (50, 50, 50))
    score_label_rect = score_label.get_rect()
    score_label_rect.center = (config.WINDOW_SIZE[0] - 100, 50)
    screen.blit(score_label, score_label_rect)

    # blit generation
    label = FONT__HEADING.render("Поколение: " + str(gen+1), True, (0, 72, 186))
    label_rect = label.get_rect()
    label_rect.center = (config.WINDOW_SIZE[0] / 2, 25)
    screen.blit(label, label_rect)

    # update display
    pygame.display.update()


def run_game(genomes, neat_config):
    global gen
    gen += 1

    # init stuff
    screen = pygame.display.set_mode((config.WINDOW_SIZE[0], config.WINDOW_SIZE[1]))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird AI - Neuroevolution")

    # objects
    background = Background()
    birds = []
    pipes = [Pipe(config.WINDOW_SIZE[0]-50),]
    floor = Floor(config.FLOOR_POS)
    score = 0

    # init genomes
    nets = []
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, neat_config)
        nets.append(net)
        g.fitness = 0 # every genome is not successful at the start

        birds.append(Bird(random.choice(NAMES),"random",random.randrange(150, 300), random.randrange(0, 300)))


    # THE LOOP
    while True:
        clock.tick(config.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # detect the closest pipe
        cpipe = 0
        if len(birds):
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].UPPER_PIPE.get_width():
                cpipe = 1

        # move birds
        user_input = pygame.key.get_pressed()
        for bi, bird in enumerate(birds):
            genomes[bi][1].fitness += 0.1
            bird.move()

            output = nets[bi].activate(
                (bird.y, abs(bird.y - pipes[cpipe].height), abs(bird.y - pipes[cpipe].bottom), abs(pipes[cpipe].x - bird.x)))

            if output[0] > 0.5:
                # jump if neuro decided so :3
                bird.jump()

                genomes[bi][1].fitness -= 1 # every jump is punishing

            # jump key
            #if user_input[pygame.K_SPACE]:
            #    bird.jump()

        # pipes
        # add new if needed & remove passed
        tbd_pipes = []
        add_new_pipe = False

        for pipe in pipes:
            # collision check
            for bi, bird in enumerate(birds):
                if pipe.collide(bird, screen):
                    print(f"Bird {bird.name} is downm ... PIPE GOT HER!")
                    genomes[bi][1].fitness -= 1
                    nets.pop(bi)
                    genomes.pop(bi)

                    birds.pop(bi)

            # check if pipe should be removed
            if pipe.x + pipe.UPPER_PIPE.get_width() < 0:
                tbd_pipes.append(pipe)

            # check if new pipe should be added
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_new_pipe = True

        # add new pipe, if needed
        if add_new_pipe:
            if birds:
                score += 1

            pipes.append(Pipe(config.WINDOW_SIZE[0]))

            # +1 fitness to every active genome for every new pipe
            for g in genomes:
                g[1].fitness += 1

        # remove leftover pipes
        for dp in tbd_pipes:
            pipes.remove(dp)

        # remove fallen birds
        for bi, bird in enumerate(birds):
            if bird.y + bird.cframe.get_height() - 10 >= config.FLOOR_POS or bird.y <= -50:
                print(f"Bird {bird.name} has FALLEN ...")
                nets.pop(bi)
                genomes.pop(bi)

                birds.pop(bi)

        # blit
        draw_all(screen, birds, pipes, floor, background, score, None, cpipe)

        if not birds:
            time.sleep(2)
            break


if __name__ == '__main__':
    neat_config_path = "./config-feedforward.txt"
    neat_cfg = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, neat_config_path)

    # init NEAT
    p = neat.Population(neat_cfg)

    # run NEAT
    best = p.run(run_game, 1000)
    print('\nWINNER (chicken dinner) IS - \n{!s}'.format(best))

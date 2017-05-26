"""
Imports dependencies from the engine so that clients can simply
use `import engine` syntax. Inefficient, but convenient.
"""

import pygame
from engineSrc.gameobject import *
from engineSrc.position import *
from engineSrc.renderer import *


def init(windowSize):
    pygame.init()
    Renderer.setScreen(windowSize)

    done = False
    clock = pygame.time.Clock()

    while not done:
        dt = clock.tick(30)

        # TODO: refactor with Input class
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True

        GameObject.updateAll(dt)
        Renderer.renderAll(dt)

    pygame.quit()

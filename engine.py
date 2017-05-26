"""
Imports dependencies from the engine so that clients can simply
use `import engine` syntax. Inefficient, but convenient.
"""

import pygame
from engineSrc.gameobject import *
from engineSrc.position import *
from engineSrc.renderer import *
from engineSrc.camera import *


def init(windowSize):
    if not Camera.getActive():
        raise Warning("No camera created. Is this intentional?")

    pygame.init()
    Camera.setScreen(windowSize)

    done = False
    clock = pygame.time.Clock()

    while not done:
        dt = clock.tick(100) / 1000.

        # TODO: refactor with Input class
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True

        GameObject.updateAll(dt)
        Camera.getActive().render(dt)
        GameObject.lateUpdateAll(dt)

    pygame.quit()

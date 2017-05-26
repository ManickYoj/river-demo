import pygame

import position as p
import renderer as r

PX_PER_COORD = 2


class Camera (object):
    _active = None
    _screen = None
    _bgColor = None
    _screenSize = None

    @staticmethod
    def setScreen(screenSize):
        Camera._screen = pygame.display.set_mode(screenSize)
        Camera._screenSize = screenSize

    @staticmethod
    def getScreenSize():
        return Camera._screenSize

    @staticmethod
    def getScreen():
        return Camera._screen

    @staticmethod
    def getActive():
        return Camera._active

    def __init__(self, position=p.Position(0, 0), bgColor=(255, 255, 255)):
        self.position = position
        self.pxPerCoord = PX_PER_COORD
        self.bgColor = bgColor

        if Camera._active is None:
            Camera._active = self

    def isActive(self):
        return self == Camera._active

    def setActive(self):
        Camera._active = self

    def setPxPerCoord(self, pxPerCoord):
        self.pxPerCoord = pxPerCoord

    def setBGColor(self, bgColor):
        self.bgColor = bgColor

    def getRelativePosition(self, position):
        return p.Position(
            position.absX() - self.position.absX(),
            position.absY() - self.position.absY()
        )

    def coordToPx(self, position):
        relPos = self.getRelativePosition(position).asTuple()
        screenWidth, screenHeight = Camera.getScreenSize()

        return (
            screenWidth / 2 + relPos[0] * self.pxPerCoord,
            screenHeight / 2 + relPos[1] * self.pxPerCoord * -1
        )

    def render(self, dt):
        Camera._screen.fill(self.bgColor)

        # TODO: Cull render calls based on bounding boxes
        for renderable in r.Renderer.getRenderables():
            renderable.render(dt)

        pygame.display.flip()


if __name__ == "__main__":
    c = Camera()
    c.coordToPx(p.Position(0, 0))

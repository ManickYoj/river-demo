import pygame
from camera import Camera


class Renderer(object):
    _registry = {}
    _id = 0

    @staticmethod
    def getId():
        newId = Renderer._id
        Renderer._id += 1
        return newId

    @staticmethod
    def getRenderables():
        return [v for _, v in Renderer._registry.items()]

    @staticmethod
    def getScreen():
        return Camera.getScreen()

    @staticmethod
    def coordToPx(position):
        return Camera.getActive().coordToPx(position)

    def __init__(self):
        self.id = Renderer.getId()
        Renderer._registry[self.id] = self

    def __del__(self):
        del Renderer._registry[self.id]

    def render(self, dt):
        pass


class PolyRenderer(Renderer):
    def __init__(self, verts=[], color=(255, 255, 255), width=0):
        self.verts = verts
        self.color = color
        self.width = width

        super(PolyRenderer, self).__init__()

    def setVerts(self, verts):
        self.verts = verts

    def setColor(self, color):
        self.color = color

    def setWidth(self, width):
        self.width = width

    def render(self, dt):
        if self.verts is None:
            return

        # Convert to screen coordinates for rendering
        pxVerts = [Renderer.coordToPx(p) for p in self.verts]

        pygame.draw.polygon(
            Renderer.getScreen(),
            self.color,
            pxVerts,
            self.width,
        )

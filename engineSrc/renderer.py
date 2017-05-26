import pygame


class Renderer(object):
    _registry = {}
    _id = 0
    _screen = None
    _bgColor = None

    @staticmethod
    def setScreen(size, bgColor=(255, 255, 255)):
        Renderer._screen = pygame.display.set_mode(size)
        Renderer._bgColor = bgColor

    @staticmethod
    def getId():
        newId = Renderer._id
        Renderer._id += 1
        return newId

    @staticmethod
    def renderAll(dt):
        Renderer._screen.fill(Renderer._bgColor)

        for k, v in Renderer._registry.items():
            v.render(dt)

        pygame.display.flip()

    @staticmethod
    def getScreen():
        return Renderer._screen

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

        pygame.draw.polygon(
            Renderer.getScreen(),
            self.color,
            self.verts,
            self.width,
        )

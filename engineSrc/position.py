class PositionBase(object):
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y


class Position(PositionBase):
    def __init__(self, x=0, y=0, parent=None):
        self.parent = parent if parent else PositionBase(x, y)
        super(Position, self).__init__(x, y)

    def absX(self):
        return self._x + self.parent.x()

    def absY(self):
        return self._y + self.parent.y()

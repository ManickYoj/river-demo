class GameObject(object):
    _registry = {}
    _id = 0

    @staticmethod
    def getId():
        newId = GameObject._id
        GameObject._id += 1
        return newId

    @staticmethod
    def updateAll(dt):
        for obj in GameObject._registry.values():
            obj.update(dt)

    @staticmethod
    def lateUpdateAll(dt):
        for obj in GameObject._registry.values():
            obj.update(dt)

    def __init__(self):
        self.id = GameObject.getId()
        GameObject._registry[self.id] = self

    def __del__(self):
        del GameObject._registry[self.id]

    def update(self, dt):
        pass

    def lateUpdate(self, dt):
        pass

# TODO: Water momentum

import engine as e
import random as r

WINDOW_SIZE = (1000, 600)
DEFAULT_VOLUME = 5
RIVER_NODES = 80
DX_PER_NODE = 1
DY_PER_NODE = -.75
Y_NOISE = 2
DAMPING = 0.0
GRAVITY = 30


class RiverNode (object):
    def __init__(self, position):
        self.volume = DEFAULT_VOLUME
        self.position = position
        self.neighbors = []
        self.inflow = 0.0

    def addNeighbor(self, neighbor):
        self.neighbors.append({
            "ref": neighbor,
            "flowTo": 0.0,
        })

    # Getter methods
    def outflow(self):
        return sum([n["flowTo"] for n in self.neighbors if n["flowTo"] > 0])

    def inflow(self):
        return self.inflow

    def waterHeight(self):
        return self.position.absY() + self.volume

    # Update methods
    def calculateFlows(self, dt):
        for n in self.neighbors:
            deltaHeight = self.waterHeight() - n["ref"].waterHeight()
            n["flowTo"] = GRAVITY * dt * deltaHeight * (1 - DAMPING) \
                if deltaHeight > 0 else 0.0

        # Check that outflow does not exceed capacity
        # If it does, scale down outflows to match volume
        if self.volume == 0:
            return

        outflowToVolumeRatio = self.outflow() / self.volume
        if outflowToVolumeRatio > 1.0:
            for n in self.neighbors:
                n["flowTo"] /= outflowToVolumeRatio

        for n in self.neighbors:
            n["ref"].addInflow(n["flowTo"])

    def addInflow(self, volume):
        self.inflow += volume

    def reset(self):
        self.inflow = 0
        for n in self.neighbors:
            n["flowTo"] = 0

    def updateVolume(self):
        outflow = self.outflow()

        self.volume += self.inflow - outflow
        if self.volume < 0:
            self.volume = 0
        self.reset()


class River(e.GameObject):
    def __init__(self):
        # Center horizontally and vertically on camera
        self.position = e.Position(
            -RIVER_NODES * DX_PER_NODE / 2,
            -RIVER_NODES * DY_PER_NODE / 2
        )

        self.nodes = [
            RiverNode(e.Position(
                i * DX_PER_NODE,
                i * DY_PER_NODE + r.random() * Y_NOISE,
                self.position
            )) for i in range(RIVER_NODES)
        ]

        for i in range(RIVER_NODES - 1):
            self.nodes[i].addNeighbor(self.nodes[i + 1])
            self.nodes[i + 1].addNeighbor(self.nodes[i])

        self.renderer = e.PolyRenderer(
            color=(0, 0, 255),
            verts=self.getVerts()
        )

        super(River, self).__init__()

    def getVerts(self):
        vertList = []
        for n in self.nodes:
            vertList.append(e.Position(
                n.position.absX(),
                n.position.absY(),
            ))

        for n in self.nodes[::-1]:
            vertList.append(e.Position(
                n.position.absX(),
                n.waterHeight(),
            ))

        return vertList

    def update(self, dt):
        for n in self.nodes:
            n.calculateFlows(dt)

        for n in self.nodes:
            n.updateVolume()

        self.renderer.setVerts(self.getVerts())


if __name__ == "__main__":
    c = e.Camera()
    River()
    e.init(WINDOW_SIZE)

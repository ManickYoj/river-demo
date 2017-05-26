import engine as e
import random as r

WINDOW_SIZE = (1000, 400)
DEFAULT_VOLUME = 15
RIVER_NODES = 40
DAMPING = 0.6


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
    def calculateFlows(self):
        for n in self.neighbors:
            deltaHeight = self.waterHeight() - n["ref"].waterHeight()
            n["flowTo"] = deltaHeight * (1 - DAMPING) if deltaHeight > 0 else 0.0

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
        self.position = e.Position(0, 0)

        self.nodes = [
            RiverNode(e.Position(
                i * 20, 100 + 4 * i + r.randint(0, 10),
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
            vertList.append((
                n.position.absX(),
                n.position.absY(),
            ))

        for n in self.nodes[::-1]:
            vertList.append((
                n.position.absX(),
                n.waterHeight(),
            ))

        return vertList

    def update(self, dt):
        for n in self.nodes:
            n.calculateFlows()

        for n in self.nodes:
            n.updateVolume()

        self.renderer.setVerts(self.getVerts())


if __name__ == "__main__":
    River()
    e.init(WINDOW_SIZE)

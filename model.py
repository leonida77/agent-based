from mesa.model import Model
from mesa.space import MultiGrid
from agents import VacuumAgent


class VacuumModel(Model):
    def __init__(self, width=10, height=10):
        super().__init__()

        self.grid = MultiGrid(width, height, False)

        self.dirty_cells = []

        for x in range(width):
            for y in range(height):
                self.dirty_cells.append((x, y))

        self.robot = VacuumAgent(1, self)

        self.grid.place_agent(self.robot, (0, 0))

    def step(self):
        self.robot.step()
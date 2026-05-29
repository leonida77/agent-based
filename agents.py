from mesa.agent import Agent
import random


class VacuumAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
        )

        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

        cell = self.model.dirty_cells

        if new_position in cell:
            cell.remove(new_position)
            print(f"Cleaned cell {new_position}")
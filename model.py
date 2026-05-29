from mesa import Model
from mesa.space import MultiGrid

from agents import VacuumAgent
from map_loader import load_floorplan_as_grid


class VacuumModel(Model):
    def __init__(self, image_path, width=80, height=50):
        super().__init__()

        self.width = width
        self.height = height

        self.grid = MultiGrid(width, height, False)

        self.real_map = load_floorplan_as_grid(
            image_path=image_path,
            grid_width=width,
            grid_height=height
        )

        self.discovered_map = {}
        self.dirty_cells = set()

        for position, cell_type in self.real_map.items():
            self.discovered_map[position] = "unknown"

            if cell_type == "dirty":
                self.dirty_cells.add(position)

        # Почетна позиција на роботот - кај X местото од сликата
        start_position = (72, 25)
        self.start_position = start_position
        self.finished = False

        self.steps_taken = 0

        self.total_free_cells = sum(
            1
            for value in self.real_map.values()
            if value != "obstacle"
        )

        self.initial_dirty_cells = len(self.dirty_cells)

        if self.real_map[start_position] == "obstacle":
            raise Exception("Start position is inside an obstacle. Choose another position.")

        self.robot = VacuumAgent(self)
        self.grid.place_agent(self.robot, start_position)

        self.scan_area(start_position, radius=3)

    def find_start_position(self):
        for y in range(self.height):
            for x in range(self.width):
                position = (x, y)

                if self.real_map[position] == "dirty":
                    return position

        raise Exception("No free starting position found.")

    def scan_area(self, position, radius=1):
        x, y = position

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx = x + dx
                ny = y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    discovered_position = (nx, ny)
                    self.discovered_map[discovered_position] = self.real_map[discovered_position]

    def is_obstacle(self, position):
        return self.real_map.get(position) == "obstacle"

    def clean_cell(self, position):
        if position in self.dirty_cells:
            self.dirty_cells.remove(position)
            self.real_map[position] = "clean"
            self.discovered_map[position] = "clean"

    def print_discovered_map(self):
        print("\nRobot discovered map:")

        for y in range(self.height - 1, -1, -1):
            row = ""

            for x in range(self.width):
                position = (x, y)

                if self.robot.pos == position:
                    row += "R"
                elif self.discovered_map[position] == "unknown":
                    row += "?"
                elif self.discovered_map[position] == "obstacle":
                    row += "#"
                elif self.discovered_map[position] == "dirty":
                    row += "."
                elif self.discovered_map[position] == "clean":
                    row += "_"

            print(row)




    def step(self):
        self.steps_taken += 1
        self.robot.step()

    def print_statistics(self):
        discovered_cells = sum(
            1
            for value in self.discovered_map.values()
            if value != "unknown"
        )

        cleaned_cells = (
                self.initial_dirty_cells -
                len(self.dirty_cells)
        )

        coverage = (
                           discovered_cells /
                           len(self.real_map)
                   ) * 100

        cleaning_percentage = (
                                      cleaned_cells /
                                      self.initial_dirty_cells
                              ) * 100

        print("\n========== FINAL STATISTICS ==========")
        print(f"Steps Taken: {self.steps_taken}")
        print(f"Total Cells: {len(self.real_map)}")
        print(f"Discovered Cells: {discovered_cells}")
        print(f"Coverage: {coverage:.2f}%")
        print(f"Cleaned Cells: {cleaned_cells}")
        print(f"Cleaning Percentage: {cleaning_percentage:.2f}%")
        print(f"Returned Home: {self.finished}")
        print("======================================")
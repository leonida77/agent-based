from mesa import Agent
from collections import deque


class VacuumAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.path = []
        self.returning_home = False

    def step(self):
        current_position = self.pos

        self.model.scan_area(current_position, radius=3)
        self.model.clean_cell(current_position)

        if self.model.finished:
            return

        if not self.path:
            if not self.returning_home:
                self.path = self.find_path_to_frontier()

                if not self.path:
                    print("Exploration finished. Returning to start...")
                    self.returning_home = True
                    self.path = self.find_path_to_position(self.model.start_position)

            else:
                if self.pos == self.model.start_position:
                    print("Robot returned to start position. Simulation finished.")
                    self.model.finished = True
                    return

                self.path = self.find_path_to_position(self.model.start_position)

        if self.path:
            next_position = self.path.pop(0)
            self.move_to(next_position)

    def move_to(self, position):
        if self.can_move_to(position):
            self.model.grid.move_agent(self, position)
            self.model.scan_area(position, radius=3)
            self.model.clean_cell(position)
        else:
            self.path = []

    def find_path_to_frontier(self):
        start = self.pos

        queue = deque()
        queue.append((start, []))

        visited = {start}

        while queue:
            current, path = queue.popleft()

            if current != start and self.is_frontier(current):
                return path

            for neighbor in self.get_valid_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []

    def find_path_to_position(self, target):
        start = self.pos

        queue = deque()
        queue.append((start, []))

        visited = {start}

        while queue:
            current, path = queue.popleft()

            if current == target:
                return path

            for neighbor in self.get_valid_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []

    def is_frontier(self, position):
        if self.model.discovered_map[position] == "unknown":
            return False

        if self.model.is_obstacle(position):
            return False

        x, y = position

        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        for neighbor in neighbors:
            nx, ny = neighbor

            if 0 <= nx < self.model.width and 0 <= ny < self.model.height:
                if self.model.discovered_map[neighbor] == "unknown":
                    return True

        return False

    def get_valid_neighbors(self, position):
        x, y = position

        candidates = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        return [
            candidate for candidate in candidates
            if self.can_move_to(candidate)
        ]

    def can_move_to(self, position):
        x, y = position

        if x < 0 or x >= self.model.width:
            return False

        if y < 0 or y >= self.model.height:
            return False

        if self.model.is_obstacle(position):
            return False

        if self.model.discovered_map[position] == "unknown":
            return False

        return True
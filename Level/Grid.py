from dataclasses import dataclass

from api.Utils.Data import Data

@dataclass()
class Grid(Data):
    cells: list[list[str]]
    cell_size: tuple[int, int]
    def get_cell(self, x: int, y: int) -> str:
        return self.cells[y][x]
    def set_cell(self, x: int, y: int, value: str):
        self.cells[y][x] = value
    def get_size(self) -> tuple[int, int]:
        return len(self.cells[0]), len(self.cells)
    def get_neighbor(self, x: int, y: int) -> list[tuple[str, str]]:
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.cells[0]) and 0 <= ny < len(self.cells):
                neighbors.append((nx, ny))
        return neighbors
    def fill(self, x, y, width, height, value: str):
        for j in range(y, y + height):
            for i in range(x, x + width):
                self.cells[j][i] = value
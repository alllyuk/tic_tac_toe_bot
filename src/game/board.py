from dataclasses import dataclass
from typing import List


@dataclass
class Board:
    FREE_SPACE = '.'
    CROSS = 'X'
    ZERO = 'O'

    state: List[List[str]]

    @classmethod
    def create_empty(cls) -> 'Board':
        return cls([[cls.FREE_SPACE] * 3 for _ in range(3)])

    def is_cell_free(self, row: int, col: int) -> bool:
        return self.state[row][col] == self.FREE_SPACE

    def get_free_cells(self) -> List[tuple[int, int]]:
        return [(r, c) for r in range(3) for c in range(3)
                if self.is_cell_free(r, c)]

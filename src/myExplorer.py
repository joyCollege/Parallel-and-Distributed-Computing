from heapq import heappush, heappop
import time
import pygame
from typing import Tuple, List
from .explorer import Explorer  


class myExplorer(Explorer):
    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        # Manhattan Distance because the distances grid only
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        self.start_time = time.time()
        start = self.maze.start_pos
        goal = self.maze.end_pos

        open_set = []
        heappush(open_set, (self.heuristic(start, goal), 0, start, []))
        visited = set()

        while open_set:
            est_total, cost_so_far, current, path = heappop(open_set)
            if current in visited:
                continue
            visited.add(current)

            self.x, self.y = current
            self.moves = path + [current]

            if self.visualize:
                self.draw_state()

            if current == goal:
                break

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if (0 <= nx < self.maze.width and
                    0 <= ny < self.maze.height and
                    self.maze.grid[ny][nx] == 0 and
                    (nx, ny) not in visited):
                    new_cost = cost_so_far + 1
                    heappush(open_set, (
                        new_cost + self.heuristic((nx, ny), goal),
                        new_cost,
                        (nx, ny),
                        self.moves
                    ))

        self.end_time = time.time()
        time_taken = self.end_time - self.start_time

        if self.visualize:
            pygame.time.wait(2000)
            pygame.quit()

        self.print_statistics(time_taken)
        return time_taken, self.moves

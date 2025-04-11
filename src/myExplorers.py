from collections import deque
from heapq import heappush, heappop
import time
import pygame
from typing import Tuple, List
from .explorer import Explorer  

class bfs_explorer(Explorer):
    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        """
        Solve the maze using the Breadth-First Search (BFS) algorithm.

        BFS explores the maze level by level, ensuring the shortest path is found 
        by visiting the nearest unvisited positions first. It uses a queue to track 
        unexplored frontier positions and builds the path incrementally.

        Returns:
            Tuple[float, List[Tuple[int, int]]]: 
                - The total time taken to solve the maze.
                - The list of positions (x, y) representing the path from start to goal.
        """
        self.start_time = time.time()
        start = self.maze.start_pos
        goal = self.maze.end_pos

        # Implementing FIFO system
        queue = deque()
        queue.append((start, []))
        visited = set()

        while queue:
            # exploring first in
            current, path = queue.popleft()

            # skipping already explored positions
            if current in visited:
                continue
            visited.add(current)

            self.x, self.y = current
            self.moves = path + [current]

            if self.visualize:
                self.draw_state()

            if current == goal:
                break
            
            # checking all four directions 
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if (0 <= nx < self.maze.width and 
                    0 <= ny < self.maze.height and # if the position is in the maze
                    self.maze.grid[ny][nx] == 0 and # if a free space
                    (nx, ny) not in visited):
                    # adding the new positions in queue
                    queue.append(((nx, ny), self.moves))

        self.end_time = time.time()
        time_taken = self.end_time - self.start_time

        if self.visualize:
            pygame.time.wait(2000)
            pygame.quit()

        self.print_statistics(time_taken)
        return time_taken, self.moves

class a_star_explorer(Explorer):
    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        """
        Estimate the cost from node `a` to node `b` using Manhattan distance.

        This heuristic is admissible for grid-based mazes without diagonal movement,
        ensuring optimality of the A* algorithm.

        Args:
            a (Tuple[int, int]): The current node (x, y).
            b (Tuple[int, int]): The goal node (x, y).

        Returns:
            int: The estimated cost to reach `b` from `a`.
        """
        # Manhattan Distance because the distances grid only
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        """
        Solve the maze using the A* pathfinding algorithm.

        A* searches for the optimal path from the maze's start to end position by 
        evaluating both the actual path cost so far (g) and a heuristic estimate 
        to the goal (h). It uses a priority queue to explore the most promising 
        paths first.

        Returns:
            Tuple[float, List[Tuple[int, int]]]: 
                - The total time taken to solve the maze.
                - The list of positions (x, y) representing the path from start to goal.
        """
        self.start_time = time.time()
        start = self.maze.start_pos
        goal = self.maze.end_pos

        open_set = []
        heappush(open_set, (self.heuristic(start, goal), 0, start, []))
        visited = set()

        while open_set:
            # choosing the lowest total estimated cost
            est_total, cost_so_far, current, path = heappop(open_set)
            if current in visited:
                continue
            # skipping alre
            # ady explored positions
            visited.add(current)

            self.x, self.y = current
            self.moves = path + [current]

            if self.visualize:
                self.draw_state()

            if current == goal:
                break

            # checking all four directions 
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = current[0] + dx, current[1] + dy
                if (0 <= nx < self.maze.width and
                    0 <= ny < self.maze.height and  # if the position is in the maze
                    self.maze.grid[ny][nx] == 0 and # if a free space
                    (nx, ny) not in visited):

                    # update g(x)
                    new_cost = cost_so_far + 1 

                    # f(x) = g(x) + h(x)
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

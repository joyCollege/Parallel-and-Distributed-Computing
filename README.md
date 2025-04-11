# Assignment 2 Maze Explorer Game
## DSAI3202 - Parallel and Distributed Computing
## By: Dela Cruz, Joy Anne 60301959

A simple maze exploration game built with Pygame where you can either manually navigate through a maze or watch an automated solver find its way to the exit.

### How the automated maze explorer works (10 points)
The algorithm used by `explorer.py` is the right-hand rule algorithm with backtracking. It is a pathfinding method on mazes that are fully enclosed by walls. The explorer begins by keeping his right side close to the wall and continues throughout the maze keeping his right side on the wall/ This ensures that the explorer finds the target if it exists and there is a valid path. During implementation, the explorer always attempts to turn right. If there is no right turn, it moves forward. If it can't go forward, it goes left. If there are no other options, it moves backwards/turns around. The explorer repeats this until it finds the target. 

``` python3
return (self.move_history[0] == self.move_history[1] == self.move_history[2])
``` 
This particular explorer keeps a memory of the last three positions it was in. If those last three positions are the same then the explorer is deemed stuck. If it's stuck, it backtracks by trying to find a path back to a position with choices to move. If it doesn't find a valid backtrack, then it just turns around. If it is not stuck, it does the normal algorithm where it tries to move right, forward, left, or backwards in that priority.

``` python3
def print_statistics(self, time_taken: float):
   """Print detailed statistics about the exploration."""
   print("\n=== Maze Exploration Statistics ===")
   print(f"Total time taken: {time_taken:.10f} seconds")
   print(f"Total moves made: {len(self.moves)}")
   print(f"Number of backtrack operations: {self.backtrack_count}")
   print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
``` 
To keep track of the performance of the explorer, some statistics are printed out about the exploration. The total time taken indicates how long it took the explorer to find a valid path from the starting point to the target in seconds. The total moves made is the count of steps the explorer took to find that path; this includes all natural moves and backtracking moves. The number of backtrack operations are also counted and displayed. Among multiple runs on different maze types I've noticed that the backtracking operation is never used; this is likely because of the strict conditions to be in the stuck position and the algorithm's natural decision for the next step. The number of moves is divided by the total time taken to give us the average move per second, which can be used to compare how much the algorithm thinks/takes before proceeding to the next move on average

I have actually tried this technique myself on grass mazes. We ended up exploring half of the maze but the method eventually got us out. It is not the most efficient method but it does guarantee the way out.


### Question 2 (30 points)
Modify the main program to run multiple maze explorers simultaneously. This is because we want to find the best route out of the maze. Your solution should:
1. Allow running multiple explorers in parallel
2. Collect and compare statistics from all explorers
3. Display a summary of results showing which explorer performed best

*Hints*:
- To get 20 points, use use multiprocessing.
- To get 30 points, use MPI4Py on multiple machines.
- Use Celery and RabbitMQ to distribute the exploration tasks. You will get full marks plus a bonus.
- Implement a task queue system
- Do not visualize the exploration, just run it in parallel
- Store results for comparison

**To answer this question:** 
1. Study the current explorer implementation
2. Design a parallel execution system
3. Implement task distribution
4. Create a results comparison system

### Question 3 (10 points)
Analyze and compare the performance of different maze explorers on the static maze. Your analysis should:

1. Run multiple explorers (at least 4 ) simultaneously on the static maze
2. Collect and compare the following metrics for each explorer:
   - Total time taken to solve the maze
   - Number of moves made
   - *Optional*:
     - Number of backtrack operations

3. What do you notice regarding the performance of the explorers? Explain the results and the observations you made.

### Question 4 (20 points)
Based on your analysis from Question 3, propose and implement enhancements to the maze explorer to overcome its limitations. Your solution should:

1. Identify and explain the main limitations of the current explorer:

2. Propose specific improvements to the exploration algorithm:

3. Implement at least two of the proposed improvements:

Your answer should include:
1. A detailed explanation of the identified limitations
2. Documentation of your proposed improvements
3. The modified code with clear comments explaining the changes

### Question 5 (20 points)

Compare the performance of your enhanced explorer with the original:
   - Run both versions on the static maze
   - Collect and compare all relevant metrics
   - Create visualizations showing the improvements
   - Document the trade-offs of your enhancements
Your answer should include:
1. Performance comparison results and analysis
2. Discussion of any trade-offs or new limitations introduced

### Final points 6 (10 points)
1. Solve the static maze in 150 moves or less to get 10 points.
2. Solve the static maze in 135 moves or less to get 15 points.
3. Solve the static maze in 130 moves or less to get 100% in your assignment.

### Bonus points
1. Fastest solver to get top  10% routes (number of moves)
2. Finding a solution with no backtrack operations
3. Least number of moves.
# Assignment 2 Maze Explorer Game
## DSAI3202 - Parallel and Distributed Computing
## By: Dela Cruz, Joy Anne 60301959

A simple maze exploration game built with Pygame where you can either manually navigate through a maze or watch an automated solver find its way to the exit.

### Automated maze explorer overview
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


### Multiple explores with MPI4Py 
At first, I ran multiple explorers on multiple machines using MPY4Py. I ran four explorers on two machines to get the results of each explorers. The machines communicated using gather() to receive all the data from other ranks. I chose this as I've already used send and receive on the other assignment.

``` bash
=== Summary of Results ===
is_stuck definition 0, Time = 0.0017559528s, Moves = 1279, Backtracks = 0
is_stuck definition 1, Time = 0.0014426708s, Moves = 1279, Backtracks = 0
is_stuck definition 2, Time = 0.0018639565s, Moves = 1279, Backtracks = 0
is_stuck definition 3, Time = 0.0015981197s, Moves = 1279, Backtracks = 0

Fastest explorer: Rank 1 Time =  0.0014426708s, Moves = 1279, Backtracks = 0
```

All the explorers had similar results, only varying the total time spent by fractions of a second. When looking at the code, the all explorers are following the exact same algorithm on the exact same static maze map, therefore they are arriving at the same results and the differences in time is not significant.

### Performance of different maze explorers
As all of the explorers had similar results, I tried to modify the explorer while still keeping the main algorithm of the right-hand rule the same. I did this by exploring changes and backtracking. On the previous runs, backtracking has never occurred due to the strict condition to trigger the is_stuck function therefore, I tried different variations on defining the triggering function. 

I kept the original stuck condition the same—where is stuck will return true if the last three moves are the same; I added a variation of this, only needing the same position for two consecutive moves. Another condition I added is if the Explorer goes back and forth on the same two positions. The last condition I made is if the Explorer ends up in the same position after five moves.

``` bash
=== Summary of Results ===
is_stuck definition 0, Time = 0.0022592545s, Moves = 1279, Backtracks = 0
is_stuck definition 1, Time = 0.0021748543s, Moves = 1279, Backtracks = 0
is_stuck definition 2, Time = 0.0031981468s, Moves = 1279, Backtracks = 0
is_stuck definition 3, Time = 0.0019450188s, Moves = 1279, Backtracks = 0

Fastest run: Rank 3 Time =  0.0019450188s, Moves = 1279, Backtracks = 0
```

Even after defining these different stuck conditions and applying them on different ranks, the results still stayed the same. 

### Implement enhancements
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
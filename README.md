# Assignment 1 - Part 2
## DSAI3202 - Parallel and Distributed Computing
## By: Dela Cruz, Joy Anne 60301959

## Completing the Functions (10 pts)

The implementations of the following functions are provided in `src/genetic_algorithms_functions.py`:

```python
def calculate_fitness(route,
                      distance_matrix,
                      infeasible_penalty):
    """
    calculate_fitness function: total distance traveled by the car.

    Parameters:
        - route (list): A list representing the order of nodes visited in the route.
        - distance_matrix (numpy.ndarray): A matrix of the distances between nodes.
            A 2D numpy array where the element at position [i, j] represents the distance between node i and node j.
        - infeasible_penalty (int): A very high number added when the path is impossible
    Returns:
        - float: The negative total distance traveled (negative because we want to minimize distance).
           Returns a large negative penalty (infeasible_penalty) if the route is infeasible.
    """
    total_distance = 0

    for i in range(len(route) - 1):
        # Retrieve the distance between node1 and node2
        node_distance = distance_matrix[route[i], route[i + 1]]

        # If the distance is equal to 100000 (indicating an infeasible route), directly return a large negative penalty (e.g., 1e6).
        if (node_distance == 100000):
            return -infeasible_penalty
        
        total_distance += node_distance
    
    # Add the return to the starting point to complete the cycle
    return_distance = distance_matrix[route[-1], route[0]]

    if return_distance == 100000:
            return -infeasible_penalty
    
    total_distance += return_distance
    
    return -total_distance 
    

def select_in_tournament(population,
                         scores,
                         number_tournaments=4,
                         tournament_size=3):
    """
    Tournament selection for genetic algorithm.

    Parameters:
        - population (list): The current population of routes.
        - scores (np.array): The calculate_fitness scores corresponding to each individual in the population.
        - number_tournaments (int): The number of the tournamnents to run in the population.
        - tournament_size (int): The number of individual to compete in the tournaments.
            >> A larger tournament_size (4–6) might be better since the population size 10000 

    Returns:
        - list: A list of selected individuals for crossover.
    """
    # An empty list selected to store the individuals 
    selected = []
    for _ in range(number_tournaments):
        # Randomly select tournament_size individuals from the population using np.random.choice.
        tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
        # Find the index of the individual with the highest fitness score among the selected individuals using np.argmax(scores[idx])
        best_idx = tournament_indices[np.argmin(scores[tournament_indices])]
        selected.append(population[best_idx])
    return selected
    
```

### Explanation of Fixes

- **calculate_fitness:**
  - Clarified that the function returns the total distance (not a negative value).
  - Explained that if any segment is infeasible (i.e. distance equals 100000), the function returns the infeasible_penalty.
  - Improved inline comments for clarity.

- **select_in_tournament:**
  - Updated the description and parameter explanations.
  - Provided more context on why a larger tournament size might be beneficial with a large population.

Does this revised README snippet meet your needs? Let me know if you'd like any further adjustments or clarifications!

## Explain and run the algorithm (5 pts).

In the genetic algorithm trial, the distance matrix was loaded from a CSV file. This contains the distances between all the nodes. Then, a set of parameters was defined. These will be experimented with later on. Now, I generated a unique set of population. The population size is the number of routes we want to create, and the number of nodes is the number of nodes in our city—in this case, 32.

In the function, we are creating a population-sized number of routes using the permutation of nodes 1 to n. These were added into a set to ensure there are no repetitions. The set is then turned into a list, returning a list of lists.

After generating a unique population, variables were initialized. The best fitness is initialized as 1,000,000 (or 10⁶).

Now, in the main part of the genetic algorithm, we iterate through each generation. For each generation, we calculate the fitness values of each route using the calculateFitness function. This function takes in a single route, the complete distance matrix, and an infeasibility penalty to apply if a route is impossible.

For each node in a route, we retrieve the distance using the distance matrix. If the distance is impossible (indicated by 100,000), we return the infeasibility penalty. If not, this distance gets added to the total distance, and that total is returned.

Then, we check for stagnation. This occurs when the same best-calculated fitness stays the same for three to five generations. That threshold can be adjusted as a parameter. If the stagnation threshold is reached, the route with the shortest distance is kept, and the rest of the population is regenerated.

Next, we select routes for crossover using the SelectInTournament function. This function iterates for a set number of tournaments, and in each tournament, a specified number of routes are randomly chosen from the population. The route with the highest fitness score (or lowest distance, in this case) is selected as the tournament winner. All winners from each tournament are returned as a list.

Then, offspring are created from these winners using crossover. During crossover, a random subset of a route is copied directly to the offspring, and then the remaining values are taken from the other parent, ensuring no node is visited twice or more in the same route.

After obtaining all the offspring, they undergo mutation using the mutate function, which randomly swaps two nodes based on a mutation threshold.

Then, the individuals that lost in the tournament are replaced with the new offspring. The population is checked for uniqueness by turning it into a set, and any missing individuals are replaced with new random permutations.

The entire process repeats for the specified number of generations. At the end, the route with the lowest total distance in the final generation is considered the best solution.

## Parallelize the code (20 pts)

* Parallelize your program (10 pts)
* Define the parts to be distributed and parallelized, explain your choices (5 pts).
* Run your code and compute the performance metrics (5 pts).

At first, I assumed threading would improve speed because the functions are not CPU intensive, but it actually made execution much slower. 
- Sequential Execution: `7.75s`  
- ThreadPoolExecutor: `36s` 

I then tried multiprocessing using `Pool.starmap()`, but it was still slow. Even when only parallelizing fitness evaluation, the improvement was not significant. So I wanted to revisit my methodology and by timing each segment of the code. 

#### **Breaking Down Execution Time**  
```bash
=== Timing Breakdown ===
Total Execution Time: 7.75 seconds
Fitness Evaluation Time: 2.55 seconds (32.85%)
Stagnation Check Time: 0.01 seconds (0.08%)
Selection Time: 0.09 seconds (1.17%)
Crossover Time: 0.01 seconds (0.14%)
Mutation Time: 0.00 seconds (0.01%)
Replacement & Uniqueness Time: 2.72 seconds (35.07%)
**************************************************  
 test6_sequentialTimed time: 7.751987934112549  
**************************************************
```
After this I called it a day and started to improve the implementation instead. Completing the enhancement of algorithm and with the knowledge from breaking down the execution time, I tried again first parallelizing only the fitness calculation with starmap. This was way slower than the sequential. I figured implementing with non-blocking starmap_async would do better and it did run around the same time as the sequential. For this attempt of starmap_async, I added more tasks to the worker, applying granularity. Each worker is assigned a sixth of the population and this segement of population returns the mutated offspring to the main function which is aggregated and added to new replaced routes for the next generation. 

However during implementation, since we are making sure that the same routes are not added to the population again, stagnations and flushing the population with new routes/individuals took a long time so I tried to check for stagnation first before the main GA worker; this way if there was a stagnation, all the cores would be working on that first before continuing to the main GA worker. This ended up improving the speedup—this time actually running faster than the sequential. 

Below are the timings after running 200 generations with the updated code

```bash
updated_GA_trial time: 2959.8253750801086
p1_starMap_fitnessOnly time: 3025.703073501587
p2_starMapAsync_largerWorker time: 8446.1833486557
p3_starMapAsync_stagnation time: 1008.216605424881 
*********************************************************************************

**************** p1_starMap_fitnessOnly Performance Analysis ********************
Speedup             0.9782273088861825
Efficiency          0.1630378848143637

**************** p2_starMapAsync_largerWorker Performance Analysis **************
Speedup             0.3504334742568898
Efficiency          0.0584055790428150

**************** p3_starMapAsync_stagnation Performance Analysis ****************
Speedup             2.9357038548604186
Efficiency          0.4892839758100698
```

If I have time I'll check on only parallelizing the stagnation and caclculation fitness (spoiler alert: I didn't have time)

### Distributing with own machine

After distributing with mpirun -n 6 python your_script.py, I got a much faster time of 68.1564929485321, running 75 generations. 
```bash
Generation 73: Best fitness = 416.0
Generation 74: Best fitness = 416.0
Best Solution: [0, 2, 8, 19, 15, 9, 11, 21, 5, 4, 13, 22, 27, 7, 1, 28, 26, 17, 6, 30, 18, 14, 3, 20, 24, 10, 12, 16, 23, 31, 29, 25]
Total Distance: 416.0
Distributed execution time with 6n: 68.1564929485321

**************** distributed Performance Analysis ****************
Speedup             2.4835316572971728
Efficiency          0.4139219428828622
```

### Distributing with more machines
Initially, I installed Anaconda in the wrong directory (`/home/student/yes/`), which caused system conflicts and missing dependencies when trying to run Conda commands. As a result, the system kept looking for Conda in a deleted path, leading to errors when managing environments. To fix this, I removed all references to the incorrect installation from my `.bashrc` file and ensured the correct Conda path (`/home/student/anaconda3/`) was set. After reloading my shell and verifying the correct Conda installation, I attempted to restore my previous environment. However, some packages were missing or referenced old local build paths, so I manually reinstalled missing dependencies via Conda and `pip`, ensuring a clean and fully functional distributed computing setup.

```bash
Generation 196: Best fitness = 450.0
Generation 197: Best fitness = 450.0
Generation 198: Best fitness = 450.0
Generation 199: Best fitness = 450.0
Best Solution: [0, 25, 12, 21, 5, 7, 1, 28, 4, 29, 6, 24, 20, 2, 17, 26, 13, 8, 19, 15, 9, 11, 22, 3, 16, 27, 31, 23, 10, 30, 18, 14]
Total Distance: 450.0
Distributed execution time with 2n: 350.5339436531067
```
This has a a speed up of 8.44376251907 and an efficieny of 0.70364687658 across the 12 processors

## Enhance the algorithm (20 pts).

•	Distribute your algorithm over 2 machines or more (10 pts).
•	What improvements do you propose? Add them to your code (5 pts).
•	After adding your improvements, recompute the performance metrics and compare with before the enhancements (5 pts).

At this point, I also formatted the total distance output to include commas (I'm dyslexic so it makes numbers easier to read) and ensure it displays a non-negative value.  

Running with default parameters led to stagnation. Increasing `num_tournaments = 7` and `tournament_size = 20` did not significantly reduce stagnation, and the Total Distance remained 1,224.0.  

### Parameter 

I changed the parameters to reduce stagnation, but the total distance remained the same, and there was still stagnation:  
```python
# Experimental Parameters
num_nodes = distance_matrix.shape[0]
population_size     = 10000  # default = 10000
num_tournaments     = 20     # default = 4  
tournament_size     = 7      # default = 3 
mutation_rate       = 0.5    # default = 0.1
num_generations     = 200    # default = 200
infeasible_penalty  = 1e6    # default = 1e6  
stagnation_limit    = 5      # default = 5  
```

I then experimented with an extreme approach, using a high number of tournaments and larger tournament sizes, which reduced stagnation but still didn’t fully solve it.  
```python
num_tournaments = 500   # default = 4  
tournament_size = 1000  # default = 3 
mutation_rate = 1       # default = 0.1
```
Running it for longer finally reduced stagnation, improving the Total Distance to 992.0.  
```python
num_tournaments     = 500   # default = 4  
tournament_size     = 1000  # default = 3 
mutation_rate       = 1     # default = 0.1
num_generations     = 10000 # default = 200
stagnation_limit    = 2     # default = 5  
```
```
Regenerating population at generation 9998 due to stagnation
Generation 9999: Best calculate_fitness = 992.0
Total Distance: 992.0
************************************************  
 p0_sequential time: 991.6502876281738  
**************************************************
```

Later on I figured that a lower mutation_rate and longer stagnation_limit improves the grade.

### Stagnation handling
I experimented with modifying stagnation handling, Originally this didn't improve anything but it improve anything until implementing unique route generation.

```python
# Attempted a different stagnation approach (reverted)
print(f"Regenerating population at generation {generation} due to stagnation")

# Keep the top 10% best individuals
elite_count = population_size // 10  # 10% of population
best_individuals = sorted(population, key=lambda ind: calculate_fitness(ind, distance_matrix, infeasible_penalty))[:elite_count]

new_population = generate_unique_population(population_size - len(best_individuals), num_nodes)
population = best_individuals + new_population
stagnation_counter = 0
continue  # Skip rest of loop for this generation
```

### Unique route generation

I suspect it's because we are creating the same routes so in test11_running_extended.py i kept track of the routes we are checking and that was indeed the problem so after fixing it worked. This new test will be refined and added to src.updated_GA_trial.py and src.updated_GA_function.py

```bash
Generation 179: Best calculate_fitness = 515
Generation 180: Best calculate_fitness = 515
Regenerating population at generation 181 due to stagnation
Best route so far: [0, 14, 10, 7, 27, 31, 12, 29, 30, 6, 21, 9, 11, 19, 8, 13, 4, 5, 22, 2, 17, 26, 20, 24, 28, 1, 18, 23, 15, 3, 16, 25] with total distance: 515.0
Generation 182: Best calculate_fitness = 515
Generation 183: Best calculate_fitness = 515
Generation 184: Best calculate_fitness = 515
Generation 185: Best calculate_fitness = 515
Regenerating population at generation 186 due to stagnation
Best route so far: [0, 14, 10, 7, 27, 31, 12, 29, 30, 6, 21, 9, 11, 19, 8, 13, 4, 5, 22, 2, 17, 26, 20, 24, 28, 1, 18, 23, 15, 3, 16, 25] with total distance: 515.0
```
This improved the distance but the run is so so so much slower. However you can argue that each generation for the updated_run is much more productive and is worth more than one generation from the original run that stagnates a lot

```bash
original_run: 77.23450
updated_run: 2959.82537
```

## Large scale problem (10 pts)
* Run the program using the extended city map: city_distances_extended.csv. Successful execution in feasible time is rewarded with 5 pts.
* How would you add more cars to the problem? (Just explain, 5 pts).

### Run the program using the extended city map
Running the larger dataset resulted in significant stagnation, and the total distance remained 1,000,000.0, even after 2,000 generations.  

I ran with more generations and different parameters in test10_running_extended.py
```python
# Experimental Parameters 
num_nodes = distance_matrix.shape[0]
population_size     = 10000 # default = 10000
num_tournaments     = 100   # default = 4  
tournament_size     = 6     # default = 3 
mutation_rate       = 0.2   # default = 0.1
num_generations     = 10**6 # default = 200
infeasible_penalty  = 1e6   # default = 1e6  
stagnation_limit    = 10    # default = 5 
```
```bash
Generation 91287: Best calculate_fitness = 1,000,000.0
Generation 91288: Best calculate_fitness = 1,000,000.0
Regenerating population at generation 91289 due to stagnation
Generation 91290: Best calculate_fitness = 1,000,000.0

```
No path is still found after 91289 generations

Then i tried running with the modified approach of checking for route uniqueness and it still couldnt find a path after running distributedly for 8 hours.
```bash
Generation 4808: Best fitness = 1,000,000.0
Regenerating population at generation 4809 due to stagnation
Best route so far: [0, 12, 55, 45, 34, 73, 66, 42, 96, 91, 3, 8, 37, 57, 14, 22, 33, 92, 29, 58, 86, 50, 13, 9, 64, 43, 75, 16, 67, 85, 6, 68, 5, 7, 53, 79, 93, 28, 72, 94, 97, 48, 81, 95, 84, 87, 11, 82, 61, 38, 60, 44, 19, 89, 51, 24, 20, 40, 36, 88, 35, 78, 71, 23, 30, 76, 80, 1, 32, 99, 4, 62, 17, 15, 90, 41, 69, 10, 54, 59, 21, 70, 2, 65, 52, 98, 31, 25, 47, 26, 27, 56, 18, 77, 46, 49, 63, 83, 74, 39] with total distance: 1000000.0
Generation 4809: Best fitness = 1,000,000.0
Generation 4810: Best fitness = 1,000,000.0
```
(please give me points for trying)

### Add more cars to the problem
I would cluster the nodes into n groups based on their distance then I'd run GA in each clsuter of cities to find a near optimal solution.

Using GA alone, I'm assuming the nodes will be spilt into n groups with all cars stating and ending at node 0. Since GA is probabilistic, I would randomly split the cities k times to fill the population. The total fitness function and selection will still remain similar. Crossover and mutation can happen between the different car-routes.

## Bonuses 
### Implement and run the code correctly with multiple cars (5 pts).
### Use AWS to do the assignment on multiple machines (5 pts).
### Best solution in the first part (2 pts).

I believe my distance in the short run is competitive. This was from the test.test15_parallelizing_stagnation.py run; the output of which is saved in  output_test15.txt
```bash
...
Generation 437: Best fitness = 325.0
Generation 438: Best fitness = 325.0
Generation 439: Best fitness = 325.0
Generation 440: Best fitness = 325.0
Regenerating population at generation 441 due to stagnation
Best route so far: [0, 14, 10, 7, 27, 16, 31, 23, 1, 28, 24, 20, 26, 17, 2, 8, 19, 15, 9, 11, 21, 12, 29, 6, 30, 18, 5, 4, 13, 22, 3, 25] with total distance: 325.0
```

I checked if the code is correct with test12_testing_routedistance.

```bash
[0, 14, 10, 7, 27, 16, 31, 23, 1, 28, 24, 20, 26, 17, 2, 8, 19, 15, 9, 11, 21, 12, 29, 6, 30, 18, 5, 4, 13, 22, 3, 25]
All 32 node are there.
All elements are unique.
>> distance from 0 and 14 is 4.0
>> distance from 14 and 10 is 10.0
>> distance from 10 and 7 is 5.0
>> distance from 7 and 27 is 9.0
>> distance from 27 and 16 is 6.0
>> distance from 16 and 31 is 21.0
>> distance from 31 and 23 is 8.0
>> distance from 23 and 1 is 27.0
>> distance from 1 and 28 is 2.0
>> distance from 28 and 24 is 11.0
>> distance from 24 and 20 is 4.0
>> distance from 20 and 26 is 24.0
>> distance from 26 and 17 is 5.0
>> distance from 17 and 2 is 4.0
>> distance from 2 and 8 is 7.0
>> distance from 8 and 19 is 12.0
>> distance from 19 and 15 is 9.0
>> distance from 15 and 9 is 7.0
>> distance from 9 and 11 is 4.0
>> distance from 11 and 21 is 3.0
>> distance from 21 and 12 is 1.0
>> distance from 12 and 29 is 3.0
>> distance from 29 and 6 is 7.0
>> distance from 6 and 30 is 1.0
>> distance from 30 and 18 is 7.0
>> distance from 18 and 5 is 19.0
>> distance from 5 and 4 is 3.0
>> distance from 4 and 13 is 12.0
>> distance from 13 and 22 is 34.0
>> distance from 22 and 3 is 14.0
>> distance from 3 and 25 is 26.0
>> distance from 25 and 0 is 16.0
Total distance: 325.0
```
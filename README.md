# Assignment 1 - Part 2
## DSAI3202 - Parallel and Distributed Computing
## By: Dela Cruz, Joy Anne 60301959

## Completing the Functions (10 pts)

The implementations of the following functions are provided in `src/genetic_algorithms_functions.py`:

```python
def calculate_fitness(route, distance_matrix, infeasible_penalty):
    """
    Calculate the total distance traveled along a given route.

    Parameters:
        route (list): A list representing the order of nodes visited in the route.
        distance_matrix (numpy.ndarray): A 2D array where the element at [i, j] represents the distance between node i and node j.
        infeasible_penalty (int): A high penalty value returned if any segment of the route is infeasible.

    Returns:
        float: The total distance traveled along the route.
               If any segment of the route is infeasible (i.e. a distance equals 100000), the function returns the infeasible_penalty.
    """
    total_distance = 0

    for i in range(len(route) - 1):
        # Retrieve the distance between consecutive nodes.
        node_distance = distance_matrix[route[i], route[i + 1]]
        # If the distance indicates an infeasible route, return the penalty.
        if node_distance == 100000:
            return infeasible_penalty
        
        total_distance += node_distance
    
    # Complete the cycle by adding the distance from the last node back to the starting node.
    return_distance = distance_matrix[route[-1], route[0]]
    if return_distance == 100000:
        return infeasible_penalty
    
    return total_distance + return_distance
    

def select_in_tournament(population, scores, number_tournaments=4, tournament_size=3):
    """
    Perform tournament selection on the population for the genetic algorithm.

    Parameters:
        population (list): The current population of routes.
        scores (np.array): The fitness scores for each individual in the population.
        number_tournaments (int): The number of tournaments to run.
        tournament_size (int): The number of individuals competing in each tournament.
            (Note: A larger tournament size (e.g., 4–6) might be more effective given a population of 10,000.)

    Returns:
        list: A list of selected individuals chosen for crossover.
    """
    selected = []
    for _ in range(number_tournaments):
        # Randomly select 'tournament_size' individuals from the population.
        tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
        # Choose the individual with the best (lowest) fitness score among the tournament participants.
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

Below are the timings after running 75 generations. 

```bash
updated_GA_trial time: 169.268807888031
p2_starMapAsync_largerWorker time: 222.8095691204071
p3_starMapAsync_stagnation time: 144.1353316307068 

**************** p2_starMapAsync_largerWorker Performance Analysis ****************
Speedup             0.7597016975359686
Efficiency          0.1266169495893281

**************** p2_starMapAsync_largerWorker Performance Analysis ****************
Speedup             1.1743741522149433
Efficiency          0.1957290253691572
```

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



## Enhance the algorithm (20 pts).

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
SHORT RUN:
Generation 0: Best calculate_fitness = 1,395.0
Generation 1: Best calculate_fitness = 1,315.0
Generation 2: Best calculate_fitness = 1,253.0
Generation 3: Best calculate_fitness = 1,195.0
Generation 4: Best calculate_fitness = 1,195.0
Generation 5: Best calculate_fitness = 1,186.0
Generation 6: Best calculate_fitness = 1,132.0
...
Generation 104: Best calculate_fitness = 519.0
Generation 105: Best calculate_fitness = 519.0
Regenerating population at generation 106 due to stagnation
```
This also fixed the extended run to actually try and find values

## Large scale problem (10 pts)
### Run the program using the extended city map
Running the larger dataset resulted in significant stagnation, and the total distance remained 1,000,000.0, even after 2,000 generations.  
```
**************************************************  
 p0_sequential time: 3776.785297393799  
**************************************************
```

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

After implementing the unique route generation. A path was finally found. 

```
EXTENDED RUN:
eneration 0: Best calculate_fitness = 1,000,000.0
Generation 1: Best calculate_fitness = 1,000,000.0
Generation 2: Best calculate_fitness = 1,602.0
Generation 3: Best calculate_fitness = 1,602.0
Generation 4: Best calculate_fitness = 1,424.0
Generation 5: Best calculate_fitness = 1,424.0
Generation 6: Best calculate_fitness = 1,424.0
...
Generation 25: Best calculate_fitness = 1,111.0
Generation 26: Best calculate_fitness = 1,111.0
Regenerating population at generation 27 due to stagnation
```
### Add more cars to the problem
Split the node and run n car

## Bonuses 
### Implement and run the code correctly with multiple cars (5 pts).
### Use AWS to do the assignment on multiple machines (5 pts).
### Best solution in the first part (2 pts).

I believe my distance in the short run is competitive. This was from the test.test15_parallelizing_stagnation.py run; the output of which is saved in  output_test15.txt
```bash
...
Generation 194: Best fitness = 371.0
Regenerating population at generation 195 due to stagnation
Best route so far: [0, 14, 10, 7, 1, 28, 23, 16, 24, 20, 26, 17, 2, 8, 19, 15, 9, 11, 21, 6, 30, 18, 5, 4, 13, 22, 27, 31, 12, 29, 3, 25] with total distance: 371.0
Generation 196: Best fitness = 371.0
Generation 197: Best fitness = 371.0
Generation 198: Best fitness = 371.0
Generation 199: Best fitness = 371.0
Best Solution: [0, 14, 10, 7, 1, 28, 23, 16, 24, 20, 26, 17, 2, 8, 19, 15, 9, 11, 21, 6, 30, 18, 5, 4, 13, 22, 27, 31, 12, 29, 3, 25]
Total Distance: 371.0
```

I checked if the code is correct with test12_testing_routedistance.

```bash
[0, 14, 10, 7, 1, 28, 23, 16, 24, 20, 26, 17, 2, 8, 19, 15, 9, 11, 21, 6, 30, 18, 5, 4, 13, 22, 27, 31, 12, 29, 3, 25]
All 32 node are there.
All elements are unique.
>> distance from 0 and 14 is 4.0
...
>> distance from 29 and 3 is 17.0
>> distance from 3 and 25 is 26.0
Total distance: 371.0
```

After trying the the distributed run I got

```bash
Best route so far: [0, 11, 9, 15, 19, 8, 2, 17, 26, 1, 28, 24, 20, 3, 22, 13, 4, 5, 21, 6, 30, 18, 14, 10, 7, 27, 16, 23, 31, 12, 29, 25] with total distance: 349.0
Generation 147: Best fitness = 349.0
Generation 148: Best fitness = 349.0
Generation 149: Best fitness = 349.0
Generation 150: Best fitness = 349.0
Generation 151: Best fitness = 349.0
Regenerating population at generation 152 due to stagnation
```

### Best solution in the second part (5 pts).
My found distance for the long run is also competitive.
```bash
Generation 4: Best calculate_fitness = 1,424.0
Generation 5: Best calculate_fitness = 1,424.0
Generation 6: Best calculate_fitness = 1,424.0
...
Generation 25: Best calculate_fitness = 1,111.0
Generation 26: Best calculate_fitness = 1,111.0
Regenerating population at generation 27 due to stagnation
```


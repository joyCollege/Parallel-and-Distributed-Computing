# Assignment 1 - Part 2
## DSAI3202 - Parallel and Distributed Computing
## By: Dela Cruz, Joy Anne 60301959

## Understanding the code
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

## Changing the the code

in the calculate_fitness i did not put negative since we are trying to find the min in the genetic_algorithm_trial

at this point i changed the total distance to print  add commas and to give non negative

## Initial approach to improve distance 

Running with normal parameter lead to stagnation and increasing to , number_tournaments=7,tournament_size=20 did not do much to fix the stagnation the Total Distance: is still 1,224.0

i changed the parameters as an attempt to top stagnation but the total distance is the same and theres stil stagnation
        # Experimental Parameters 
        num_nodes = distance_matrix.shape[0]
        population_size     = 10000 # default = 10000
        num_tournaments     = 20    # default = 4  
        tournament_size     = 7     # default = 3 
        mutation_rate       = 0.5   # default = 0.1
        num_generations     = 200   # default = 200
        infeasible_penalty  = 1e6   # default = 1e6  
        stagnation_limit    = 5     # default = 5  
  
i changed the stagnation but it actually got worst with a distance of 2,416 to imreturning ti back but this was the attempt
                print(f"Regenerating population at generation {generation} due to stagnation")
                
                # Keep the top 10% best individuals
                elite_count = population_size // 10  # 10% of population
                best_individuals = sorted(population, key=lambda ind: calculate_fitness(ind, distance_matrix, infeasible_penalty))[:elite_count]
                
                new_population = generate_unique_population(population_size - len(best_individuals), num_nodes)
                population = best_individuals + new_population
                stagnation_counter = 0
                continue  # Skip rest of loop for this generation

 i experimented with using the new stagnant function and and a very high num_tournaments 500 and there are still stagnation and the total distance improved now being 1,211.0, adding more tournament_size 1000 did not improve the results. since theres still so much stagnation, i make the stgantion and mutation extreme giving a Total Distance: 1,074.0 which is the best one so far
        num_tournaments     = 500   # default = 4  
        tournament_size     = 1000  # default = 3 
        mutation_rate       = 1     # default = 0.1

## Parallelizing 
For this we are using the default parameters, i first assumed threading would improve the speed but it got much slower running fro 7.75s with sequential to 36 with threadingPoolExecutor then i tried Pool start with all the functions and with just the fitness evaluations and theyre all still very slow. 
 

Now I broke down the time for each process
bash```
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